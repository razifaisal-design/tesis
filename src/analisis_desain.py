# -*- coding: utf-8 -*-
"""Analisis desain sistem pemanenan air hujan (sesuai Proposal Tesis).
Sumber data: data/processed/hidrologi.db + data/processed/hasil_validasi.json (analisis2.py).
Output: tabel hasil_desain & neraca_bulanan ditulis ke DB, ringkasan ke data/processed/hasil_desain.json.
Rumus mengacu ke nomor persamaan OMML naskah tesis (lihat komentar [n])."""
import math
import json
import sqlite3

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "processed" / "hidrologi.db"
HV = ROOT / "data" / "processed" / "hasil_validasi.json"
HD = ROOT / "data" / "processed" / "hasil_desain.json"

con = sqlite3.connect(DB)
kaw = {k: (v, s, src) for k, v, s, src in con.execute("SELECT kunci,nilai,satuan,sumber FROM kawasan")}
par = {k: (v, s, ket) for k, v, s, ket in con.execute("SELECT kunci,nilai,satuan,keterangan FROM parameter_desain")}
evap = {b: e for b, e, _ in con.execute("SELECT bulan,evap_mm,keterangan FROM evaporasi")}
pipa = [(lab, d, a) for _, lab, d, a in con.execute("SELECT urut,label,d_mm,luas_m2 FROM pipa_standar ORDER BY urut")]
bulan = [(y, b, mm, nd) for y, b, mm, nd in con.execute(
    "SELECT tahun,bulan,mm,n_hari FROM curah_hujan_bulanan ORDER BY tahun,bulan")]

def num(d, k):
    return float(d[k][0])

n_unit = num(kaw, "jumlah_unit")
jiwa = num(kaw, "jiwa_per_unit")
atap_unit = num(kaw, "luas_atap_per_unit")
A_atap = num(kaw, "luas_atap_total")
q = num(kaw, "q_kebutuhan_air")
C = num(kaw, "C_atap")
f_des = num(kaw, "fraksi_desain")
hf = num(kaw, "freeboard")
th_des = num(kaw, "th_durasi_efektif")
Lo, S_atap = num(par, "Lo"), num(par, "S_atap")
Ld, S_pipa, n_pipa = num(par, "Ld"), num(par, "S_pipa"), num(par, "n_pipa")
he = num(par, "he_kolam")

hv = json.load(open(HV))
R24 = hv["freq"]["10"][hv["chosen"]]           # hujan rencana T=10 th, dist. terpilih (mm)
chosen = hv["chosen"]

# ---------- 1. KEBUTUHAN AIR [36] ----------
Qharian_l = n_unit * jiwa * q                  # liter/hari
Qharian = Qharian_l / 1000                     # m3/hari
FR = [1.00, 0.70, 0.65, 0.60, 0.50]

# ---------- 2. WAKTU KONSENTRASI + HIDROLIKA PIPA INDUK ----------
# to Kirpich pada permukaan ATAP [21]: to = 0,0195 (Lo/sqrt(S))^0,77 (menit)
to = 0.0195 * (Lo / math.sqrt(S_atap)) ** 0.77
A_km2 = A_atap / 1e6
D_std = [d for _, d, _ in pipa]

def d_komersial(dteor):
    for d in D_std:
        if d >= dteor * 1000:
            return d
    return D_std[-1]

# iterasi v <-> td <-> tc <-> I <-> Q <-> D (pipa induk, Manning aliran penuh [29][30][38][39])
# Catatan: umpan balik positif (v naik -> tc turun -> I naik -> Q naik) plus pembulatan
# diameter diskrit membuat iterasi ber-osilasi antara dua ukuran. Desain diambil
# konservatif (envelope): Q desain = maksimum iterasi, D teoritis dihitung dari Q tsb,
# lalu dibulatkan ke atas ke ukuran komersial.
v = 1.0
iter_rows = []
for _ in range(12):
    td_i = Ld / (60 * v)                        # [22]
    tc_i = (to + td_i) / 60                     # [20]
    I_i = (R24 / 24) * (24 / tc_i) ** (2 / 3)   # [19] Mononobe
    Q_i = 0.278 * C * I_i * A_km2               # [23] Rasional
    Dteor_i = (Q_i * n_pipa / (0.312 * math.sqrt(S_pipa))) ** (3 / 8)   # [38]
    Dkom_i = d_komersial(Dteor_i)
    A_kom = math.pi * (Dkom_i / 1000) ** 2 / 4
    v_baru = Q_i / A_kom                        # [39]
    iter_rows.append((v, td_i, tc_i, I_i, Q_i, Dteor_i, Dkom_i, v_baru))
    v = v_baru
