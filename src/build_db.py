# -*- coding: utf-8 -*-
"""Bangun SQLite data/processed/hidrologi.db sebagai sumber kebenaran semua analisis.
Isi: data mentah curah hujan harian + turunannya (bulanan), parameter kawasan/site,
evaporasi muka air Penman (src/evaporasi_penman.py), tabel pipa standar, dan
parameter desain (sesuai Proposal Tesis)."""
import math
import csv
import calendar
import sqlite3
import datetime
import pandas as pd

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "processed" / "hidrologi.db"
NAMA_RAW = "Curah_Hujan_Sungai_Ambawang_BWSK_2012-2025.xlsx"
SRC = ROOT / "data" / "raw" / NAMA_RAW
if not SRC.exists():     # fallback environment cloud: data/raw di-ignore git -> pakai sample
    SRC = ROOT / "data" / "sample" / NAMA_RAW
if len(sys.argv) > 1:    # override manual: python src/build_db.py <path_xlsx>
    SRC = Path(sys.argv[1])

# ---------- 1. curah hujan harian dari data mentah ----------
xl = pd.ExcelFile(SRC)
rows = []
for ys in xl.sheet_names:
    y = int(ys)
    df = pd.read_excel(SRC, sheet_name=ys, header=None)
    hdr = None
    for r in range(df.shape[0]):
        v0, v1 = df.iat[r, 0], df.iat[r, 1]
        if isinstance(v0, str) and v0.strip().upper() == 'TANGGAL' and isinstance(v1, str) and v1.strip()[:3].lower() == 'jan':
            hdr = r
            break
    assert hdr is not None, f"header tidak ditemukan di sheet {ys}"
    for b in range(1, 13):
        for d in range(1, calendar.monthrange(y, b)[1] + 1):
            val = df.iat[hdr + d, b]
            mm = None
            if isinstance(val, (int, float)) and not (isinstance(val, float) and math.isnan(val)):
                mm = float(val)
            rows.append((datetime.date(y, b, d).isoformat(), y, b, d, mm))

# ---------- 2. curah hujan bulanan (diturunkan dari harian) ----------
bulan_rows = []
for y in sorted({r[1] for r in rows}):
    for b in range(1, 13):
        vals = [r[4] for r in rows if r[1] == y and r[2] == b and r[4] is not None]
        n_days = sum(1 for r in rows if r[1] == y and r[2] == b)
        if n_days:
            bulan_rows.append((y, b, round(sum(vals), 1), n_days))

# ---------- 3. parameter kawasan (sumber: Proposal Tesis + siteplan 1:1500) ----------
kawasan_rows = [
    ("nama_kawasan", "Rajawali Residence", "-", "Tesis 1.1/3.2"),
    ("lokasi", "Jl. Wonodadi 2, Kec. Sungai Raya, Kab. Kubu Raya", "-", "Tesis 3.2"),
    ("luas_kawasan", 28800.0, "m2", "Tesis 1.1 (2,88 ha); siteplan 330,40 x 85,78 m"),
    ("jumlah_unit", 160.0, "unit", "Tesis 1.1/3.2 (Tipe 36)"),
    ("jiwa_per_unit", 4.0, "jiwa", "Tesis 1.1"),
    ("luas_atap_per_unit", 65.0, "m2", "Tesis 1.1"),
    ("luas_atap_total", 10400.0, "m2", "Tesis 1.1 (36,1% luas kawasan)"),
    ("q_kebutuhan_air", 120.0, "liter/jiwa/hari", "SNI 03-7065-2005 (Tabel 2.1)"),
    ("C_atap", 0.80, "-", "Tabel 2.7 (atap logam/seng, rentang 0,70-0,90)"),
    ("fraksi_desain", 0.65, "-", "Tesis 3.4.1 (titik tengah 60-70% kebutuhan non-potabel)"),
    ("fraksi_diuji", "1.00; 0.70; 0.65; 0.60; 0.50", "-", "Tesis 3.4.1"),
    ("freeboard", 0.50, "m", "Tesis 2.7 (Putra dkk., 2023)"),
    ("th_durasi_efektif", 1.0, "jam", "Tesis 3.4.3 (sensitivitas 0,5-3 jam)"),
]

# ---------- 4. parameter desain hidrolika (siteplan + asumsi terdokumentasi) ----------
parameter_rows = [
    ("Lo", 8.0, "m", "Panjang aliran permukaan ATAP titik terjauh (Tipe 36, atap 65 m2). Asumsi tipologi - WAJIB diverifikasi survei (Tesis 3.3.1)"),
    ("S_atap", 0.30, "m/m", "Kemiringan atap (asumsi 30%) - masuk Kirpich utk to"),
    ("Ld", 330.0, "m", "Panjang pipa penyalur: unit terjauh ujung timur ke kolam rencana ujung barat laut (siteplan 1:1500, bentang 330,40 m)"),
    ("S_pipa", 0.003, "m/m", "Kemiringan pipa 0,30% (asumsi topografi datar - WAJIB diverifikasi waterpass)"),
    ("n_pipa", 0.011, "-", "Manning pipa (Tabel 2.8)"),
    ("he_kolam", 3.00, "m", "Kedalaman efektif kolam (asumsi desain)"),
    ("distribusi", "Bab V (jaringan tekan + pompa)", "-", "Perancangan jaringan distribusi dilakukan tahap teknis (Tesis 3.4.4)"),
]

