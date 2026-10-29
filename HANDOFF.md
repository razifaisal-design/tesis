# HANDOFF — Tesis Hidrologi Razi (Sistem Pemanenan Air Hujan Rajawali Residence)

Dokumen keadaan proyek untuk dilanjutkan sesi berikutnya. Jangan mulai dari nol —
baca bagian "Status" dan "Pekerjaan berikutnya" dulu.

## Peta tahap (pembagian kerja sesuai kesepakatan)

**Restukturisasi (akhir Tahap 2):** repositori sudah ditata ulang ke struktur standar
riset Python/GitHub (`src/`, `tools/`, `data/{raw,sample,processed}`, `manuscript/`,
`figures/`, `notebooks/`), Git sudah di-init dengan `.gitignore` (data mentah ~1,2 GB
di-ignore; `manuscript/*.docx` dikecualikan agar ter-commit), `requirements.txt` dan
`README.md` (peta tahap resmi) tersedia di root. Path folder bernomor lama sudah
dihapus.

| Tahap | Bab | Isi | Status |
|---|---|---|---|
| 1 | IV | Fondasi & verifikasi rumus OMML + skema database | SELESAI |
| 2 | IV | Mesin desain (analisis_desain.py) + 5 sheet Excel baru + recalc + verifikasi | SELESAI |
| 3 | IV | Visualisasi hasil siap naskah (grafik Bab 4) | BERIKUTNYA |
| 4 | IV | Analisis sensitivitas + pembahasan + verifikasi asumsi lapangan | — |
| 5 | IV | Naskah Bab 4 final (docx) + lampiran | — |
| 1 | V | Jaringan distribusi bertekanan + pompa | — |
| 2 | V | Ekonomi teknik: RAB, operasional, retribusi, BEP | — |
| 3 | V | TAHAP TEST — dashboard web lokal (pipeline + test suite) | — |

## Status per tahap

### Tahap 1 (sesi sebelum) — SELESAI
- Seluruh rumus tesis (OMML dari proposal) diverifikasi: koreksi typo Gumbel,
  konfirmasi pipa diperlakukan MAJOR flow penuh -> diputuskan: pipa = Manning
  ALIRAN PENUH (bukan aliran terbuka); talang tetap aliran terbuka.
- `02_Database/hidrologi.db` dibangun sebagai sumber kebenaran: curah_hujan_harian
  (5.114 baris, 12 hilang), curah_hujan_bulanan (168), kawasan (13), parameter_desain (8),
  evaporasi (12), pipa_standar (15), hasil_desain, neraca_bulanan, meta.

### Tahap 2 (sesi ini) — SELESAI
- `03_Skrip_Analisis/analisis_desain.py`: neraca air 5 fraksi (100/70/65/60/50%,
  desain 65%), hidrolika pipa induk dengan ATURAN ENVELOPE (iterasi v<->td<->tc<->I<->Q<->D
  12x, Q desain = maksimum iterasi konservatif, D dibulatkan ke atas ke pipa komersial),
  pipa per unit + talang + bak, desain kolam kriteria ganda (Va vs Vs) + pass-2/pass-3
  umpan balik evaporasi + sensitivitas th + reliability per fraksi.
- `03_Skrip_Analisis/buat_excel.py` ditulis ulang: `04_Hasil/Perhitungan_Hidrologi.xlsx`
  kini 14 sheet, semua formula Excel hidup silang-sheet (taste: tanpa nilai hardcode):
  ...Chi_Kuadrat, Debit_Rencana, **Kawasan, Evaporasi, Hidrolika_Pipa, Neraca_Air,
  Desain_Kolam**, Koefisien. Neraca_Air = 5 blok x 168 bulan; blok fraksi desain punya
  kolom O-X (pass-2 & pass-3).
- `03_Skrip_Analisis/verifikasi_excel.py` (BARU): recalc via pustaka `formulas` +
  bandingkan terhadap hasil_validasi.json, hasil_desain.json dan tabel neraca_bulanan.
  Hasil akhir: **5.972 pemeriksaan, 0 gagal** (5.880 sel deret neraca vs DB).
- File xlsx di-recalc dengan LibreOffice (cached values dibakar, formula tetap utuh),
  hasil recalc divalidasi ulang terhadap DB (lolos) lalu menggantikan file asli.

