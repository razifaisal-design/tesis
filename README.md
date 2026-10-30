# Tesis — Analisis Sistem Pemanenan Air Hujan untuk Mitigasi Banjir di Kawasan Perumahan Rajawali Residence

**Razi Faisal (D2071241011)** — Magister Teknik Sipil, Universitas Tanjungpura Pontianak

Repositori komputasi tesis: seluruh analisis hidrologi, hidrolika perpipaan, neraca air,
dan desain kolam retensi dijalankan sebagai **pipeline Python yang dapat direproduksi**
dari data mentah → SQLite → JSON → workbook Excel berformula hidup → verifikasi silang
otomatis. Database SQLite adalah **satu-satunya sumber kebenaran**; setiap angka di
naskah harus ditarik dari hasil pipeline ini.

**Status saat ini: Bab IV Tahap 1–5 SELESAI (naskah Bab 4 + lampiran + grafik terbit) — sesi berikutnya = Tahap 6 (finishing PDF/CAD/keputusan lahan), lalu Bab V.**

---

## 1. Status & Peta Tahap Riset

Penulisan dan komputasi tesis terbagi dalam tahapan kerja terstruktur:

| Tahap | Bab | Isi | Status |
|---|---|---|---|
| 1 | IV | Fondasi & verifikasi rumus OMML + skema database | **SELESAI** |
| 2 | IV | Mesin desain (`analisis_desain.py`) + 5 sheet Excel baru + recalc + verifikasi | **SELESAI** |
| 3 | IV | Visualisasi hasil siap naskah (grafik Bab 4) | **SELESAI** (`figures/gambar4-1..8.png`, digarap bersama Tahap 5) |
| 4 | IV | Analisis sensitivitas + pembahasan + verifikasi asumsi lapangan | **SELESAI** (Subbab 4.9 & 4.10) |
| 5 | IV | Naskah Bab 4 final (docx) + lampiran | **SELESAI** (`manuscript/BAB_IV_HASIL_DAN_PEMBAHASAN.docx`, `LAMPIRAN_BAB_IV.docx`; Daftar Pustaka & Muka-muka oleh user) |
| 1 | V | Jaringan distribusi bertekanan + pompa | — |
| 2 | V | Ekonomi teknik: RAB, operasional, retribusi, BEP | — |
| 3 | V | TAHAP TEST — dashboard web lokal (pipeline + test suite) | — |

Catatan progres:

- **Tahap 1 selesai** — fondasi teoritis: seluruh rumus persamaan OMML proposal
  terverifikasi (termasuk koreksi typo Gumbel dan keputusan pipa = Manning *aliran
  penuh*), skema database fix (9 tabel).
- **Tahap 2 selesai** — mesin desain beroperasi penuh: neraca air 5 fraksi,
  hidrolika pipa induk (aturan *envelope* iterasi), pipa per unit + talang + bak,
  desain kolam kriteria ganda (Vs vs Va) beserta umpan balik evaporasi; workbook
  14 sheet berformula hidup terekalkulasi dan **terverifikasi 5.972 pemeriksaan, 0 gagal**.
- **Fokus berikutnya (Tahap 6 sesi)** — finishing: ekspor PDF naskah (LibreOffice),
  render ulang gambar CAD, analisis keputusan alokasi lahan kolam (Ap rencana vs
  lahan FASOS), housekeeping; rincian di [`HANDOFF_TAHAP_6.md`](HANDOFF_TAHAP_6.md).
  Setelah itu Bab V Tahap 1 (jaringan distribusi + pompa).

Detail handoff per sesi (dokumen keadaan, angka hasil, isu terbuka): lihat
[`HANDOFF.md`](HANDOFF.md).

---

## 2. Struktur Repositori

