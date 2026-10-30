"""Grafik Bab V Tahap 1 (jaringan distribusi + pompa) — semua angka dari
data/processed/hasil_jaringan.json + tabel jaringan_distribusi di hidrologi.db
(semua sudah diverifikasi tools/verifikasi_excel.py).

JANGAN menghitung ulang rumus di sini; baca hasil pipeline saja.

Output: figures/gambar5-1.png (diagram skematik jaringan + pompa),
        figures/gambar5-2.png (profil los gesek & tekanan jalur terburuk).
"""

import json
import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data/processed"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

HJ = json.loads((PROC / "hasil_jaringan.json").read_text(encoding="utf-8"))
DB = sqlite3.connect(PROC / "hidrologi.db")
JRG = list(DB.execute(
    "SELECT segmen,ket,L_m,Q_l_det,D_mm,v_ms,hf_m FROM jaringan_distribusi ORDER BY rowid"))
DB.close()

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "savefig.dpi": 300,
})


def id_num(x, dec=1):
    s = f"{x:.{dec}f}"
    return s.replace(".", ",")


def save(fig, nama):
    path = FIG / nama
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  {path.relative_to(ROOT)}")


P = HJ["pompa"]
K = HJ["kebutuhan"]
L = HJ["layout"]

# ---------------- gambar5-1: diagram skematik ----------------
fig, ax = plt.subplots(figsize=(12, 6.5))
ax.set_axis_off()
ax.set_xlim(0, 120)
ax.set_ylim(0, 65)

# kolam
ax.add_patch(Rectangle((3, 12), 16, 16, fc="#bfe3f5", ec="#1f6fa8", lw=1.5))
ax.text(11, 25.5, "KOLAM RETENSI", ha="center", fontsize=9, fontweight="bold")
ax.text(11, 22.5, "15.751,7 m³\n72,5 × 72,5 × 3,0 m\nmuka air -0,5 m", ha="center",
        fontsize=7.5, va="top")

# rumah pompa
ax.add_patch(Rectangle((23, 12), 14, 12.5, fc="#ffe9b8", ec="#b8860b", lw=1.5))
ax.text(30, 22.5, "RUMAH POMPA", ha="center", fontsize=9, fontweight="bold")
ax.text(30, 20.8, f"{P['unit']} unit (1 + 1 cadangan)\nsentrifugal permukaan\n"
                  f"Q = {id_num(P['Q'], 2)} m³/jam\nH = {id_num(P['H_terpilih'], 0)} m | "
                  f"{id_num(P['P_motor'], 0)} W", ha="center", fontsize=7.5, va="top")

# suction
ax.add_patch(FancyArrowPatch((19, 20), (23, 20), arrowstyle="-|>", mutation_scale=14,
                              color="#1f6fa8", lw=2))
ax.text(21.5, 27.5, "SUCTION\nDN63, 4 m", ha="center", fontsize=7)

# pipa induk (10 sub-segmen)
x0, y0 = 37, 20
seg_w = 5.2
for i in range(10):
    x = x0 + i * seg_w
    ax.add_patch(Rectangle((x, y0 - 1.1), seg_w - 0.6, 2.2,
                           fc="#d7ecd9", ec="#2f7d32", lw=1.1))
ax.annotate("", xy=(x0 + 10 * seg_w, y0), xytext=(x0, y0),
            arrowprops=dict(arrowstyle="-|>", color="#2f7d32", lw=2))
ax.text(x0 + 5 * seg_w, y0 + 3.2,
        f"PIPA INDUK DN32 — 10 sub-segmen × {id_num(L['L_seg'], 2)} m = 330 m",
        ha="center", fontsize=8, color="#2f7d32", fontweight="bold")

# lateral + blok unit
blok_x = [42, 55, 68, 81, 94]
for i, bx in enumerate(blok_x, start=1):
    ax.add_patch(FancyArrowPatch((bx, y0 - 1.1), (bx, 9.5), arrowstyle="-|>",
                                 mutation_scale=12, color="#a84632", lw=1.4))
    ax.add_patch(Rectangle((bx - 5.2, 3.2), 10.4, 5.6, fc="#f6dedb", ec="#a84632", lw=1.2))
    ax.text(bx, 6.0, f"BLOK {i}\n32 unit", ha="center", fontsize=7.5, va="center")
ax.text(68, 11.6, f"LATERAL DN25 × 5 (masing-masing {id_num(L['lebar_kawasan'], 2)} m, "
                  f"Q/5 = {id_num(P['Q'] * 1000 / 5 / 3600, 3)} l/dtk)",
        ha="center", fontsize=8, color="#a84632", fontweight="bold")

# arah aliran utama
ax.add_patch(FancyArrowPatch((x0, y0 + 5.5), (x0 + 10 * seg_w - 2, y0 + 5.5),
                             arrowstyle="-|>", mutation_scale=12, color="#2f7d32", lw=1.2))
ax.text((x0 + x0 + 10 * seg_w) / 2, y0 + 6.6, "ALIRAN DISTRIBUSI", ha="center",
        fontsize=7.5, color="#2f7d32")