i_max = max(range(len(iter_rows)), key=lambda i: iter_rows[i][4])
_, td, tc, I, Q, Dteor, _, _ = iter_rows[i_max]
Dkom = d_komersial(Dteor)
A_kom = math.pi * (Dkom / 1000) ** 2 / 4
v_pipa = Q / A_kom
kapasitas_pipa = (1 / n_pipa) * A_kom * (Dkom / 1000 / 4) ** (2 / 3) * math.sqrt(S_pipa)

# ---------- 3. PER UNIT: pipa penyalur (downspout), talang, bak penampung ----------
Q_unit = 0.278 * C * I * (atap_unit / 1e6)      # debit per unit (m3/dtk)
D_unit = (Q_unit * n_pipa / (0.312 * math.sqrt(S_pipa))) ** (3 / 8)
D_unit_kom = d_komersial(D_unit)
v_unit = Q_unit / (math.pi * (D_unit_kom / 1000) ** 2 / 4)
# talang: segi empat b x h, aliran terbuka Manning [29][30]
b_th, h_th, S_th, n_th = 0.15, 0.10, 0.005, 0.012
A_th, Pw_th = b_th * h_th, b_th + 2 * h_th
Rh_th = A_th / Pw_th
Q_talang = (1 / n_th) * A_th * Rh_th ** (2 / 3) * math.sqrt(S_th)
v_talang = Q_talang / A_th
# bak penampung sementara: ~1,5x kebutuhan harian unit (asumsi terdokumentasi)
V_harian_unit = jiwa * q * f_des / 1000          # m3/hari/unit
V_bak = math.ceil(V_harian_unit * 1.5 * 10) / 10

# ---------- 4. NERACA AIR BULANAN [24]-[28] + kurva massa (Rippl [27]) ----------
# Evaporasi = metode Penman muka air (src/evaporasi_penman.py), BUKAN ET0 rumput.
# Hujan langsung di permukaan kolam (P x Ap) dimasukkan sebagai pemasukan
# (keputusan 1 REVISI.md) sehingga umpan balik luas kolam menjadi negatif
# dan iterasi Vs <-> Ap konvergen.
def neraca(fraksi, ap):
    out = []
    K = 0.0
    for y, b, R, nd in bulan:
        supply = C * A_atap * R / 1000           # [24] limpasan atap
        p_pond = R * ap / 1000                   # hujan langsung di permukaan kolam
        demand = (Qharian * fraksi) * nd         # [25]
        E = evap[b] * ap / 1000                  # evaporasi Penman x luas muka kolam
        net = supply + p_pond - demand - E
        K += net
        out.append(dict(tahun=y, bulan=b, R=R, supply=supply, p_pond=p_pond,
                        demand=demand, E=E, net=net, K=K))
    Sp = 0.0
    vs = 0.0
    for r in out:
        Sp = max(Sp, r["K"])
        r["Sp"] = Sp
        r["defisit"] = Sp - r["K"]
        vs = max(vs, r["defisit"])
    total_net = out[-1]["K"]
    return out, vs, total_net

# ---------- 5. VA + KOLAM: iterasi konvergensi Vs <-> Ap + sensitivitas ----------
# Umpan balik: E dan hujan kolam bergantung luas muka (Ap), sedangkan Ap ditentukan
# Vs = fungsi(E, hujan kolam). Dengan hujan langsung dimasukkan (R > E klimatologis),
# umpan baliknya negatif dan iterasi mencapai titik tetap: Ap(Vs(Ap)) = Ap.
# Basis neraca SEMUA fraksi = Ap titik tetap (kondisi desain final) [28].
def dimensi(v):
    l = math.ceil(math.sqrt(v / he) * 2) / 2
    p = math.ceil(v / (he * l) * 2) / 2
    return p, l, p * l

Va = Q * th_des * 3600                           # [32]
p0, l0, Ap0 = dimensi(Va)                        # kolam kriteria atenuasi (titik awal iterasi)