```text
repo-tesis/
├── .gitignore              # Filter data mentah ~1,2 GB, .venv, cache, file temp docx
├── requirements.txt        # Dependensi Python (auto-detect di Cloud/Codespaces)
├── README.md               # Dokumen ini: peta tahap riset + panduan run
├── HANDOFF.md              # Handoff antar-sesi (status detail, angka hasil, checklist)
├── manuscript/             # Naskah tesis (.docx) & draft penulisan — WAJIB ter-commit
│   ├── Proposal Tesis (claude) (Revisi Antigravity) 2.docx   ← naskah aktif
│   ├── Proposal Tesis (7).docx / (7).pdf                     ← versi revisi ke-7 (arsip FIX)
│   ├── bab 4 claude (Revisi Antigravity).docx                ← draft Bab 4 (bahan Tahap 5)
│   ├── BAB_V_KESIMPULAN_DAN_SARAN.docx                       ← draft Bab V
│   └── tesis_text.txt                                        ← ekstraksi teks proposal
├── src/                    # Kode komputasi inti
│   ├── build_db.py         # Bangun SQLite dari data mentah + parameter desain
│   ├── analisis2.py        # Statistik, uji homogenitas/konsistensi, frekuensi, chi-kuadrat
│   ├── analisis_desain.py  # Neraca air + hidrolika pipa + desain kolam (engine Tahap 2)
│   └── legacy/             # Skrip lama (analisis_hujan.py) — sudah digantikan
├── tools/                  # Skrip utilitas & output
│   ├── buat_excel.py       # Workbook Excel 14 sheet, formula hidup silang-sheet
│   ├── buat_diagram.py     # Diagram alur hidrologi (HTML/SVG)
│   ├── verifikasi_excel.py # Recalc (pustaka formulas) + verifikasi vs DB/JSON
│   ├── recalc_excel.py     # Recalc via LibreOffice headless (bake cached values)
│   └── buat_bab5_docx.py, revisi_dokumen_tesis_docx.py  # generator docx dari proyek lama
├── notebooks/              # Jupyter untuk analisis eksploratif (Tahap 3+)
├── figures/                # Output grafik/chart Bab IV/V (diagram alur, grafik Tahap 3)
└── data/
    ├── raw/                # Data mentah & arsip ~1,2 GB — DI-IGNORE Git (lihat README di dalamnya)
    ├── sample/             # Salinan data curah hujan (68 KB) agar pipeline jalan penuh di cloud
    └── processed/          # HASIL: hidrologi.db, hasil_validasi.json, hasil_desain.json,
                            #        Perhitungan_Hidrologi.xlsx (14 sheet, terverifikasi)
```

---

## 3. Persiapan Environment (lokal maupun Cloud/Codespaces)

```bash
# 1. Buat & aktifkan virtual environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2. Pasang dependensi
pip install -r requirements.txt
```

Catatan cloud: `data/raw/` tidak ikut ter-clone (di-ignore Git). `build_db.py`
otomatis memakai `data/sample/` sebagai fallback, jadi seluruh pipeline tetap
bisa dijalankan penuh di Codespaces/Runner. `data/processed/hidrologi.db` ikut
ter-commit sehingga analisis bisa langsung berjalan bahkan tanpa rebuild database.

---

## 4. Menjalankan Pipeline

Urutan wajib (dari root repositori):

```bash
python src/build_db.py          # 1. data mentah/sample -> data/processed/hidrologi.db
python src/analisis2.py         # 2. statistik, uji, frekuensi -> hasil_validasi.json
python src/analisis_desain.py   # 3. neraca air, hidrolika pipa, kolam -> hasil_desain.json + DB
python tools/buat_diagram.py    # 4. figures/diagram-alur-hidrologi.html
python tools/buat_excel.py      # 5. data/processed/Perhitungan_Hidrologi.xlsx (formula hidup)
python tools/verifikasi_excel.py# 6. recalc + verifikasi silang (WAJIB LULUS, exit code 0)
python tools/recalc_excel.py    # 7. (opsional) bake cached values via LibreOffice
```

Verifikasi terakhir (Tahap 2): **5.972 pemeriksaan, 0 gagal** — termasuk 5.880 sel
deret neraca air (5 fraksi × 168 bulan × 7 kolom) dibandingkan langsung ke tabel
`neraca_bulanan` di database. `tools/verifikasi_excel.py` keluar dengan kode 1 bila
ada nilai yang menyimpang — aman dipakai sebagai test suite otomatis (dasar
dashboard web lokal di Bab V Tahap 3).

