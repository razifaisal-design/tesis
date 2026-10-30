"""Grafik Bab 4 (Tahap 3) — semua angka dibaca dari data/processed (DB + JSON).

JANGAN menghitung ulang rumus hidrologi di sini; setiap nilai berasal dari
hasil_validasi.json, hasil_desain.json, atau tabel di hidrologi.db yang sudah
divalidasi tools/verifikasi_excel.py.

Output: figures/gambar4-1.png .. gambar4-8.png (dpi 300, label Bahasa Indonesia).
Jalankan setelah pipeline inti (build_db -> analisis2 -> analisis_desain).
"""

import json
import math
import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data" / "processed"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

VAL = json.loads((PROC / "hasil_validasi.json").read_text(encoding="utf-8"))
DES = json.loads((PROC / "hasil_desain.json").read_text(encoding="utf-8"))
DB = sqlite3.connect(PROC / "hidrologi.db")

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "figure.dpi": 100,
    "savefig.dpi": 300,
})

BULAN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]


def id_num(x, dec=1):
    """Format angka gaya Indonesia (koma desimal)."""
    s = f"{x:,.{dec}f}"
    return s.replace(",", "\u2063").replace(".", ",").replace("\u2063", ".")


def id_fmt(dec=1):
    return FuncFormatter(lambda v, _: id_num(v, dec))


def save(fig, nama):
    path = FIG / nama
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"  {path.relative_to(ROOT)}")


# --------------------------------------------------------------- Grafik 4.1
def grafik_hujan_tahunan():
    tahun = VAL["years"]
    total = [VAL["per_year"][str(y)]["total"] for y in tahun]
    xmax = [VAL["per_year"][str(y)]["xmax"] for y in tahun]

    fig, ax1 = plt.subplots(figsize=(8.5, 4.2))
    ax1.bar(tahun, total, color="#4C72B0", label="Total curah hujan tahunan", zorder=2)
    ax1.set_xlabel("Tahun")
    ax1.set_ylabel("Total curah hujan (mm)")
    ax1.set_xticks(tahun)
    ax1.tick_params(axis="x", rotation=45)
    ax1.set_ylim(0, max(total) * 1.25)
    ax1.yaxis.set_major_formatter(id_fmt(0))

    ax2 = ax1.twinx()
    ax2.grid(False)
    ax2.plot(tahun, xmax, "o-", color="#C44E52", lw=2,
             label="Maksimum hujan harian (mm)", zorder=3)
    ax2.set_ylabel("Maksimum hujan harian (mm)")
    ax2.set_ylim(0, max(xmax) * 1.3)
    ax2.yaxis.set_major_formatter(id_fmt(0))
    for x, v in zip(tahun, xmax):
        ax2.annotate(id_num(v, 0), (x, v), textcoords="offset points",
                     xytext=(0, 8), ha="center", fontsize=7.5, color="#C44E52",
                     bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.8))

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=8.5)
    ax1.set_title("Curah Hujan Tahunan dan Maksimum Harian, Stasiun BWSK Sungai Ambawang 2012-2025")
    save(fig, "gambar4-1.png")


# --------------------------------------------------------------- Grafik 4.2
def grafik_konsistensi():
    s_norm = VAL["kons"]["Sstar_norm"]
    q95 = VAL["kons"]["q95"]
    q99 = VAL["kons"]["q99"]
    n = len(s_norm)
    tahun = VAL["years"]

    kum = []
    s = 0.0
    for v in s_norm:
        s += v
        kum.append(s)
    ks = list(range(1, n + 1))
    env95 = [q95 * math.sqrt(k) for k in ks]
    env99 = [q99 * math.sqrt(k) for k in ks]

    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    ax.plot(tahun, kum, "o-", color="#4C72B0", lw=2, label="Deviasi kumulatif ternormalisasi")
    ax.plot(tahun, env99, "--", color="#C44E52",
            label=f"Batas kritis 99% (q = {id_num(q99, 3)})")
    ax.plot(tahun, [-v for v in env99], "--", color="#C44E52")
    ax.plot(tahun, env95, "--", color="#DD8452",
            label=f"Batas kritis 95% (q = {id_num(q95, 3)})")
    ax.plot(tahun, [-v for v in env95], "--", color="#DD8452")
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xlabel("Tahun")
    ax.set_ylabel(r"$\sum S^*/D_y$ kumulatif")
    ax.set_xticks(tahun)
    ax.tick_params(axis="x", rotation=45)
    ax.legend(loc="upper left", fontsize=8.5)
    ax.set_title("Uji Konsistensi Data Hujan (Double-Mass Kumulatif), Q = "
                 + id_num(VAL["kons"]["qsqrt"], 3) + " < q$_{95}$")
    save(fig, "gambar4-2.png")


