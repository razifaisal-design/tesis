#!/usr/bin/env python3
"""Generator LAMPIRAN BAB IV (docx). Seluruh angka dari data/processed.

Lampiran A - Data hujan & pengendalian mutu
Lampiran B - Analisis frekuensi (parameter, faktor frekuensi, chi-kuadrat)
Lampiran C - Intensitas (IDF Mononobe) & debit rencana
Lampiran D - Hidrolika pipa (iterasi envelope, pipa standar)
Lampiran E - Neraca air bulanan 168 bulan (fraksi 65%)
Lampiran F - Rantai hitung evaporasi Penman
Lampiran G - Rekap hasil desain

Output: manuscript/LAMPIRAN_BAB_IV.docx
"""

import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from naskah_util import (ROOT, PROC, DB, setup_doc, para, heading, subheading,
                         caption_table, table, bullet, P, set_run,
                         n, ni, rup, VAL, DES, KOL, HID, UNIT, BULAN, BULAN3,
                         demand_tahun)

OUT = ROOT / "manuscript" / "LAMPIRAN_BAB_IV.docx"
doc = setup_doc()

TS = [2, 5, 10, 25, 50, 100]

# ================================================================== JUDUL
p = P(doc, align=1, before=0, after=4)
set_run(p.add_run("LAMPIRAN"), bold=True)
p = P(doc, align=1, after=14)
set_run(p.add_run("LAMPIRAN BAB IV \u2014 DATA DAN PERHITUNGAN PENDUKUNG"), bold=True)

para(doc,
     "Lampiran ini memuat data dan tabel perhitungan pendukung Bab IV. Seluruh angka "
     "dibangkitkan dari basis data terpadu (data/processed/hidrologi.db), "
     "hasil_validasi.json, dan hasil_desain.json, sehingga konsisten dengan naskah "
     "Bab IV dan dapat dihitung ulang.")

# ------------------------------------------------------------------ LAMPIRAN A
heading(doc, "Lampiran A", "Data Hujan dan Pengendalian Mutu")

caption_table(doc, "A.1", "Seri Hujan Harian Maksimum Tahunan Stasiun BWSK Sungai Ambawang 2012\u20132025")
rows = []
for i, y in enumerate(VAL["years"], 1):
    d = VAL["per_year"][str(y)]
    rows.append([ni(i), y, ni(d["total"]), ni(d["xmax"]), ni(d["hari_hujan"]),
                 ni(d["n_valid"]), ni(d["n_missing"])])
table(doc, ["No", "Tahun", "Total hujan (mm)", "R maks harian (mm)",
            "Hari hujan", "Hari valid", "Hari hilang"],
      rows, widths=[0.9, 1.4, 2.9, 2.9, 2.2, 2.2, 2.2],
      numerik={0, 1, 2, 3, 4, 5, 6})

caption_table(doc, "A.2", "Daftar Hari Tanpa Data (NULL) pada Seri 2012\u20132025")
rows = [[ni(i), y, ni(m), ni(d), "Dibiarkan kosong (NULL)"]
        for i, (y, m, d) in enumerate(VAL["missing"], 1)]
table(doc, ["No", "Tahun", "Bulan", "Tanggal", "Perlakuan"],
      rows, widths=[1.2, 2.5, 2.5, 2.5, 5.3], numerik={0, 1, 2, 3})

caption_table(doc, "A.3", "Hasil Uji Homogenitas (Uji-t) dan Konsistensi")
table(doc, ["Uji", "Parameter", "Nilai"],
      [["Homogenitas (Uji-t)", "t hitung", rup(VAL["t"]["t"], 3)],
       ["Homogenitas (Uji-t)", "t kritis (dua arah, \u03b1 = 5%; dk = 12)", "2,179"],
       ["Homogenitas (Uji-t)", "Kesimpulan", "Homogen"],
       ["Konsistensi", "Dy (mm)", rup(VAL["kons"]["Dy"], 3)],
       ["Konsistensi", "Q = maks |S*k|", rup(VAL["kons"]["Q"], 3)],
       ["Konsistensi", "Q/\u221an", rup(VAL["kons"]["qsqrt"], 3)],
       ["Konsistensi", "Nilai kritis 95% / 99%",
        n(VAL["kons"]["q95"], 3) + " / " + n(VAL["kons"]["q99"], 3)],
       ["Konsistensi", "Kesimpulan", "Konsisten"]],
      widths=[4.2, 6.3, 3.5])