# sambungan unit (contoh di blok 5)
ax.add_patch(FancyArrowPatch((94, 3.2), (94, 1.2), arrowstyle="-|>", mutation_scale=10,
                             color="#555", lw=1))
ax.text(99.5, 2.0, "SAMBUNGAN UNIT DN25 (12 m) → bak tandon 0,5 m³ di tower +2,5 m",
        ha="left", fontsize=7.5, va="center")

# ringkasan tekanan
ax.add_patch(Rectangle((72, 36), 45, 20, fc="#f7f7f7", ec="#666", lw=1))
ax.text(74.5, 53.5, "RINGKASAN HIDROLIKA JALUR TERBURUK (kolam → unit terjauh)",
        fontsize=8.5, fontweight="bold")
baris = [
    f"Lift statis + tekanan sisa : {id_num(P['lift_statis_tekanan_sisa'], 2)} m",
    f"Los gesek Hazen-Williams   : {id_num(P['los_gesek'], 2)} m",
    f"Rugi minor (10%)           : {id_num(P['minor'], 2)} m",
    f"H kerja                    : {id_num(P['H_kerja'], 2)} m",
    f"H pompa terpilih           : {id_num(P['H_terpilih'], 0)} m (margin 20%)",
    f"Total panjang pipa         : {id_num(L['L_total_pipa'], 1)} m",
]
for i, t in enumerate(baris):
    ax.text(74.5, 50.4 - i * 2.4, t, fontsize=8, va="top", family="DejaVu Sans")

ax.text(3, 62, "DIAGRAM SKEMATIK JARINGAN DISTRIBUSI BERTEKANAN + POMPA (Rajawali Residence)",
        fontsize=11, fontweight="bold")
ax.text(3, 59, f"Kebutuhan harian desain {id_num(K['Q_desain_harian'], 2)} m³/hari "
                f"(fraksi {id_num(K['fraksi'], 2)} × {id_num(K['Q_harian_100pct'], 2)} m³) "
                f"÷ {id_num(K['jam_operasi'], 0)} jam operasi = Q pompa "
                f"{id_num(K['Q_pompa'], 2)} m³/jam", fontsize=8.5, color="#444")
ax.text(3, 0.2, "Sumber: data/processed/hasil_jaringan.json + tabel jaringan_distribusi "
        "(src/jaringan_distribusi.py). Asumsi jam operasi & elevasi bak BELUM disepakati dosen.",
        fontsize=7, color="#888")
save(fig, "gambar5-1.png")

# ---------------- gambar5-2: profil los gesek ----------------
seg = [r for r in JRG if r[0] != "SUCTION"]
LABEL_PENDEK = {"LATERAL": "LAT", "SAMBUNGAN_UNIT": "SAMB"}
labels = [LABEL_PENDEK.get(r[0], r[0].replace("INDUK_", "I")) for r in seg]
hf = [r[6] for r in seg]
D = [int(r[4]) for r in seg]
v = [r[5] for r in seg]
kum = []
s = 0.0
for h in hf:
    s += h
    kum.append(s)

fig, ax1 = plt.subplots(figsize=(11, 5.5))
warna = ["#2f7d32" if l.startswith("I") else ("#a84632" if l == "LATERAL" else "#555")
         for l in labels]
ax1.bar(labels, hf, color=warna, alpha=0.85, label="hf per segmen (m)")
ax1.set_ylabel("Los gesek hf per segmen (m)")
ax1.set_xlabel("Segmen (I01-I10 = pipa induk, LAT = lateral per baris blok, "
               "SAMB = sambungan unit terjauh)")
ax1.grid(alpha=0.3)
for i, h in enumerate(hf):
    ax1.text(i, h + 0.03, id_num(h, 2), ha="center", fontsize=7.5)

ax2 = ax1.twinx()
ax2.plot(labels, kum, "o-", color="#1f6fa8", lw=1.8, label="hf kumulatif (m)")
ax2.set_ylabel("Los gesek kumulatif (m)", color="#1f6fa8")
ax2.tick_params(axis="y", colors="#1f6fa8")
ax2.grid(False)
for i, k_ in enumerate(kum):
    if i % 3 == 0 or i == len(kum) - 1:
        ax2.text(i, k_ + 0.4, id_num(k_, 1), ha="center", fontsize=7.5, color="#1f6fa8")

h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=8.5)
ax1.set_title("Profil los gesek Hazen-Williams jalur terburuk — kolam → unit terjauh\n"
              f"(H kerja = lift statis + tekanan sisa {id_num(P['lift_statis_tekanan_sisa'], 2)} m + "
              f"los kumulatif {id_num(P['los_gesek'], 2)} m + minor {id_num(P['minor'], 2)} m = "
              f"{id_num(P['H_kerja'], 2)} m)", fontsize=10.5)
ax1.text(0.0, -0.22, "Sumber: tabel jaringan_distribusi (src/jaringan_distribusi.py); "
         "C Hazen-Williams = 140 (PVC).", transform=ax1.transAxes, fontsize=8, color="#888")
save(fig, "gambar5-2.png")