# --------------------------------------------------------------- Grafik 4.3
def grafik_kurva_frekuensi():
    freq = VAL["freq"]
    T_vals = [int(t) for t in freq.keys()]
    warna = {"Normal": "#4C72B0", "Gumbel": "#DD8452", "LP3": "#55A868"}

    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    for dist in ("Normal", "Gumbel", "LP3"):
        xt = [freq[str(t)][dist] for t in T_vals]
        ax.plot(T_vals, xt, "o-", color=warna[dist], lw=2, label=f"Distribusi {dist}")

    # titik observasi: posisi plotting Weibull T = (n+1)/m
    xmax = sorted(VAL["xmax"], reverse=True)
    n = len(xmax)
    T_obs = [(n + 1) / (m + 1) for m in range(n)]
    ax.plot(T_obs, xmax, "k^", ms=6, label="Data observasi (Weibull)")

    r24 = VAL["R24"]
    ax.axhline(r24, color="gray", lw=0.9, ls=":")
    ax.plot([10], [r24], "*", color="#C44E52", ms=16, zorder=5,
            label=f"R$_{{24}}$ T = 10 tahun = {id_num(r24, 3)} mm")
    ax.annotate(f"{id_num(r24, 3)} mm", (10, r24), textcoords="offset points",
                xytext=(8, -12), fontsize=9, color="#C44E52")

    ax.set_xscale("log")
    ax.set_xticks(T_vals)
    ax.set_xticklabels([str(t) for t in T_vals])
    ax.set_xlabel("Kala ulang, T (tahun)")
    ax.set_ylabel("Curah hujan rencana 24 jam, X$_T$ (mm)")
    ax.set_ylim(0, 300)
    ax.yaxis.set_major_formatter(id_fmt(0))
    ax.legend(loc="upper left", fontsize=8.5)
    ax.set_title("Kurva Frekuensi Curah Hujan Maksimum Harian 24 Jam")
    save(fig, "gambar4-3.png")


# --------------------------------------------------------------- Grafik 4.4
def grafik_rippl():
    rows = list(DB.execute(
        "SELECT tahun, bulan, kumulatif_m3, defisit_m3 FROM neraca_bulanan "
        "WHERE fraksi = 0.65 ORDER BY tahun, bulan"))
    K = [r[2] for r in rows]
    Sp = [r[2] + r[3] for r in rows]
    idx = list(range(1, len(rows) + 1))

    kol = DES["kolam"]
    Vs, Va = kol["Vs"], kol["Va"]

    fig, ax = plt.subplots(figsize=(8.5, 4.4))
    ax.plot(idx, Sp, "-", color="#C44E52", lw=1.8, label="Kumulatif maksimum (Sp)")
    ax.plot(idx, K, "-", color="#4C72B0", lw=1.8,
            label="Kumulatif surplus/defisit (K), fraksi 65%")
    ax.fill_between(idx, K, Sp, color="#8172B3", alpha=0.25, label=f"Kebutuhan tampungan (Vs)")

    # penanda Vs (gap terbesar = Vs)
    i_max = max(range(len(rows)), key=lambda i: Sp[i] - K[i])
    ax.annotate("", xy=(i_max, K[i_max]), xytext=(i_max, Sp[i_max]),
                arrowprops=dict(arrowstyle="<->", color="#8172B3", lw=2))
    ax.annotate(f"Vs = {id_num(Vs, 1)} m$^3$", (i_max, (K[i_max] + Sp[i_max]) / 2),
                textcoords="offset points", xytext=(10, 0), fontsize=9,
                color="#8172B3", fontweight="bold")

    ax.axhline(K[0] + Va, color="#55A868", ls="--", lw=1.3,
               label=f"Va (atenuasi) = {id_num(Va, 1)} m$^3$")
    ax.annotate(f"V desain = Vs = {id_num(Vs, 1)} m$^3$", (0.03, 0.55),
                xycoords="axes fraction", fontsize=9, va="top",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.9))

    ax.set_xlabel("Bulan ke- (Jan 2012 - Agu 2025, n = 168)")
    ax.set_ylabel("Volume kumulatif (m$^3$)")
    ax.yaxis.set_major_formatter(id_fmt(0))
    ax.legend(loc="upper left", fontsize=8.5)
    ax.set_title("Kurva Massa Rippl Neraca Air Bulanan (fraksi kebutuhan 65%)")
    save(fig, "gambar4-4.png")