### Angka desain terakhir (tahap 2, envelope final)
- R24 (T=10 th, LP3) = 163,236 mm; to = 0,154 mnt; tc = 0,0576 jam; I = 383,15 mm/jam
- Q desain (maks iterasi) = 0,8862 m3/dtk; D teoritis = 810 mm -> **DN900**;
  v = 1,393 m/dtk; kapasitas Manning penuh = 1,1718 m3/dtk (AMAN)
- Q per unit = 5,49 l/dtk -> pipa DN160; talang 0,15x0,10 m kapasitas 10,82 l/dtk; bak 0,5 m3
- Va (th=1 jam) = 3.190,4 m3; Vs pass-1 = 15.148,4 m3 -> **V desain = 15.148,4 m3**
  -> kolam 71 x 71,5 x 3,0 m (+freeboard 0,5 m = 3,5 m); Ap hasil desain = 5.076,5 m2
- Umpan balik evaporasi: Vs pass-2 = 35.121; pass-3 = 139.673 m3 (divergen — dokumen Tesis)
- Reliability: f=1,00: 66,1% | 0,70: 98,2% | **0,65: 99,4%** | 0,60: 100% | 0,50: 100%

## Peta file (setelah restukturisasi akhir Tahap 2)

Struktur repo standar riset Python (detail di `README.md`):

- `src/` — komputasi inti: `build_db.py` (raw/sample -> DB), `analisis2.py` (statistik,
  uji, frekuensi, chi-kuadrat -> hasil_validasi.json), `analisis_desain.py`
  (-> hasil_desain.json + tabel hasil_desain/neraca_bulanan);
  `legacy/analisis_hujan.py` (sudah digantikan analisis2.py)
- `tools/` — `buat_excel.py` (workbook 14 sheet formula hidup), `buat_diagram.py`
  (-> figures/diagram-alur-hidrologi.html), `verifikasi_excel.py` (recalc + verifikasi
  silang, JALANKAN TERAKHIR), `recalc_excel.py` (bake cached values via LibreOffice),
  generator docx dari proyek lama
- `data/processed/` — SUMBER KEBENARAN: `hidrologi.db` + `hasil_validasi.json` +
  `hasil_desain.json` + `Perhitungan_Hidrologi.xlsx` (semua ter-commit Git)
- `data/raw/` — data mentah & arsip ~1,2 GB (DI-IGNORE git; ada README di dalamnya):
  curah hujan BWSK, `arsip-tesis-lengkap/`, PDF SNI/BSN, `tesis_extract/` (OMML)
- `data/sample/` — salinan data curah hujan (68 KB) -> pipeline jalan penuh di cloud
- `manuscript/` — naskah utama .docx/.pdf (proposal aktif, draft Bab 4 & Bab V,
  Proposal (7), tesis_text.txt) — WAJIB ter-commit, dikecualikan dari .gitignore
- `figures/` — output grafik (diagram alur + grafik Tahap 3: gambar4-*.png)
- `notebooks/` — eksplorasi Tahap 3+; `README.md` — peta tahap resmi + panduan run

Path lama sudah TIDAK dipakai: 01_Data, 02_Database, 03_Skrip_Analisis, 04_Hasil,
05_Dokumen (semua sudah dipindahkan ke struktur di atas).

## Perintah pipeline (urutan wajib, dari root repo)

```bash
python src/build_db.py            # raw -> data/processed/hidrologi.db (fallback: data/sample/)
python src/analisis2.py
python src/analisis_desain.py
python tools/buat_diagram.py
python tools/buat_excel.py
python tools/verifikasi_excel.py  # WAJIB LULUS (exit code 0)
python tools/recalc_excel.py      # opsional: bake cached values via LibreOffice
```

LibreOffice lokal: `/Volumes/Lexar/APPS/LibreOffice.app` (otomatis dipakai
`tools/recalc_excel.py`). Pustaka: pandas, numpy, openpyxl, formulas, matplotlib
(semua tercantum di `requirements.txt`). Git sudah di-init; `data/raw/` di-ignore,
`manuscript/*.docx` dikecualikan agar selalu ter-commit.

## Konvensi yang WAJIB dipertahankan (learned taste)

- SQLite = sumber kebenaran; semua keluaran analisis harus ditarik dari DB/JSON.
- Excel deliverable: formula HIDUP silang-sheet, tanpa nilai hardcode (input = biru
  + kuning, hasil = formula hitam).
- Pipa = Manning aliran penuh; talang = aliran terbuka. Setiap asumsi harus
  terdokumentasi di sel/komentar (jangan menyisipkan nilai tanpa keterangan).
