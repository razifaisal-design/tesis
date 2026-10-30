"""Bab V Tahap 1 — Jaringan distribusi bertekanan + pompa (Rajawali Residence).

Membaca parameter kawasan/desain dari hidrologi.db (sumber kebenaran), menghitung
layout jaringan, los gesek Hazen-Williams (pipa tekan PVC, C = 140), titik kerja
pompa, dan daya motor. Output: tabel `jaringan_distribusi` + `pipa_tekan` +
baris baru `parameter_desain`, serta data/processed/hasil_jaringan.json.

Asumsi desain (wajib diverifikasi lapangan / disepakati dosen — mirip flag he/Lo):
- pompa bekerja jam_operasi = 8 jam/hari; Q_pompa = kebutuhan harian desain / jam kerja
- elevasi tanah = 0; muka air kolam operasi = -0,5 m (freeboard 0,5 m di atas he = 3,0 m)
- bak unit 0,5 m3 (Bab IV) dipasang di tower elevasi +2,5 m
- tekanan sisa minimum di unit terjauh = 2,0 m (20 kPa)
- kecepatan ekonomis pipa tekan 0,6-1,5 m/s
- layout siteplan (sket_lengkap.dxf): jalan induk memanjang 330,40 m (Ld),
  5 baris blok, lebar kawasan 85,78 m, sambungan rumah 12 m dari jalan ke bak unit

Urutan pipeline: setelah src/analisis_desain.py (pembaca DB yang sama, tidak
mengubah tabel lama; build_db.py meng-drop tabel baru bila DB dibangun ulang —
jalankan skrip ini lagi setelah build_db).
"""
import json
import math
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data/processed/hidrologi.db"
JSON_OUT = ROOT / "data/processed/hasil_jaringan.json"

# ---------- parameter asumsi (juga ditulis ke parameter_desain) ----------
ASUMSI = [
    ("jam_operasi_pompa", "8.0", "jam/hari", "Asumsi operasi malam hari (Bab V 3.4.4) - WAJIB disepakati dosen"),
    ("C_HazenWilliams", "140.0", "-", "Pipa tekan PVC (Tabel 2.8 aditif)"),
    ("elev_muka_air_kolam", "-0.5", "m", "Muka air operasi = dasar + he - freeboard (elevasi tanah = 0)"),
    ("elev_bak_unit", "2.5", "m", "Tandon unit 0,5 m3 di tower (asumsi tipe 36) - WAJIB diverifikasi lapangan"),
    ("tekanan_sisa_min", "2.0", "m", "Tekanan sisa di unit terjauh (20 kPa)"),
    ("v_min_tekan", "0.6", "m/s", "Kecepatan minimum pencucian-sendiri"),
    ("v_max_tekan", "1.5", "m/s", "Kecepatan ekonomis maksimum"),
    ("L_sambungan_unit", "12.0", "m", "Sambungan jalan -> bak unit (RMJ 6 m + halaman)"),
    ("n_baris_blok", "5.0", "-", "5 baris blok pada siteplan (01-160)"),
    ("n_seg_induk", "10.0", "-", "Pembagian pipa induk menjadi 10 sub-segmen (profil debit)"),
    ("lebar_kawasan_siteplan", "85.78", "m", "Lebar kawasan dr siteplan (lateral = lebar kawasan)"),
    ("eta_pompa", "0.55", "-", "Efisiensi pompa sentrifugal kecil (asumsi katalog)"),
]

# katalog pipa tekan PVC PN10 (mm) - dipilih dgn kriteria v 0,6-1,5 m/s
PIPE_TEKAN = [25, 32, 40, 50, 63, 75, 90, 110, 125, 160]
ETA_POMPA = 0.55  # efisiensi pompa sentrifugal kecil (asumsi katalog)


def hw_hf(Q_m3s: float, D_m: float, L_m: float, C: float = 140.0) -> float:
    """Los gesek Hazen-Williams (SI): hf = 10,67 L (Q/C)^1,852 / D^4,87."""
    return 10.67 * L_m * (Q_m3s / C) ** 1.852 / D_m**4.87


def pilih_D(Q_m3s: float, v_min: float, v_max: float):
    """Pilih DN terkecil dgn v <= v_max; bila semua v > v_max, pakai DN terbesar."""
    for d in PIPE_TEKAN:
        A = math.pi * (d / 1000) ** 2 / 4
        if Q_m3s / A <= v_max:
            return d
    return PIPE_TEKAN[-1]


con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

kawasan = {}
for r in cur.execute("SELECT kunci, nilai FROM kawasan"):
    try:
        kawasan[r["kunci"]] = float(r["nilai"])
    except ValueError:
        pass
hd = {r["kunci"]: r for r in cur.execute("SELECT * FROM hasil_desain")}

