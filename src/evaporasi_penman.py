# -*- coding: utf-8 -*-
"""Evaporasi muka air terbuka bulanan — metode Penman (1948).

Sumber data (keputusan 1 & 29 Okt 2026, REVISI.md):
- NOAA ISD Supadio (WMO 965810, ICAO WIOO): suhu udara T, titik embun Td (-> RH),
  kecepatan angin 10 m, tekanan udara.  CSV per tahun di data/raw/isd_supadio/.
- NASA POWER (CERES + MERRA-2): radiasi global Rs (MJ/m2/hari) harian 2012-2025
  di data/raw/nasa_power/NASA_POWER_daily_2012-2025.csv.

Metode — Penman (1948) "Natural Evaporation from Open Water, Bare Soil and Grass",
Proc. Royal Society A 193(1032), 120-145, persamaan kombinasi untuk muka air:

    E0 = (Delta.Rn + gamma.Ea) / (Delta + gamma)                     [mm/hari]
    Ea = 0,26.(1 + 0,54.u2).(es - ea)                                [mm/hari]
        (es-ea dalam mmHg; nilai kPa dikalikan 7,5006)

Komponen (FAO-56 utk radiasi bersih, Penman utk suku aerodinamika):
    es   = 0,6108.exp(17,27.T/(T+237,3))                             [kPa]
    ea   = RH/100 . es  (RH dari T & Td, persamaan Magnus)           [kPa]
    Delta= 4098.es/(T+237,3)^2                                       [kPa/degC]
    gamma= 0,000665.P                                                [kPa/degC]
    Rn   = Rns - Rnl; Rns = (1-alfa).Rs, alfa muka air = 0,08
    Rnl  = 4,903e-9.((TmaxK^4+TminK^4)/2).(0,34-0,14.sqrt(ea))
           .(1,35.Rs/Rso - 0,35)                                     [MJ/m2/hari]
    Rso  = (0,75+2e-5.z).Ra  (z elevasi stasiun)
    lam  = 2,501 - 0,00237.T                                         [MJ/kg]
    E0 dalam mm/hari dengan Rn dibagi lam.

Asumsi terdokumentasi:
- Penyimpanan panas muka air (G) diabaikan untuk skala bulanan.
- Angin 10 m dikoreksi ke 2 m: u2 = u10.0,748 (FAO-56).
- Albedo permukaan air 0,08 (muka air tenang, Penman 1948).
- Tekanan dari SLP ISD; bila hilang dipakai rata-rata bulan -> 1011,5 hPa.

Keluaran (ter-commit, jadi pipeline cloud tetap jalan):
- data/processed/evaporasi_penman.csv  (evaporasi bulanan mm/bulan + detail iklim)
"""
import csv
import json
import math
import calendar
import datetime

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ISD_DIR = ROOT / "data" / "raw" / "isd_supadio"
NASA = ROOT / "data" / "raw" / "nasa_power" / "NASA_POWER_daily_2012-2025.csv"
OUT_CSV = ROOT / "data" / "processed" / "evaporasi_penman.csv"
OUT_JSON = ROOT / "data" / "processed" / "evaporasi_penman.json"

LAT, LON, Z = -0.1507, 109.4039, 3.0        # Supadio (metadata ISD)
ALFA = 0.08                                  # albedo muka air
P_FALLBACK = 1011.5                          # hPa (SLP rata-rata laut)

# ---------- 1. NOAA ISD Supadio: agregasi harian ----------
def _f(sub, idx, scale, lo, hi):
    """Ambil subfield numerik ISD (mis. TMP '246,1'); None bila hilang/di luar rentang."""
    try:
        v = float(sub.split(",")[idx]) / scale
    except (ValueError, IndexError):
        return None
    return v if lo <= v <= hi else None


harian = {}
for f in sorted(ISD_DIR.glob("96581099999-*.csv")):
    with open(f, newline="") as fh:
        head = fh.readline()
        delim = ";" if head.count(";") > head.count(",") else ","
        fh.seek(0)
        for row in csv.DictReader(fh, delimiter=delim):
            tgl = row["DATE"][:10]
            T = _f(row["TMP"], 0, 10, -50, 60)
            Td = _f(row["DEW"], 0, 10, -60, 60)
            u10 = _f(row["WND"], 3, 10, 0, 100) if row["WND"].count(",") >= 4 else None
            P = _f(row["SLP"], 0, 10, 800, 1100)
            d = harian.setdefault(tgl, dict(T=[], Td=[], Tmax=[], Tmin=[], u=[], P=[]))
            if T is not None:
                d["T"].append(T)
                d["Tmax"].append(T)
                d["Tmin"].append(T)
            if Td is not None:
                d["Td"].append(Td)
            if u10 is not None:
                d["u"].append(u10)
            if P is not None:
                d["P"].append(P)