- File kerja tetap di dalam folder projek (struktur repo src/tools/data/manuscript),
  jangan di scratchpad.
- Komunikasi & naskah dalam Bahasa Indonesia.
- Setelah sesi terputus/mulai baru: ringkas status 2 kalimat dulu, lanjutkan dari
  dokumen ini — JANGAN refactor/mulai ulang yang sudah terverifikasi.

## Bahan proyek lama: `data/raw/arsip-tesis-lengkap/` (di-ignore Git, lokal saja)

Arsip proyek tesis sebelumnya (1,2 GB, pindahan dari 05_Dokumen/Tesis_Lengkap) —
DASAR & BAHAN, bukan sumber kebenaran angka. Sumber kebenaran tetap pipeline DB di
`data/processed/hidrologi.db`. Naskah utamanya sudah disalin ke `manuscript/`.

- `00_FIX/` — Proposal Tesis (7).docx/.pdf (naskah acuan final versi lama)
- `02_Bab_dan_Revisi_Parsial/` — **`bab 4 claude (Revisi Antigravity).docx` (DRAFT BAB 4
  lama — bahan utama Bab 4 Tahap 5)**, `BAB_V_KESIMPULAN_DAN_SARAN.docx`, BAB 1-2 & 3,
  Metodologi/Tinjauan Pustaka revisi, `buat_bab5_docx.py` & `revisi_dokumen_tesis_docx.py`
  (generator docx — pola bisa dipakai ulang)
- `03_Desain_CAD_dan_Peta/` — sket.dwg/.bak, Drawing1.vsdx (diagram alur Visio),
  peta.mxd + peta.docx (ArcGIS), alir.jpg, konsep PAH tipe 36
- `04_Data_dan_Analisis/` — Siteplan.pdf/.jpg, `Data Curah Hujan/`, Standar_Kebutuhan_Air.xlsx,
  SNI 8135:2025, SNI 8153:2015, sni-03-7065-2005, Dokumentasi survei (30+ foto & video),
  **`Tahap_2_Neraca_Air_PAH/`** — analisis neraca air versi lama (docx+xlsx+py+grafik PDF)
- `05_Jurnal_dan_Referensi/` — Jurnal/ (40+ PDF), Ref/ (Tesis Edwin, Skripsi Purnama,
  Skripsi Lourdes, GSS Sambas Besar) + SE Dirjen Bina Marga 23/2021 & PBM 15/2021
- `06_Presentasi/` — slide deck seminar proposal; `07_Arsip_Asli/` — Tesis.zip (513 MB)

### PERBEDAAN KRITIS proyek lama vs pipeline baru (PAKAI YANG BARU untuk angka!)

| Aspek | Lama (Tesis_Lengkap) | Baru (pipeline ini, tervalidasi) |
|---|---|---|
| Data hujan | BMKG Supadio 2000-2024 (25 th) | BWSK Sungai Ambawang 2012-2025 (14 th) |
| Xbar / R24 (LP3, T=10) | 116,8 mm / **153,46 mm** | 111,29 mm / **163,236 mm** |
| Luas atap total | 8.640 m2 (160 x 54) | 10.400 m2 (160 x 65) |
| Q puncak | 1.172 m3/dtk (I=506,7 mm/j) | 0,8862 m3/dtk (I=383,15 mm/j) |
| Vs fraksi 65% | 517 m3 | **15.148,4 m3** |
| Va (th=1 jam) | 4.219 m3 | 3.190,4 m3 |
| Penentu V desain | Va (4.219) | **Vs (15.148,4) — berubah dominan!** |
| Kolam | 65 x 32,5 x 2,0 m | 71 x 71,5 x 3,0 m (+0,5 freeboard) |
| n / S pipa | 0,009 (PVC) / 0,002 | 0,011 (Tabel 2.8) / 0,003 |
| Reliability 65% | 99,7% | 99,4% |

Konsekuensi:
1. Narasi/draft Bab 4 lama (`bab 4 claude...docx`) memakai angka lama — saat Bab 4
   Tahap 5, jadikan struktur/kalimatnya sebagai kerangka, tapi ANGKA ganti dari
   workbook/DB. Jangan mencampur angka lama & baru dalam satu tabel.