# --------------------------------------------------------------- Grafik 4.5
def grafik_neraca_bulanan():
    rows = list(DB.execute(
        "SELECT tahun, bulan, supply_m3, p_pond_m3, demand_m3, e_m3, kumulatif_m3 "
        "FROM neraca_bulanan WHERE fraksi = 0.65 ORDER BY tahun, bulan"))
    idx = list(range(1, len(rows) + 1))
    supply = [r[2] for r in rows]
    ppond = [r[3] for r in rows]
    demand = [r[4] for r in rows]
    evap = [r[5] for r in rows]
    kum = [r[6] for r in rows]

    fig, ax1 = plt.subplots(figsize=(9.5, 4.4))
    ax1.bar(idx, supply, width=0.8, color="#4C72B0", label="Limpasan atap (C.A.R)", zorder=2)
    ax1.bar(idx, ppond, width=0.8, bottom=supply, color="#937860",
            label="Hujan langsung kolam (P.Ap)", zorder=2)
    ax1.bar(idx, [-d for d in demand], width=0.8, color="#C44E52",
            label="Kebutuhan air (demand)", zorder=2)
    ax1.bar(idx, [-e for e in evap], width=0.8, bottom=[-d for d in demand],
            color="#DD8452", label="Evaporasi kolam (E.Ap)", zorder=2)
    ax1.axhline(0, color="k", lw=0.8)
    ax1.set_xlabel("Bulan ke- (Jan 2012 - Agu 2025)")
    ax1.set_ylabel("Neraca bulanan (m$^3$)")
    ax1.set_xlim(0, len(rows) + 1)
    ax1.yaxis.set_major_formatter(id_fmt(0))

    ax2 = ax1.twinx()
    ax2.grid(False)
    ax2.plot(idx, kum, "-", color="#55A868", lw=1.8, label="Kumulatif net (K)")
    ax2.set_ylabel("Kumulatif net (m$^3$)")
    ax2.yaxis.set_major_formatter(id_fmt(0))

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=8, ncol=2)
    ax1.set_title("Neraca Air Bulanan dan Kumulatif, Fraksi Kebutuhan 65%")
    save(fig, "gambar4-5.png")


# --------------------------------------------------------------- Grafik 4.6
def grafik_sensitivitas():
    ner = DES["neraca"]
    fraksi = sorted(float(f) for f in ner.keys())
    vs = [ner[f"{f:.2f}"]["vs"] for f in fraksi]
    rel = [ner[f"{f:.2f}"]["reliability"] for f in fraksi]

    va_s = DES["kolam"]["Va_sensitivitas"]
    th = sorted(float(t) for t in va_s.keys())
    va = [va_s[f"{t:g}"] if f"{t:g}" in va_s else va_s[str(t)] for t in th]

    it = DES["kolam"]["iterasi_konvergen"]
    langkah = [d["i"] for d in it]
    ap_in = [d["Ap_masuk"] for d in it]
    ap_out = [d["Ap_keluar"] for d in it]
    vs_it = [d["Vs"] for d in it]

    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.0))

    ax = axes[0]
    ax.plot([f * 100 for f in fraksi], vs, "o-", color="#4C72B0", lw=2)
    for f, v, r in zip(fraksi, vs, rel):
        ax.annotate(f"{id_num(v, 0)}\n({id_num(r, 1)}%)", (f * 100, v),
                    textcoords="offset points", xytext=(0, 8), ha="center",
                    fontsize=7.5)
    ax.set_xlabel("Fraksi kebutuhan terlayani (%)")
    ax.set_ylabel("Vs (m$^3$)")
    ax.set_title("(a) Vs vs fraksi kebutuhan")
    ax.yaxis.set_major_formatter(id_fmt(0))

    ax = axes[1]
    ax.plot(th, va, "s-", color="#C44E52", lw=2)
    for t, v in zip(th, va):
        ax.annotate(id_num(v, 0), (t, v), textcoords="offset points",
                    xytext=(0, 7), ha="center", fontsize=7.5)
    ax.set_xlabel("th (jam)")
    ax.set_ylabel("Va (m$^3$)")
    ax.set_title("(b) Va vs waktu konsentrasi th")
    ax.yaxis.set_major_formatter(id_fmt(0))

    ax = axes[2]
    ax.plot(langkah, ap_in, "o--", color="#4C72B0", lw=1.8, label="Ap masuk (m$^2$)")
    ax.plot(langkah, ap_out, "s-", color="#55A868", lw=1.8, label="Ap keluar (m$^2$)")
    ax2 = ax.twinx()
    ax2.grid(False)
    ax2.plot(langkah, vs_it, "^:", color="#8172B3", lw=1.5, label="Vs (m$^3$)")
    ax2.set_ylabel("Vs (m$^3$)")
    ax2.yaxis.set_major_formatter(id_fmt(0))
    ax.set_xlabel("Langkah iterasi")
    ax.set_ylabel("Luas muka kolam (m$^2$)")
    ax.set_title("(c) Iterasi konvergen Vs<->Ap")
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="lower right", fontsize=7.5)
    ax.yaxis.set_major_formatter(id_fmt(0))

    fig.suptitle("Analisis Sensitivitas Desain Kolam", y=1.02)
    save(fig, "gambar4-6.png")