hari = {}
for tgl, d in harian.items():
    if not (d["T"] and d["Td"] and d["u"]):
        continue
    T = sum(d["T"]) / len(d["T"])
    Td = sum(d["Td"]) / len(d["Td"])
    hari[tgl] = dict(
        T=T, Tmax=max(d["Tmax"]), Tmin=min(d["Tmin"]),
        Td=Td, u2=sum(d["u"]) / len(d["u"]) * 0.748,
        P=(sum(d["P"]) / len(d["P"])) if d["P"] else None)
assert hari, f"data ISD tidak terbaca dari {ISD_DIR}"
P_bulan = {}
for tgl, d in hari.items():
    if d["P"]:
        P_bulan.setdefault(tgl[:7], []).append(d["P"])
for tgl, d in hari.items():
    if d["P"] is None:
        d["P"] = sum(P_bulan[tgl[:7]]) / len(P_bulan[tgl[:7]]) if P_bulan.get(tgl[:7]) else P_FALLBACK

# ---------- 2. NASA POWER: Rs harian ----------
nasa = {}
with open(NASA) as fh:
    lines = fh.read().splitlines()
i0 = next(i for i, ln in enumerate(lines) if ln.startswith("YEAR,DOY"))
for ln in lines[i0 + 1:]:
    if not ln.strip():
        continue
    y, doy, rs = ln.split(",")[0], ln.split(",")[1], ln.split(",")[2]
    tgl = (datetime.date(int(y), 1, 1) + datetime.timedelta(days=int(doy) - 1)).isoformat()
    nasa[tgl] = float(rs)

# ---------- 3. Penman harian ----------
def ra_mj(tgl):
    """Radiasi ekstraterestrial MJ/m2/hari (FAO-56 eq. 21)."""
    dt = datetime.date.fromisoformat(tgl)
    J = dt.timetuple().tm_yday
    dr = 1 + 0.033 * math.cos(2 * math.pi * J / 365)
    delta = 0.409 * math.sin(2 * math.pi * J / 365 - 1.39)
    phi = math.radians(LAT)
    ws = math.acos(-math.tan(phi) * math.tan(delta))
    return (1440 / math.pi) * 0.0820 * dr * (
        ws * math.sin(phi) * math.sin(delta) + math.cos(phi) * math.cos(delta) * math.sin(ws))


def penman(tgl, d, rs):
    T, Td, P = d["T"], d["Td"], d["P"]
    es = 0.6108 * math.exp(17.27 * T / (T + 237.3))
    ea = 0.6108 * math.exp(17.27 * Td / (Td + 237.3))
    ea = min(ea, es)
    rh = 100 * ea / es
    Delta = 4098 * es / (T + 237.3) ** 2
    gamma = 0.000665 * (P / 10)     # P hPa -> kPa
    rso = (0.75 + 2e-5 * Z) * ra_mj(tgl)
    ratio = min(max(rs / rso, 0.05), 1.0)
    tmaxk, tmink = d["Tmax"] + 273.16, d["Tmin"] + 273.16
    rnl = 4.903e-9 * ((tmaxk ** 4 + tmink ** 4) / 2) * (0.34 - 0.14 * math.sqrt(ea)) * (1.35 * ratio - 0.35)
    rn = (1 - ALFA) * rs - rnl
    lam = 2.501 - 0.00237 * T
    ea_pen = 0.26 * (1 + 0.54 * d["u2"]) * (es - ea) * 7.5006     # mm/hari
    e0 = (Delta * (rn / lam) + gamma * ea_pen) / (Delta + gamma)
    return e0, rh, es - ea