n_unit = int(kawasan["jumlah_unit"])
jiwa_unit = int(kawasan["jiwa_per_unit"])
q_harian = kawasan["q_kebutuhan_air"] / 1000.0          # m3/jiwa/hari
fraksi = kawasan["fraksi_desain"]
Q_hari = float(hd["Qharian_total"]["nilai"])             # 76,8 m3/hari (100%)
L_induk = float(cur.execute("SELECT nilai FROM parameter_desain WHERE kunci='Ld'").fetchone()[0])
lebar_kawasan = 85.78                                    # siteplan (m)

jam_op = 8.0
elev_muka = -0.5
elev_bak = 2.5
P_sisa = 2.0
v_min, v_max = 0.6, 1.5
L_samb = 12.0
n_lateral = 5

Q_des = Q_hari * fraksi                                  # kebutuhan harian desain
Q_pompa = Q_des / jam_op                                 # m3/jam -> pompa
Q_pompa_m3s = Q_pompa / 3600.0

# ---------- layout: induk terbagi rata (kolam di tengah), tiap lateral 1/5 Q ----------
n_seg_induk = 10                                         # 10 sub-segmen x 33 m
L_seg = L_induk / n_seg_induk
n_lat_per_sisi = n_lateral // 2 + n_lateral % 2          # lateral per sisi jalan
q_lat = Q_pompa_m3s / n_lateral