# ------------------------------------------------------------------ LAMPIRAN B
heading(doc, "Lampiran B", "Analisis Frekuensi")

caption_table(doc, "B.1", "Parameter Statistik Seri Hujan (n = 14)")
table(doc, ["Parameter", "Data asli", "Data logaritmik"],
      [["Rata-rata", rup(VAL["xbar"], 3) + " mm", n(VAL["logXbar"], 4)],
       ["Standar deviasi (S)", rup(VAL["S"], 3) + " mm", n(VAL["Slog"], 4)],
       ["Koefisien variasi (Cv)", n(VAL["Cv"], 4), "-"],
       ["Koefisien kemencengan (Cs)", n(VAL["Cs"], 4), n(VAL["Cslog"], 4)],
       ["Koefisien kurtosis (Ck)", n(VAL["Ck"], 4), "-"]])

caption_table(doc, "B.2", "Faktor Frekuensi dan Hujan Rencana R24 (mm) Menurut Distribusi")
import math


def faktor(dist, t):
    if dist == "Normal":
        return statistics.NormalDist().inv_cdf(1 - 1 / t)
    if dist == "Gumbel":
        return -math.log(-math.log(1 - 1 / t))
    return VAL["freq"][str(t)]["K_lp3"]


rows = []
for lbl, key in (("Normal", "Normal"), ("Gumbel Tipe I", "Gumbel"),
                 ("Log Pearson III", "LP3")):
    rows.append([lbl + " \u2013 faktor"] + [n(faktor(key, t), 4) for t in TS])
    rows.append([lbl + " \u2013 R24 (mm)"] + [n(VAL["freq"][str(t)][key], 3) for t in TS])
table(doc, ["Distribusi / besaran"] + [f"T = {t}" for t in TS], rows,
      widths=[4.4] + [1.6] * len(TS), numerik=set(range(1, len(TS) + 1)))
para(doc,
     "Gumbel Tipe I: a = " + n(VAL["gumbel"]["a"], 4) + "; X\u2080 = "
     + rup(VAL["gumbel"]["Xo"], 3) + " mm. Faktor K Normal = z(T) dari sebaran "
     "normal baku; variabel Y Gumbel = \u2212ln(\u2212ln(1 \u2212 1/T)); K Log Pearson "
     "Tipe III diinterpolasi dari tabel pada Cs logaritmik.", after=8)

caption_table(doc, "B.3", "Rincian Uji Chi-Kuadrat per Distribusi")
rows = []
for dist, key in (("Normal", "Normal"), ("Gumbel Tipe I", "Gumbel"),
                  ("Log Pearson III", "LP3")):
    c = VAL["chi"][key]
    rows.append([dist, ", ".join(n(b, 3) for b in c["batas"]),
                 " ".join(ni(o) for o in c["O"]),
                 ", ".join(n(e, 2) for e in c["E"]),
                 n(c["chi2"], 4), ni(c["df"]), n(c["crit"], 3)])
table(doc, ["Distribusi", "Batas kelas (mm)", "O", "E", "\u03c7\u00b2", "dk",
            "\u03c7\u00b2 kritis"],
      rows, widths=[3.0, 4.0, 1.9, 3.2, 1.4, 0.9, 1.6],
      numerik={4, 5, 6}, size=9)
para(doc,
     "Uji tambahan syarat E \u2265 5 (kelas 2\u20135 digabung): O = [9; 5], "
     "E = [7,0; 7,0], \u03c7\u00b2 = " + n(VAL["chi"]["LP3"]["e5"]["chi2"], 3) + ".",
     after=8)

# ------------------------------------------------------------------ LAMPIRAN C
heading(doc, "Lampiran C", "Intensitas Hujan dan Debit Rencana")