### Hasil desain terkini (Tahap 2, terverifikasi)

| Besaran | Nilai | Keterangan |
|---|---|---|
| R24 (T=10 th, LP3) | 163,236 mm | uji chi-kuadrat: LP3 terpilih |
| Q desain (envelope) | 0,8862 m³/dtk | maksimum dari 12 iterasi v↔td↔tc↔I↔Q↔D |
| Pipa induk | DN900 | Manning aliran penuh; kapasitas 1,1718 m³/dtk (AMAN) |
| Va (th = 1 jam) | 3.190,4 m³ | kriteria atenuasi |
| Vs (fraksi 65%) | 15.148,4 m³ | kriteria penyimpanan (Rippl) — **penentu desain** |
| Kolam retensi | 71 × 71,5 × 3,0 m (+0,5 m freeboard) | kedap (lined), lahan gambut |
| Reliability fraksi 65% | 99,4% | 167 dari 168 bulan terpenuhi |

---

## 5. Kebijakan Data & Batas Ukuran Git

- **`data/raw/` DI-IGNORE** (~1,2 GB: arsip tesis lama, PDF referensi, foto survei).
  Hanya `README.md` di dalamnya yang ter-commit sebagai dokumentasi.
- **`manuscript/*.docx` DAN `manuscript/*.pdf` TIDAK boleh ter-ignore** — diberi
  aturan eksplisit `!manuscript/*.docx` di `.gitignore` agar naskah utama selalu
  ikut ter-upload.
- `data/sample/` (68 KB) + `data/processed/` (DB 380 KB + workbook 304 KB + JSON)
  ikut ter-commit agar pipeline dapat dijalankan ulang penuh di cloud.
- Target total repo < 100 MB; file tunggal > 50 MB jangan di-commit (pakai
  `data/raw/` lokal saja).
- File temporary Word (`~$*.docx`), `.DS_Store`, `.venv/`, `__pycache__/` di-ignore.

---

## 6. Konvensi Komputasi (wajib dipertahankan)

1. **SQLite = sumber kebenaran.** Semua output analisis (JSON, Excel, grafik)
   ditarik dari `data/processed/hidrologi.db` — jangan menghitung ulang rumus di
   tempat lain tanpa melalui pipeline.
2. **Excel = formula hidup.** Workbook memakai formula silang-sheet (tanpa nilai
   hardcode); input = biru + kuning, hasil = formula hitam. Audit angka kapan pun.
3. **Pipa = Manning aliran penuh** (bukan aliran terbuka); talang = aliran terbuka.
4. **Setiap asumsi terdokumentasi** di sel/komentar (Lo, S_pipa, he, ET0, dll.
   ditandai sebagai asumsi yang wajib diverifikasi lapangan).
5. **Verifikasi sebelum menyimpulkan.** Setelah mengubah input/rumus, jalankan
   ulang pipeline penuh + `tools/verifikasi_excel.py` sampai LULUS.
6. Pembagian kerja antar-sesi dan aturan kelanjutan ada di [`HANDOFF.md`](HANDOFF.md)
   (komunikasi & naskah dalam Bahasa Indonesia).

---

## 7. Peta Isu Terbuka

1. Evaporasi masih asumsi 120 mm/bulan (`data/processed` → tabel `evaporasi`) —
   rencana diganti data ERA5/BMKG pada Tahap 3/4.
2. `parameter_desain.Ap_kolam` (1.200 m²) sudah tidak konsisten dengan hasil desain
   (5.076,5 m²) — ditandai otomatis di sheet Desain_Kolam.
3. Asumsi lapangan (Lo = 8 m, S_atap = 30%, S_pipa = 0,30%, he = 3 m) wajib
   diverifikasi survei/waterpass (Tahap 4).
4. Sumber data hujan: pipeline baru memakai BWSK 2012–2025; draft lama memakai
   Supadio 2000–2024 — keputusan narasi diputuskan di Tahap 4–5 (perbedaan angka
   lama vs baru tercatat lengkap di `HANDOFF.md`).