iterasi = []
Ap_i = Ap0
for k in range(1, 21):
    _, Vs_i, tn_i = neraca(f_des, Ap_i)
    V_i = max(Vs_i, Va)                          # [33]
    p_i, l_i, Ap_baru = dimensi(V_i)
    iterasi.append(dict(i=k, Ap_masuk=Ap_i, Vs=round(Vs_i, 1), V=round(V_i, 1),
                        p=p_i, l=l_i, Ap_keluar=Ap_baru))
    if Ap_baru == Ap_i:
        Vs, V_desain, total_net = Vs_i, V_i, tn_i
        break
    Ap_i = Ap_baru
else:
    raise RuntimeError("iterasi Vs<->Ap tidak konvergen dalam 20 langkah")
p_kol, l_kol, Ap = dimensi(V_desain)             # = titik tetap (p_i, l_i, Ap_i)
V_kolam = p_kol * l_kol * he                     # [34]
htotal = he + hf                                 # [35]
Va_sens = {f"{th:g}": Q * th * 3600 for th in [0.5, 1.0, 1.5, 2.0, 3.0]}

# neraca + reliability untuk SEMUA fraksi pada basis Ap titik tetap [28]
neraca_all = {}
for f in FR:
    rows_f, vs_f, tn = neraca(f, Ap)
    S = 0.0
    n_penuh = 0
    for r in rows_f:
        muat = S + r["supply"] + r["p_pond"] - r["E"]
        r["terpenuhi"] = 1 if muat >= r["demand"] else 0
        n_penuh += r["terpenuhi"]
        S = min(V_desain, max(0.0, muat - r["demand"]))   # [26]
    neraca_all[f] = dict(rows=rows_f, vs=vs_f, total_net=tn,
                         reliability=100.0 * n_penuh / len(rows_f),
                         n_penuh=n_penuh, n_total=len(rows_f))

# ---------- 6. overflow: pipa pelimpah untuk Qin ----------
D_ov = (Q * n_pipa / (0.312 * math.sqrt(S_pipa))) ** (3 / 8)
D_ov_kom = d_komersial(D_ov)

con.close()

# ---------- simpan ke DB ----------
con = sqlite3.connect(DB)
con.execute("DELETE FROM hasil_desain")
con.execute("DELETE FROM neraca_bulanan")
hasil = [
    ("hujan_rencana_R24", R24, "mm", f"T=10 th, distribusi {chosen} (hasil_validasi.json)"),
    ("distribusi_terpilih", chosen, "-", "uji chi-kuadrat"),
    ("Qharian_total", Qharian, "m3/hari", "[36] 160 unit x 4 jiwa x 120 l"),
    ("to_kirpich", to, "menit", "[21] pada atap"),
    ("tc", tc, "jam", "[20] to+td, hasil iterasi"),
    ("td", td, "menit", "[22] Ld/(60.v)"),
    ("I_mononobe", I, "mm/jam", "[19]"),
    ("Q_rasional", Q, "m3/dtk", "[23] seluruh atap kawasan"),
    ("D_teoris_induk", round(Dteor * 1000, 1), "mm", "[38] Manning penuh"),
    ("D_komersial_induk", Dkom, "mm", "pipa standar"),
    ("v_pipa_induk", round(v_pipa, 3), "m/dtk", "[39] verifikasi"),
    ("kapasitas_pipa_induk", round(kapasitas_pipa, 4), "m3/dtk", "Manning penuh"),
    ("Q_unit", round(Q_unit, 5), "m3/dtk", "per unit (atap 65 m2)"),
    ("D_komersial_unit", D_unit_kom, "mm", "pipa penyalur per unit"),
    ("v_unit", round(v_unit, 3), "m/dtk", "[39]"),
    ("Q_kapasitas_talang", round(Q_talang, 5), "m3/dtk", f"segi empat {b_th}x{h_th} m, S={S_th}"),
    ("V_bak_unit", V_bak, "m3", "asumsi 1,5x kebutuhan harian unit"),
    ("Va", round(Va, 1), "m3", f"[32] Qin.th, th={th_des:g} jam"),
    ("Ap_kriteria_Va", Ap0, "m2", f"luas kolam kriteria atenuasi ({p0}x{l0} m) - titik awal iterasi"),
    ("Vs", round(Vs, 1), "m3", f"[27] Rippl fraksi 65% pada Ap titik tetap ({Ap:g} m2)"),
    ("iterasi_konvergen", json.dumps(iterasi), "-", "iterasi Vs<->Ap sampai titik tetap (rincian di hasil_desain.json)"),
    ("V_desain", round(V_desain, 1), "m3", "[33] maks(Vs, Va) pada titik tetap"),
    ("p_kolam", p_kol, "m", "panjang kolam"),
    ("l_kolam", l_kol, "m", "lebar kolam"),
    ("he_kolam", he, "m", "kedalaman efektif"),
    ("hf_freeboard", hf, "m", "[35]"),
    ("htotal", htotal, "m", "[35]"),
    ("Ap_kolam", Ap, "m2", "luas permukaan (titik tetap iterasi Vs<->Ap)"),
    ("D_overflow", D_ov_kom, "mm", "pipa pelimpah utk Qin"),
    ("n_bulan", len(bulan), "bulan", "periode neraca 2012-2025"),
    ("total_net_65", round(total_net, 1), "m3", "neraca kumulatif fraksi 65%"),
]
for f in FR:
    hasil.append((f"Vs_fraksi_{f:.2f}", round(neraca_all[f]["vs"], 1), "m3", "kebutuhan tampungan [27]"))
    hasil.append((f"reliability_{f:.2f}", round(neraca_all[f]["reliability"], 1), "%",
                  f"[28] terpenuhi {neraca_all[f]['n_penuh']}/{neraca_all[f]['n_total']} bln"))