durasi = [5, 10, 15, 20, 30, 45, 60, 90, 120, 180, 240, 360, 720, 1440]
caption_table(doc, "C.1", "Kurva Intensitas\u2013Durasi\u2013Frekuensi (IDF) Mononobe (mm/jam)")
rows = []
for dmin in durasi:
    tj = dmin / 60
    rows.append([ni(dmin)] + [n(VAL["freq"][str(t)]["LP3"] / 24 * (24 / tj) ** (2 / 3), 1)
                              for t in (2, 5, 10, 25)])
table(doc, ["Durasi (menit)", "T = 2", "T = 5", "T = 10", "T = 25"],
      rows, widths=[3.4, 2.6, 2.6, 2.6, 2.6], numerik={0, 1, 2, 3, 4})
para(doc, "Waktu konsentrasi tc = " + n(HID["tc"], 5) + " jam = "
     + rup(HID["tc"] * 60, 3) + " menit; I pada tc (T = 10) = " + rup(HID["I"], 2)
     + " mm/jam.", after=8)

caption_table(doc, "C.2", "Debit Puncak Limpasan Atap (Metode Rasional, C = 0,80; A = 0,0104 km\u00b2)")
rows = [["I pada tc (mm/jam)"] + [n(VAL["freq"][str(t)]["LP3"] / 24
                                   * (24 / HID["tc"]) ** (2 / 3), 2)
                                  for t in (2, 5, 10, 25)],
        ["Q (m\u00b3/detik)"] + [n(0.278 * 0.80 * VAL["freq"][str(t)]["LP3"] / 24
                                   * (24 / HID["tc"]) ** (2 / 3) * 0.0104, 4)
                                for t in (2, 5, 10, 25)]]
table(doc, ["Besaran"] + [f"T = {t}" for t in (2, 5, 10, 25)], rows,
      widths=[4.4] + [2.4] * 4, numerik={1, 2, 3, 4})

# ------------------------------------------------------------------ LAMPIRAN D
heading(doc, "Lampiran D", "Hidrolika Pipa Penyalur")

caption_table(doc, "D.1", "Iterasi Pemilihan Diameter Pipa (Aturan Envelope) \u2014 Rincian Penuh")
rows = []
for i, r in enumerate(HID["iterasi"], 1):
    rows.append([ni(i), n(r[0], 3), n(r[1], 3), n(r[2] * 60, 4), n(r[3], 2),
                 n(r[4], 4), ni(r[5] * 1000), ni(r[6]), n(r[7], 3)])
table(doc, ["Langkah", "v masuk (m/dtk)", "td (menit)", "tc (menit)", "I (mm/jam)",
            "Q (m\u00b3/dtk)", "D teoritis (mm)", "D komersial (mm)", "v keluar (m/dtk)"],
      rows, widths=[1.4, 1.8, 1.6, 1.7, 1.7, 1.7, 1.8, 1.8, 1.8],
      numerik=set(range(9)), size=8.5)

try:
    ps_cols = [d[1] for d in DB.execute("PRAGMA table_info(pipa_standar)")]
    ps_rows = [list(r) for r in DB.execute("SELECT * FROM pipa_standar")]
    caption_table(doc, "D.2", "Diameter Pipa Standar yang Ditinjau (tabel pipa_standar)")
    table(doc, ps_cols, [[("" if v is None else str(v)) for v in r] for r in ps_rows],
          size=9)
except Exception as e:  # pragma: no cover
    para(doc, "(Tabel pipa standar tidak tersedia: " + str(e) + ")")

# ------------------------------------------------------------------ LAMPIRAN E
heading(doc, "Lampiran E", "Neraca Air Bulanan 168 Bulan (Fraksi Kebutuhan 65%)")
para(doc,
     "Tabel berikut memuat neraca air bulanan penuh periode Januari 2012 sampai "
     "Desember 2025 (168 bulan) pada fraksi kebutuhan 65%. Kolom Vsupply = limpasan "
     "atap; P\u00b7Ap = hujan langsung di permukaan kolam; Vdemand = kebutuhan; "
     "E = evaporasi kolam; net = neraca bulanan; K = kumulatif net.")