# ---------- 5. evaporasi bulanan (Penman muka air, src/evaporasi_penman.py) ----------
# kolom = seluruh rantai hitung Penman (utk validasi silang sheet Evaporasi)
EVAP_CSV = ROOT / "data" / "processed" / "evaporasi_penman.csv"
assert EVAP_CSV.exists(), f"{EVAP_CSV} tidak ada - jalankan python3 src/evaporasi_penman.py"
with open(EVAP_CSV) as fh:
    rdr = csv.DictReader(fh)
    EVAP_COLS = [k for k in rdr.fieldnames if k != "keterangan"]
    evap_rows = []
    for row in rdr:
        vals = [int(row[k]) if k in ("bulan", "n_hari", "j_hari", "n_obs") else float(row[k])
                for k in EVAP_COLS]
        evap_rows.append(tuple(vals) + (row["keterangan"],))

# ---------- 6. tabel pipa standar ----------
pipa_rows = [
    (1, '4" (DN110)', 110.0), (2, '6" (DN160)', 160.0), (3, '8" (DN200)', 200.0),
    (4, '10" (DN250)', 250.0), (5, '12" (DN315)', 315.0), (6, '14" (DN355)', 355.0),
    (7, '16" (DN400)', 400.0), (8, '18" (DN450)', 450.0), (9, '20" (DN500)', 500.0),
    (10, '24" (DN600)', 600.0), (11, '30" (DN750)', 750.0), (12, '32" (DN800)', 800.0),
    (13, '36" (DN900)', 900.0), (14, '40" (DN1000)', 1000.0), (15, '48" (DN1200)', 1200.0),
]

con = sqlite3.connect(DB)
con.executescript("""
DROP TABLE IF EXISTS curah_hujan_harian;
DROP TABLE IF EXISTS curah_hujan_bulanan;
DROP TABLE IF EXISTS kawasan;
DROP TABLE IF EXISTS parameter_desain;
DROP TABLE IF EXISTS evaporasi;
DROP TABLE IF EXISTS pipa_standar;
DROP TABLE IF EXISTS hasil_desain;
DROP TABLE IF EXISTS neraca_bulanan;
DROP TABLE IF EXISTS meta;
CREATE TABLE curah_hujan_harian (
    tanggal TEXT PRIMARY KEY, tahun INTEGER NOT NULL, bulan INTEGER NOT NULL,
    tgl INTEGER NOT NULL, mm REAL);
CREATE TABLE curah_hujan_bulanan (
    tahun INTEGER NOT NULL, bulan INTEGER NOT NULL, mm REAL, n_hari INTEGER,
    PRIMARY KEY (tahun, bulan));
CREATE TABLE kawasan (kunci TEXT PRIMARY KEY, nilai TEXT, satuan TEXT, sumber TEXT);
CREATE TABLE parameter_desain (kunci TEXT PRIMARY KEY, nilai TEXT, satuan TEXT, keterangan TEXT);
CREATE TABLE pipa_standar (urut INTEGER PRIMARY KEY, label TEXT, d_mm REAL, luas_m2 REAL);
CREATE TABLE hasil_desain (kunci TEXT PRIMARY KEY, nilai TEXT, satuan TEXT, ket TEXT);
CREATE TABLE neraca_bulanan (
    tahun INTEGER, bulan INTEGER, fraksi REAL, supply_m3 REAL, p_pond_m3 REAL, demand_m3 REAL,
    e_m3 REAL, net_m3 REAL, kumulatif_m3 REAL, defisit_m3 REAL, terpenuhi INTEGER,
    PRIMARY KEY (tahun, bulan, fraksi));
CREATE TABLE meta (kunci TEXT PRIMARY KEY, nilai TEXT);
""")
EVAP_INT = {"n_hari", "j_hari", "n_obs"}
con.execute("CREATE TABLE evaporasi (%s, keterangan TEXT)" % ", ".join(
    f"{c} INTEGER PRIMARY KEY" if c == "bulan" else
    f"{c} INTEGER" if c in EVAP_INT else
    f"{c} REAL" for c in EVAP_COLS))
con.executemany("INSERT INTO curah_hujan_harian VALUES (?,?,?,?,?)", rows)
con.executemany("INSERT INTO curah_hujan_bulanan VALUES (?,?,?,?)", bulan_rows)
con.executemany("INSERT INTO kawasan VALUES (?,?,?,?)", kawasan_rows)
con.executemany("INSERT INTO parameter_desain VALUES (?,?,?,?)", parameter_rows)
con.executemany("INSERT INTO evaporasi VALUES (%s)" % ",".join("?" * (len(EVAP_COLS) + 1)),
                evap_rows)
con.executemany("INSERT INTO pipa_standar VALUES (?,?,?,?)",
                [(u, lab, d, round(math.pi * (d / 1000) ** 2 / 4, 6)) for u, lab, d in pipa_rows])
con.executemany("INSERT INTO meta VALUES (?,?)", [
    ("sumber_harian", str(SRC.relative_to(ROOT)) if SRC.is_relative_to(ROOT) else str(SRC)),
    ("dibuat", datetime.datetime.now().isoformat(timespec="seconds")),
    ("jumlah_hari", str(len(rows))),
    ("jumlah_hilang", str(sum(1 for r in rows if r[4] is None))),
    ("sumber_evaporasi", "Penman (1948) muka air - NOAA ISD Supadio + NASA POWER (src/evaporasi_penman.py)"),
])
con.commit()
con.close()
print(f"[ok] {DB}")
print(f"     harian: {len(rows)} baris ({sum(1 for r in rows if r[4] is None)} hilang)")
print(f"     bulanan: {len(bulan_rows)} baris | kawasan: {len(kawasan_rows)} | parameter: {len(parameter_rows)}")
print(f"     evaporasi: {len(evap_rows)} | pipa standar: {len(pipa_rows)}")