rekor = {}
for tgl in sorted(hari):
    if tgl in nasa:
        e0, rh, vpd = penman(tgl, hari[tgl], nasa[tgl])
        k = tgl[:7]
        r = rekor.setdefault(k, dict(e0=[], rh=[], T=[], u2=[], rs=[], vpd=[]))
        r["e0"].append(e0)
        r["rh"].append(rh)
        r["T"].append(hari[tgl]["T"])
        r["u2"].append(hari[tgl]["u2"])
        r["rs"].append(nasa[tgl])
        r["vpd"].append(vpd)

# ---------- 4. agregasi bulanan -> mm/bulan ----------
baris = []
for k in sorted(rekor):
    r = rekor[k]
    y, b = int(k[:4]), int(k[5:7])
    nd = calendar.monthrange(y, b)[1]
    e_hari = sum(r["e0"]) / len(r["e0"])
    baris.append(dict(
        bulan=b, evap_mm=e_hari * nd, e0_mm_hari=e_hari,
        t_c=sum(r["T"]) / len(r["T"]), rh_pct=sum(r["rh"]) / len(r["rh"]),
        u2_ms=sum(r["u2"]) / len(r["u2"]), rs_mj=sum(r["rs"]) / len(r["rs"]),
        n_hari_obs=len(r["e0"]), periode=k))

# rata-rata klimatologis per bulan kalender (>=1 tahun data)
klm = {}
for r in baris:
    klm.setdefault(r["bulan"], []).append(r)
evap_rows = []
for b in range(1, 13):
    rs = klm.get(b, [])
    assert rs, f"bulan {b} tidak punya data"
    evap_rows.append(dict(
        bulan=b,
        evap_mm=sum(x["evap_mm"] for x in rs) / len(rs),
        e0_mm_hari=sum(x["e0_mm_hari"] for x in rs) / len(rs),
        t_c=sum(x["t_c"] for x in rs) / len(rs),
        rh_pct=sum(x["rh_pct"] for x in rs) / len(rs),
        u2_ms=sum(x["u2_ms"] for x in rs) / len(rs),
        rs_mj=sum(x["rs_mj"] for x in rs) / len(rs),
        n_tahun=len(rs)))

with open(OUT_CSV, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["bulan", "evap_mm", "e0_mm_hari", "t_c", "rh_pct", "u2_ms", "rs_mj",
                "n_tahun", "keterangan"])
    for r in evap_rows:
        w.writerow([r["bulan"], f"{r['evap_mm']:.2f}", f"{r['e0_mm_hari']:.3f}",
                    f"{r['t_c']:.2f}", f"{r['rh_pct']:.1f}", f"{r['u2_ms']:.2f}",
                    f"{r['rs_mj']:.2f}", r["n_tahun"],
                    "Penman (1948) muka air - NOAA ISD Supadio (T, Td, u, P) + NASA POWER CERES (Rs)"])

json.dump(dict(
    metode="Penman (1948) evaporasi muka air terbuka",
    sumber=dict(isd="NOAA ISD Supadio 96581099999 (data/raw/isd_supadio/)",
                nasa="NASA POWER CERES/MERRA-2 (data/raw/nasa_power/)"),
    asumsi=dict(alfa=ALFA, G=0.0, u2="u10 x 0,748 (FAO-56)",
                Rnl="FAO-56 eq. 39 dengan Tmax/Tmin harian ISD",
                satuan_ea="mmHg (kPa x 7,5006)"),
    n_hari_terhitung=sum(len(rekor[k]["e0"]) for k in rekor),
    periode=f"{min(rekor)}..{max(rekor)}",
    bulanan=evap_rows,
    harian_per_bulan={k: dict(n=len(v["e0"]), e0=sum(v["e0"]) / len(v["e0"]))
                      for k, v in sorted(rekor.items())},
), open(OUT_JSON, "w"), indent=1)

print(f"[ok] {OUT_CSV} + {OUT_JSON}")
print(f"     {sum(len(rekor[k]['e0']) for k in rekor)} hari terhitung, periode {min(rekor)}..{max(rekor)}")
for r in evap_rows:
    print(f"     bln {r['bulan']:2d}: E0 = {r['evap_mm']:6.1f} mm/bulan "
          f"({r['e0_mm_hari']:.2f} mm/hari, T={r['t_c']:.1f} C, RH={r['rh_pct']:.0f}%, u2={r['u2_ms']:.2f} m/s)")
print(f"     rata-rata tahunan = {sum(r['evap_mm'] for r in evap_rows):.1f} mm/tahun")