2. Keputusan sumber data (Supadio 25 th vs BWSK 14 th) harus dipilih &
   dipertanggungjawabkan di Bab 4 Tahap 4-5 (lihat flag isu terbuka #4).
3. Hasil lama menunjukkan Va >> Vs; hasil baru Vs >> Va — implikasi pembahasan
   "kolam ganda ditentukan fungsi mana" berubah total, bahas di Bab 4 Tahap 4.
4. Siteplan, foto survei, jurnal & tesis rujukan di sini dipakai langsung untuk
   Bab 4 Tahap 4 (verifikasi asumsi) dan Bab 5 (jaringan distribusi & BEP).

## Flag / isu terbuka

1. **Evaporasi masih asumsi 120 mm/bulan** (tabel evaporasi, ditandai kuning) —
   ganti dengan data ERA5/BMKG (Tesis 3.3.2) saat tersedia; jalankan ulang pipeline.
2. **parameter_desain.Ap_kolam = 1200 m2** sudah tidak konsisten dengan hasil desain
   5.076,5 m2 — sheet Desain_Kolam menandai "UPDATE parameter_desain.Ap_kolam".
   Nilai itu tidak dipakai hitungan (hanya cek konsistensi), perbaiki saat naskah Bab 4/5.
3. **Asumsi lapangan WAJIB diverifikasi survei/waterpass**: Lo=8 m, S_atap=30%,
   S_pipa=0,30%, he=3 m (parameter_desain).
4. Selisih sumber data: proposal menyebut hujan Supadio 2000-2024 + ERA5 untuk
   bulanan/ET0; database memakai BWSK 2012-2025 — putuskan narasi & konsistensi di Bab 4.
5. `alur-hidrologi-I-R-Q.html` = aset lama, belum dipakai tahap berjalan.

## Pekerjaan berikutnya: BAB 4 TAHAP 3 — Visualisasi hasil siap naskah

Tujuan: grafik + tabel siap tempel untuk Bab IV, angka 100% ditarik dari
`hasil_validasi.json`, `hasil_desain.json`, dan tabel `neraca_bulanan`/`hasil_desain`
di DB (semua sudah tervalidasi tahap 2).

Daftar grafik yang dibuat (usulan, boleh disesuaikan):
1. Curah hujan tahunan (total) + X maks harian per tahun — dari statistik/DB.
2. Uji konsistensi: S**k/Dy kumulatif + garis kritik 95% & 99% (Tabel 2.3 interpolasi).
3. Kurva frekuensi XT: Normal, Gumbel, LP3 + titik observasi + penanda R24 T=10 th.
4. Kurva massa Rippl: K kumulatif fraksi desain (65%) + penanda Vs, Va, dan V desain;
   opsional overlay 5 fraksi.
5. Neraca bulanan fraksi desain: supply vs (demand + evaporasi) per bulan + garis kumulatif.
6. Sensitivitas: (a) Vs vs fraksi kebutuhan; (b) Va vs th (0,5-3 jam);
   (c) Vs pass-1/pass-2/pass-3 (umpan balik evaporasi).
7. Hidrolika pipa: Q per iterasi (menunjukkan osilasi + envelope) + Q desain vs
   kapasitas DN900.

Checklist tahap 3:
- [ ] Buat `tools/buat_grafik.py` (baca DB/JSON, jangan hitung ulang rumus)
- [ ] Output PNG dpi 300 (+ SVG opsional) ke `figures/`, penomoran mengikuti
      urutan Bab 4 (mis. gambar4-1.png ...)
- [ ] Semua angka pada grafik identik dengan json/DB (sudah tervalidasi)
- [ ] Legenda/label Bahasa Indonesia, satuan lengkap, konsisten dgn sheet Excel
- [ ] (Jika data ERA5 sudah ada) tambah skenario evaporasi nyata + bandingkan
- [ ] Jalankan ulang pipeline + `verifikasi_excel.py` untuk pastikan tidak ada regresi
- [ ] Perbarui tabel status di dokumen HANDOFF.md ini

## Panduan memulai sesi baru

1. Baca HANDOFF.md ini + `README.md` + `data/processed/hasil_desain.json`.
2. Beri user ringkasan 2 kalimat (status: tahap 1 & 2 Bab IV selesai, lanjut tahap 3).
3. Kerjakan checklist tahap 3 di atas; semua perubahan skrip di `src/`/`tools/`,
   hasil di `data/processed/` & `figures/`, jangan ubah DB/JSON yang sudah
   tervalidasi kecuali memang ada perubahan input (lalu pipeline ulang penuh).
