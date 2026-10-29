# -*- coding: utf-8 -*-
"""Evaporasi muka air bulanan metode Penman (1948) — rantai hitung transparan.

Sumber data (keputusan 1 & 29 Okt 2026, REVISI.md):
- NOAA ISD Supadio (WMO 965810, ICAO WIOO): suhu udara T, suhu maks/min harian,
  titik embun Td (-> RH), kecepatan angin 10 m, tekanan udara.
  CSV per tahun di data/raw/isd_supadio/.
- NASA POWER (CERES + MERRA-2): radiasi global Rs (MJ/m2/hari) harian 2012-2025
  di data/raw/nasa_power/NASA_POWER_daily_2012-2025.csv.

Metode — Penman (1948) "Natural Evaporation from Open Water, Bare Soil and Grass",
Proc. Royal Society A 193(1032), 120-145, persamaan kombinasi untuk muka air,
dihitung dari PARAMETER IKLIM BULANAN (rata-rata harian per bulan kalender
2012-2025) supaya setiap langkah kali/bagi bisa ditampilkan sebagai formula di
sheet Evaporasi Perhitungan_Hidrologi.xlsx (tools/buat_excel.py) dan divalidasi
silang oleh tools/verifikasi_excel.py.

Rantai perhitungan (kolom di evaporasi_penman.csv = urutan kolom sheet Evaporasi):
    es   = 0,6108.exp(17,27.T/(T+237,3))                             [kPa]
    ea   = MIN(es ; 0,6108.exp(17,27.Td/(Td+237,3)))                 [kPa]
    RH   = 100.ea/es                                                 [%]
    delta= 4098.es/(T+237,3)^2                                       [kPa/degC]
    gamma= 0,000665.SLP/10                                           [kPa/degC]  (SLP hPa -> kPa)
    u2   = u10.0,748                                                 [m/s]       (FAO-56 koreksi 10 m -> 2 m)
    J    = hari ke- perwakilan bulan (tengah bulan, FAO-56 Tabel 2.1) [hari]
    dr   = 1 + 0,033.cos(2.pi.J/365)                                 [-]
    dec  = 0,409.sin(2.pi.J/365 - 1,39)                              [rad]
    ws   = ACOS(-TAN(phi).TAN(dec))                                  [rad]
    Ra   = (1440/pi).0,0820.dr.(ws.sin(phi).sin(dec)+cos(phi).cos(dec).sin(ws)) [MJ/m2/hari]
    Rso  = (0,75 + 2e-5.z).Ra                                        [MJ/m2/hari]
    ratio= MIN(MAX(Rs/Rso; 0,05); 1)                                 [-]
    Rns  = (1-alfa).Rs, alfa muka air = 0,08                         [MJ/m2/hari]
    Rnl  = 4,903e-9.((TmaxK^4+TminK^4)/2).(0,34-0,14.SQRT(ea))
           .(1,35.ratio-0,35)                                        [MJ/m2/hari] (FAO-56 eq. 39)
    Rn   = Rns - Rnl                                                 [MJ/m2/hari]
    lam  = 2,501 - 0,00237.T                                         [MJ/kg]
    Ea   = 0,26.(1+0,54.u2).(es-ea).7,5006                           [mm/hari]   (Penman; ea kPa -> mmHg)
    E0   = (delta.Rn/lam + gamma.Ea)/(delta+gamma)                   [mm/hari]
    evap = E0.n_hari                                                 [mm/bulan]

Asumsi terdokumentasi:
- Penyimpanan panas muka air (G) diabaikan untuk skala bulanan.
- Albedo permukaan air 0,08 (muka air tenang, Penman 1948).
- Tekanan = SLP harian ISD (diisi rata-rata bulan bila hilang; fallback 1011,5 hPa).
- Sudut lintang stasiun -0,1507 derajat, elevasi z = 3 m (metadata ISD).
- E0 dihitung dari parameter bulanan (bukan rata-rata E0 harian) — keduanya
  mendekati; rute bulanan dipilih agar transparan di workbook.

Keluaran (ter-commit, jadi pipeline cloud tetap jalan):
- data/processed/iklim_harian.csv      (data mentah harian gabungan ISD + NASA)
- data/processed/evaporasi_penman.csv  (parameter bulanan + SELURUH rantai Penman)
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
OUT_HARIAN = ROOT / "data" / "processed" / "iklim_harian.csv"
OUT_CSV = ROOT / "data" / "processed" / "evaporasi_penman.csv"
OUT_JSON = ROOT / "data" / "processed" / "evaporasi_penman.json"

# konstanta (harus sama persis dengan blok konstanta sheet Evaporasi)
LAT = -0.1507          # derajat, Supadio (metadata ISD)
Z = 3.0                # m, elevasi stasiun
ALFA = 0.08            # albedo muka air
F_U2 = 0.748           # koreksi angin 10 m -> 2 m (FAO-56)
K_EA = 7.5006          # kPa -> mmHg utk suku aerodinamika Penman
GSC = 0.0820           # MJ/m2/menit, konstanta surya
P_FALLBACK = 1011.5    # hPa (SLP rata-rata laut)
J_BULAN = [16, 45, 74, 105, 135, 162, 182, 213, 244, 274, 305, 335]  # hari perwakilan (FAO-56)

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
        Td=Td, u10=sum(d["u"]) / len(d["u"]),
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

# ---------- 3. tabel harian gabungan -> data/processed/iklim_harian.csv ----------
# nilai DIBULATKAN pada sumbernya (2 desimal; SLP 1) supaya agregasi bulanan di
# sini identik dengan SUMIFS pada sheet Iklim_Harian (validasi silang presisi)
baris_harian = []
for tgl in sorted(hari):
    if tgl not in nasa:
        continue
    d = hari[tgl]
    dt = datetime.date.fromisoformat(tgl)
    baris_harian.append(dict(
        tanggal=tgl, tahun=dt.year, bulan=dt.month,
        t_c=round(d["T"], 2), tmax_c=round(d["Tmax"], 2), tmin_c=round(d["Tmin"], 2),
        td_c=round(d["Td"], 2), u10_ms=round(d["u10"], 2),
        slp_hpa=round(d["P"], 1), rs_mj=round(nasa[tgl], 2)))
assert baris_harian
with open(OUT_HARIAN, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["tanggal", "tahun", "bulan", "t_c", "tmax_c", "tmin_c", "td_c",
                "u10_ms", "slp_hpa", "rs_mj"])
    for r in baris_harian:
        w.writerow([r["tanggal"], r["tahun"], r["bulan"], r["t_c"], r["tmax_c"],
                    r["tmin_c"], r["td_c"], r["u10_ms"], r["slp_hpa"], r["rs_mj"]])

# ---------- 4. parameter iklim bulanan (rata-rata harian per bulan kalender) ----------
kumpul = {b: dict(t=[], tmax=[], tmin=[], td=[], u10=[], slp=[], rs=[], n=0) for b in range(1, 13)}
for r in baris_harian:
    k = kumpul[r["bulan"]]
    k["t"].append(r["t_c"])
    k["tmax"].append(r["tmax_c"])
    k["tmin"].append(r["tmin_c"])
    k["td"].append(r["td_c"])
    k["u10"].append(r["u10_ms"])
    k["slp"].append(r["slp_hpa"])
    k["rs"].append(r["rs_mj"])
    k["n"] += 1


def rata(vals):
    return sum(vals) / len(vals)


# ---------- 5. rantai Penman bulanan (identik dengan formula sheet Evaporasi) ----------
def penman_bulanan(b):
    k = kumpul[b]
    T, Tmax, Tmin, Td = rata(k["t"]), rata(k["tmax"]), rata(k["tmin"]), rata(k["td"])
    u10, slp, rs = rata(k["u10"]), rata(k["slp"]), rata(k["rs"])
    n_hari = calendar.monthrange(2025, b)[1]     # jumlah hari kalender bulan ini
    es = 0.6108 * math.exp(17.27 * T / (T + 237.3))
    ea = min(es, 0.6108 * math.exp(17.27 * Td / (Td + 237.3)))
    rh = 100 * ea / es
    delta = 4098 * es / (T + 237.3) ** 2
    gamma = 0.000665 * slp / 10
    u2 = u10 * F_U2
    j = J_BULAN[b - 1]
    dr = 1 + 0.033 * math.cos(2 * math.pi * j / 365)
    dec = 0.409 * math.sin(2 * math.pi * j / 365 - 1.39)
    phi = math.radians(LAT)
    ws = math.acos(-math.tan(phi) * math.tan(dec))
    ra = (1440 / math.pi) * GSC * dr * (
        ws * math.sin(phi) * math.sin(dec) + math.cos(phi) * math.cos(dec) * math.sin(ws))
    rso = (0.75 + 2e-5 * Z) * ra
    ratio = min(max(rs / rso, 0.05), 1.0)
    rns = (1 - ALFA) * rs
    rnl = 4.903e-9 * (((Tmax + 273.16) ** 4 + (Tmin + 273.16) ** 4) / 2) \
        * (0.34 - 0.14 * math.sqrt(ea)) * (1.35 * ratio - 0.35)
    rn = rns - rnl
    lam = 2.501 - 0.00237 * T
    ea_pen = 0.26 * (1 + 0.54 * u2) * (es - ea) * K_EA
    e0 = (delta * (rn / lam) + gamma * ea_pen) / (delta + gamma)
    return dict(
        bulan=b, n_hari=n_hari,
        t_c=T, tmax_c=Tmax, tmin_c=Tmin, td_c=Td, u10_ms=u10, slp_hpa=slp, rs_mj=rs,
        es_kpa=es, ea_kpa=ea, rh_pct=rh, delta=delta, gamma=gamma, u2_ms=u2,
        j_hari=j, dr=dr, deklinasi=dec, omega_s=ws, ra_mj=ra, rso_mj=rso, ratio=ratio,
        rns_mj=rns, rnl_mj=rnl, rn_mj=rn, lam=lam, ea_pen_mm=ea_pen,
        e0_mm_hari=e0, evap_mm=e0 * n_hari,
        n_obs=k["n"])


kolom = ["bulan", "n_hari", "t_c", "tmax_c", "tmin_c", "td_c", "u10_ms", "slp_hpa", "rs_mj",
         "es_kpa", "ea_kpa", "rh_pct", "delta", "gamma", "u2_ms", "j_hari", "dr",
         "deklinasi", "omega_s", "ra_mj", "rso_mj", "ratio", "rns_mj", "rnl_mj", "rn_mj",
         "lam", "ea_pen_mm", "e0_mm_hari", "evap_mm"]
evap_rows = [penman_bulanan(b) for b in range(1, 13)]

with open(OUT_CSV, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(kolom + ["n_obs", "keterangan"])
    for r in evap_rows:
        w.writerow([repr(r[k]) if isinstance(r[k], float) else r[k] for k in kolom]
                   + [r["n_obs"],
                      "Penman (1948) muka air - NOAA ISD Supadio + NASA POWER, parameter bulanan 2012-2025"])

json.dump(dict(
    metode="Penman (1948) evaporasi muka air terbuka dari parameter iklim bulanan",
    sumber=dict(isd="NOAA ISD Supadio 96581099999 (data/raw/isd_supadio/)",
                nasa="NASA POWER CERES/MERRA-2 (data/raw/nasa_power/)"),
    konstanta=dict(lat=LAT, z=Z, alfa=ALFA, f_u2=F_U2, k_ea=K_EA, gsc=GSC,
                   j_perwakilan=J_BULAN),
    asumsi=dict(G=0.0, alfa=ALFA, u2="u10 x 0,748 (FAO-56)",
                Rnl="FAO-56 eq. 39 dengan Tmax/Tmin bulanan",
                satuan_ea="mmHg (kPa x 7,5006)",
                agregasi="rata-rata harian per bulan kalender 2012-2025"),
    n_hari_terhitung=len(baris_harian),
    periode=f"{baris_harian[0]['tanggal']}..{baris_harian[-1]['tanggal']}",
    kolom=kolom,
    bulanan=evap_rows,
), open(OUT_JSON, "w"), indent=1)

print(f"[ok] {OUT_HARIAN} ({len(baris_harian)} hari)")
print(f"[ok] {OUT_CSV} + {OUT_JSON}")
for r in evap_rows:
    print(f"     bln {r['bulan']:2d}: E0 = {r['e0_mm_hari']:.2f} mm/hari -> {r['evap_mm']:6.1f} mm/bulan "
          f"(T={r['t_c']:.1f} C, RH={r['rh_pct']:.0f}%, u2={r['u2_ms']:.2f} m/s, Rs={r['rs_mj']:.1f})")
print(f"     total tahunan = {sum(r['evap_mm'] for r in evap_rows):.1f} mm/tahun")