# --------------------------------------------------------------- Grafik 4.7
def grafik_hidrolika():
    hid = DES["hidrolika"]
    it = hid["iterasi"]           # (v_masuk, td, tc, I, Q, Dteor, Dkom, v_keluar)
    Qs = [row[4] for row in it]
    qs = list(range(1, len(it) + 1))
    Q_des = hid["Q"]
    kap = hid["kapasitas"]

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.0), gridspec_kw={"width_ratios": [2, 1]})

    ax = axes[0]
    ax.plot(qs, Qs, "o-", color="#4C72B0", lw=2, label="Q per iterasi")
    ax.axhline(Q_des, color="#C44E52", ls="--", lw=1.5,
               label=f"Q desain (envelope) = {id_num(Q_des, 4)} m$^3$/dtk")
    ax.axhline(kap, color="#55A868", ls="-.", lw=1.5,
               label=f"Kapasitas DN900 (Manning penuh) = {id_num(kap, 4)} m$^3$/dtk")
    for x, q in zip(qs, Qs):
        ax.annotate(id_num(q, 3), (x, q), textcoords="offset points",
                    xytext=(0, 7), ha="center", fontsize=7.5)
    ax.set_xlabel("Langkah iterasi envelope (v-td-tc-I-Q-D)")
    ax.set_ylabel("Debit puncak, Q (m$^3$/dtk)")
    ax.set_xticks(qs)
    ax.set_ylim(0, kap * 1.25)
    ax.legend(fontsize=8)
    ax.set_title("(a) Osilasi iterasi hidrolika dan aturan envelope")

    ax = axes[1]
    labels = ["Q desain", "Kapasitas\nDN900"]
    vals = [Q_des, kap]
    bars = ax.bar(labels, vals, color=["#C44E52", "#55A868"], width=0.55)
    for b, v in zip(bars, vals):
        ax.annotate(id_num(v, 4), (b.get_x() + b.get_width() / 2, v),
                    textcoords="offset points", xytext=(0, 6), ha="center",
                    fontsize=8.5)
    ax.set_ylabel("Debit (m$^3$/dtk)")
    ax.set_ylim(0, kap * 1.25)
    ax.set_title(f"(b) Aman? v = {id_num(hid['v'], 3)} m/dtk")
    ax.yaxis.set_major_formatter(id_fmt(3))

    fig.suptitle("Hidrolika Pipa Penyalur Utama (DN900)", y=1.02)
    save(fig, "gambar4-7.png")


# --------------------------------------------------------------- Grafik 4.8
def grafik_evaporasi():
    rows = list(DB.execute("SELECT bulan, evap_mm, rn_mj, ea_pen_mm FROM evaporasi ORDER BY bulan"))
    b = [r[0] for r in rows]
    evap = [r[1] for r in rows]
    rn = [r[2] for r in rows]
    ea = [r[3] for r in rows]

    fig, ax1 = plt.subplots(figsize=(8.5, 4.2))
    bars = ax1.bar(b, evap, color="#4C72B0", width=0.6, label="Evaporasi (mm/bulan)")
    ax1.set_xlabel("Bulan")
    ax1.set_ylabel("Evaporasi (mm/bulan)")
    ax1.set_xticks(b)
    ax1.set_xticklabels(BULAN)
    ax1.set_ylim(0, max(evap) * 1.35)
    ax1.yaxis.set_major_formatter(id_fmt(0))
    for bar, v in zip(bars, evap):
        ax1.annotate(id_num(v, 1), (bar.get_x() + bar.get_width() / 2, v),
                     textcoords="offset points", xytext=(0, 4), ha="center",
                     fontsize=8)

    ax2 = ax1.twinx()
    ax2.grid(False)
    ax2.plot(b, rn, "o-", color="#C44E52", lw=1.8, label="Rn (MJ/m$^2$/hari)")
    ax2.plot(b, ea, "s-", color="#55A868", lw=1.8, label="Ea (mm/hari)")
    ax2.set_ylabel("Rn (MJ/m$^2$/hari) / Ea (mm/hari)")
    ax2.set_ylim(0, max(rn) * 1.5)

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=8.5)
    ax1.set_title("Evaporasi Muka Air Bulanan (Penman 1948) dan Komponen Iklimnya")
    save(fig, "gambar4-8.png")


if __name__ == "__main__":
    print("Membuat grafik Bab 4 ->", FIG.relative_to(ROOT))
    grafik_hujan_tahunan()
    grafik_konsistensi()
    grafik_kurva_frekuensi()
    grafik_rippl()
    grafik_neraca_bulanan()
    grafik_sensitivitas()
    grafik_hidrolika()
    grafik_evaporasi()
    print("Selesai:", len(list(FIG.glob("gambar4-*.png"))), "grafik.")