rows = []
for r in DB.execute("SELECT tahun, bulan, supply_m3, p_pond_m3, demand_m3, e_m3, "
                    "net_m3, kumulatif_m3, defisit_m3, terpenuhi FROM neraca_bulanan "
                    "WHERE fraksi=0.65 ORDER BY tahun, bulan"):
    rows.append([f"{BULAN3[r['bulan'] - 1]} {r['tahun']}", ni(r["supply_m3"]),
                 ni(r["p_pond_m3"]), ni(r["demand_m3"]), ni(r["e_m3"]),
                 ni(r["net_m3"]), ni(r["kumulatif_m3"]), ni(r["defisit_m3"]),
                 "Ya" if r["terpenuhi"] else "Tidak"])
table(doc, ["Bulan", "Vsupply", "P\u00b7Ap", "Vdemand", "E", "Net", "K",
            "Defisit", "Terpenuhi"],
      rows, widths=[2.0, 1.7, 1.5, 1.7, 1.4, 1.5, 1.9, 1.6, 1.7],
      numerik={1, 2, 3, 4, 5, 6, 7}, size=8)

# ------------------------------------------------------------------ LAMPIRAN F
heading(doc, "Lampiran F", "Rantai Hitung Evaporasi Penman Bulanan")
para(doc,
     "Evaporasi muka air dihitung dengan metode Penman (1948) dari parameter iklim "
     "bulanan (NOAA ISD Supadio + radiasi NASA POWER). Seluruh kolom berikut identik "
     "dengan sheet Evaporasi pada berkas kerja dan tervalidasi silang terhadap basis "
     "data.")
rows = []
for e in DB.execute("SELECT * FROM evaporasi ORDER BY bulan"):
    rows.append([BULAN[e["bulan"] - 1], n(e["t_c"], 2), n(e["rh_pct"], 1),
                 n(e["u2_ms"], 3), n(e["rs_mj"], 2), n(e["rn_mj"], 2),
                 n(e["ea_pen_mm"], 3), n(e["e0_mm_hari"], 3), n(e["evap_mm"], 2),
                 ni(e["evap_mm"] / 1000 * KOL["Ap"])])
table(doc, ["Bulan", "T (\u00b0C)", "RH (%)", "u2 (m/dtk)", "Rs (MJ/m\u00b2)",
            "Rn (MJ/m\u00b2)", "Ea (mm/hari)", "E0 (mm/hari)", "Evap (mm/bln)",
            "Evap (m\u00b3/bln)"],
      rows, widths=[2.0, 1.4, 1.3, 1.5, 1.5, 1.5, 1.6, 1.6, 1.6, 1.9],
      numerik={1, 2, 3, 4, 5, 6, 7, 8, 9}, size=8.5)
tot = DB.execute("SELECT SUM(evap_mm) s, SUM(evap_mm) FROM evaporasi").fetchone()["s"]
para(doc, "Total evaporasi: " + rup(tot, 1) + " mm/tahun (setara "
     + ni(tot / 1000 * KOL["Ap"]) + " m\u00b3/tahun pada Ap = " + n(KOL["Ap"], 2)
     + " m\u00b2).", after=8)

# ------------------------------------------------------------------ LAMPIRAN G
heading(doc, "Lampiran G", "Rekapitulasi Hasil Desain (Tabel hasil_desain)")


def fmt_val(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return str(v)
    if f == int(f):
        return ni(f)
    return n(f, 3)


rows = []
skip = {"iterasi_konvergen", "Va_sensitivitas"}
for r in DB.execute("SELECT kunci, nilai, satuan, ket FROM hasil_desain ORDER BY rowid"):
    if r["kunci"] in skip:
        continue
    rows.append([r["kunci"], fmt_val(r["nilai"]), r["satuan"] or "-",
                 (r["ket"] or "").split("[")[0].strip()])
table(doc, ["Kunci", "Nilai", "Satuan", "Keterangan"], rows,
      widths=[4.2, 3.0, 1.8, 5.5], size=8.5)
para(doc,
     "Nilai rinci iterasi konvergensi Ap\u2194Vs disajikan pada Lampiran D/Tabel 4.18, "
     "dan sensitivitas Va terhadap th pada Tabel 4.17.", after=8)

doc.save(OUT)
print("Tersimpan:", OUT.relative_to(ROOT), f"({OUT.stat().st_size:,} bytes)")