hasil.append(("Va_sensitivitas", json.dumps(Va_sens), "m3", "th 0,5-3 jam [3.4.3]"))
con.executemany("INSERT INTO hasil_desain VALUES (?,?,?,?)", hasil)
con.executemany("INSERT INTO neraca_bulanan VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                [(r["tahun"], r["bulan"], f, round(r["supply"], 2), round(r["p_pond"], 2),
                  round(r["demand"], 2), round(r["E"], 2), round(r["net"], 2), round(r["K"], 2),
                  round(r["defisit"], 2), r["terpenuhi"])
                 for f in FR for r in neraca_all[f]["rows"]])
con.commit()
con.close()

json.dump(dict(
    R24=R24, distribusi=chosen, Qharian=Qharian,
    hidrolika=dict(to=to, td=td, tc=tc, I=I, Q=Q, Dteor=Dteor, Dkom=Dkom, v=v_pipa,
                   kapasitas=kapasitas_pipa, C=C, A_km2=A_km2, iterasi=iter_rows),
    unit=dict(Q_unit=Q_unit, D_kom=D_unit_kom, v=v_unit,
              Q_talang=Q_talang, v_talang=v_talang, V_bak=V_bak),
    kolam=dict(Va=Va, Vs=Vs, Ap_kriteria_Va=Ap0, iterasi_konvergen=iterasi,
               V_desain=V_desain, p=p_kol, l=l_kol, he=he, hf=hf,
               htotal=htotal, Ap=Ap, D_overflow=D_ov_kom, Va_sensitivitas=Va_sens),
    neraca={f"{f:.2f}": dict(vs=neraca_all[f]["vs"], reliability=neraca_all[f]["reliability"],
                             total_net=neraca_all[f]["total_net"]) for f in FR},
), open(HD, "w"), indent=1)

print(f"[ok] {HD} + tabel hasil_desain & neraca_bulanan di DB")
print(f"  R24 ({chosen}) = {R24:.2f} mm | I = {I:.2f} mm/jam | Q = {Q:.4f} m3/dtk")
print(f"  to = {to:.2f} mnt | td = {td:.2f} mnt | tc = {tc:.4f} jam")
print(f"  pipa induk: D teoritis {Dteor*1000:.0f} mm -> komersial {Dkom:.0f} mm, v = {v_pipa:.2f} m/dtk")
print(f"  per unit: Q = {Q_unit*1000:.2f} l/dtk, pipa {D_unit_kom:.0f} mm, talang kapasitas {Q_talang*1000:.2f} l/dtk")
print(f"  iterasi Vs<->Ap ({len(iterasi)} langkah): " +
      " -> ".join(f"Ap={it['Ap_masuk']:g}->{it['Ap_keluar']:g}" for it in iterasi) +
      f" | titik tetap Ap = {Ap:g} m2")
print(f"  kolam: Vs = {Vs:.0f} | Va = {Va:.0f} | Vdesain = {V_desain:.0f} m3 -> {p_kol} x {l_kol} x {he} m (+freeboard {hf} m)")
print(f"  reliability fraksi: " + " | ".join(f"{f:.0%}: {neraca_all[f]['reliability']:.1f}%" for f in FR))