segmen = []          # (label, L, Q, D, hf)
kum_hf = 0.0         # los kumulatif jalur terburuk (dari kolam ke unit terjauh)
D_induk = None
for i in range(n_seg_induk):
    sisa_lateral = n_lateral - (i // 2) * 2 - (1 if i % 2 else 0)
    Q_seg = max(q_lat * max(sisa_lateral, 0) / 2, q_lat)  # sisi timur & barat mirip
    D = pilih_D(Q_seg, v_min, v_max)
    hf = hw_hf(Q_seg, D / 1000.0, L_seg)
    segmen.append((f"INDUK_{i+1:02d}", L_seg, Q_seg, D, hf))
    kum_hf += hf
D_induk = segmen[0][3]

# lateral terburuk (membawa 1/5 Q sepanjang lebar kawasan utk jalur terjauh)
D_lat = pilih_D(q_lat, v_min, v_max)
hf_lat = hw_hf(q_lat, D_lat / 1000.0, lebar_kawasan)
segmen.append(("LATERAL", lebar_kawasan, q_lat, D_lat, hf_lat))
kum_hf += hf_lat

# sambungan unit terjauh (1 unit dari 160: q_unit = Q_pompa/160)
q_unit = Q_pompa_m3s / n_unit
D_samb = pilih_D(q_unit, v_min, v_max)
hf_samb = hw_hf(q_unit, D_samb / 1000.0, L_samb)
segmen.append(("SAMBUNGAN_UNIT", L_samb, q_unit, D_samb, hf_samb))
kum_hf += hf_samb

# suction (kolam -> pompa rumah pompa): DN63, L 4 m, lift statis
D_suction = 63
L_suction = 4.0
hf_suction = hw_hf(Q_pompa_m3s, D_suction / 1000.0, L_suction)
lift_suction = elev_bak - elev_muka + P_sisa            # total statis + sisa
kum_hf += hf_suction                                    # los gesek suction ikut H kerja
minor = 0.10 * kum_hf                                    # rugi minor 10% los gesek

H_kerja = lift_suction + kum_hf + minor
H_pompa = math.ceil(H_kerja * 1.2 / 2) * 2              # dibulatkan - 2 m, margin 20%

P_hidro = 9810.0 * Q_pompa_m3s * H_kerja                 # watt
P_shaft = P_hidro / ETA_POMPA
P_motor = math.ceil(P_shaft / 185.0) * 185               # - seri motor 0,185 kW

# ---------- validasi ----------
masalah = []
v_induk = Q_pompa_m3s / 2 / (math.pi * (D_induk / 1000) ** 2 / 4)
if v_induk > v_max:
    masalah.append(f"v induk {v_induk:.2f} m/s > {v_max}")
for lab, L, Q, D, hf in segmen:
    v = Q / (math.pi * (D / 1000) ** 2 / 4)
    if v > v_max:
        masalah.append(f"v {lab} = {v:.2f} m/s > {v_max}")
if H_pompa < H_kerja:
    masalah.append("H pompa < H kerja")
if masalah:
    print("GAGAL:")
    for m in masalah:
        print(" -", m)
    raise SystemExit(1)

# ---------- tulis DB ----------
cur.execute("DROP TABLE IF EXISTS jaringan_distribusi")
cur.execute("""CREATE TABLE jaringan_distribusi (
    segmen TEXT, ket TEXT, L_m REAL, Q_l_det REAL, D_mm REAL, v_ms REAL, hf_m REAL)""")
baris = [("SUCTION", "Kolam -> pompa (rumah pompa)", L_suction, Q_pompa_m3s * 1000,
          D_suction, Q_pompa_m3s / (math.pi * (D_suction / 1000) ** 2 / 4), hf_suction)]
for lab, L, Q, D, hf in segmen:
    v = Q / (math.pi * (D / 1000) ** 2 / 4)
    ket = {"INDUK": "Pipa induk distribusi (per sub-segmen)",
           "LATERAL": "Lateral per baris blok (jalur terburuk)",
           "SAMBUNGAN": "Sambungan rumah -> bak unit"}[lab.split("_")[0]]
    baris.append((lab, ket, round(L, 2), round(Q * 1000, 3), D, round(v, 3), round(hf, 3)))
cur.executemany("INSERT INTO jaringan_distribusi VALUES (?,?,?,?,?,?,?)", baris)

cur.execute("DROP TABLE IF EXISTS pipa_tekan")
cur.execute("CREATE TABLE pipa_tekan (urut INTEGER, label TEXT, d_mm REAL)")
cur.executemany("INSERT INTO pipa_tekan VALUES (?,?,?)",
                [(i + 1, f"DN{d}", float(d)) for i, d in enumerate(PIPE_TEKAN)])

for kunci, nilai, satuan, ket in ASUMSI:
    cur.execute("INSERT OR REPLACE INTO parameter_desain VALUES (?,?,?,?)",
                (kunci, nilai, satuan, ket))

pompa = [
    ("pompa_Q_kerja", f"{Q_pompa:.2f}", "m3/jam",
     f"Q desain = kebutuhan {Q_des:.2f} m3/hari / {jam_op:.0f} jam operasi"),
    ("pompa_H_kerja", f"{H_kerja:.2f}", "m",
     "statis (muka air -> bak unit + tekanan sisa) + los gesek HW + rugi minor 10%"),
    ("pompa_H_terpilih", f"{H_pompa:.1f}", "m", "dibulatkan - 2 m, margin 20% thd H kerja"),
    ("pompa_P_shaft", f"{P_shaft:.0f}", "W", f"rho.g.Q.H / efisiensi {ETA_POMPA:.2f} (asumsi katalog)"),
    ("pompa_P_motor", f"{P_motor:.0f}", "W", "daya motor seri terdekat (0,185 kW kelipatan)"),
    ("pompa_unit", "2", "unit", "1 aktif + 1 cadangan (rumah pompa di FASOS)"),
    ("pompa_tipe", "0", "-", "sentrifugal permukaan (self-priming), rumah pompa di tepi kolam"),
]
for kunci, nilai, satuan, ket in pompa:
    cur.execute("INSERT OR REPLACE INTO parameter_desain VALUES (?,?,?,?)",
                (kunci, nilai, satuan, ket))
con.commit()

# ---------- JSON ----------
keluaran = dict(
    kebutuhan=dict(Q_harian_100pct=Q_hari, fraksi=fraksi, Q_desain_harian=Q_des,
                   jam_operasi=jam_op, Q_pompa=round(Q_pompa, 3)),
    layout=dict(L_induk=L_induk, n_seg_induk=n_seg_induk, L_seg=round(L_seg, 2),
                n_lateral=n_lateral, lebar_kawasan=lebar_kawasan,
                L_sambungan_unit=L_samb,
                L_total_pipa=round(sum(s[1] for s in segmen) + L_suction, 1)),
    segmen=[dict(segmen=lab, L_m=round(L, 2), Q_l_det=round(Q * 1000, 3), D_mm=D,
                 v_ms=round(Q / (math.pi * (D / 1000) ** 2 / 4), 3), hf_m=round(hf, 3))
            for lab, L, Q, D, hf in segmen],
    pompa=dict(Q=round(Q_pompa, 3), H_kerja=round(H_kerja, 2), H_terpilih=H_pompa,
               lift_statis_tekanan_sisa=round(lift_suction, 2),
               los_gesek=round(kum_hf, 2),
               minor=round(minor, 2), P_shaft=round(P_shaft), P_motor=P_motor,
               unit=2, tipe="sentrifugal permukaan self-priming"),
)
json.dump(keluaran, open(JSON_OUT, "w"), indent=1, ensure_ascii=False)
print(f"[ok] {JSON_OUT} + tabel jaringan_distribusi/pipa_tekan + parameter_desain")
print(f"  Q pompa = {Q_pompa:.2f} m3/jam @ H kerja {H_kerja:.2f} m "
      f"(terpilih {H_pompa:.0f} m), motor {P_motor} W, 2 unit")
print(f"  los gesek jalur terburuk = {kum_hf:.2f} m (L total "
      f"{sum(s[1] for s in segmen) + L_suction:.0f} m); D induk DN{D_induk}, "
      f"lateral DN{D_lat}, sambungan DN{D_samb}")
