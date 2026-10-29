# HANDOFF — Tesis Hidrologi Razi (Sistem Pemanenan Air Hujan Rajawali Residence)

Dokumen keadaan proyek untuk dilanjutkan sesi berikutnya. Jangan mulai dari nol —
baca bagian "Status" dan "Pekerjaan berikutnya" dulu.

> **⚠️ SESI 29 OKT 2026 (LANJUTAN, PAKET A SELESAI) — BACA BAGIAN INI DULU.**
> **Paket A sudah dieksekusi penuh**: evaporasi kini **Penman muka air + hujan langsung
> di kolam** (bukan ET0 120 mm/bulan), `Ap_kolam=1.200` dihapus, field lama
> `to/td/tc/I/Q` dibersihkan, chi-kuadrat diperbaiki (χ² ≈ 2,37). Pipeline penuh +
> `verifikasi_excel.py` **LULUS (6.807 cek, 0 gagal)**. Angka desain berubah:
> **Vs = 15.823,6 m³, kolam 72,5 × 73,0 × 3,0 m, reliability 65% = 100%**.
> Rincian keputusan di `REVISI.md`; data iklim NOAA ISD Supadio 2012–2025 ada di
> `data/raw/isd_supadio/` (di-ignore Git) — output Penman ter-commit di
> `data/processed/evaporasi_penman.csv/.json`.

## SESI 29 OKT 2026 (LANJUTAN) — EKSEKUSI PAKET A

### Apa yang sudah dilakukan

1. **`src/evaporasi_penman.py` (BARU):** evaporasi muka air terbuka metode
   **Penman (1948)** harian 2012–2025 dari **NOAA ISD Supadio** (T, titik embun→RH,
   angin 10 m→2 m, tekanan) + **NASA POWER CERES (Rs)**, agregasi bulanan →
   `data/processed/evaporasi_penman.csv` + `.json` (TER-COMMIT). Hasil:
   **142,3–166,2 mm/bulan** (rata-rata **154,3 mm/bulan**, total 1.851 mm/tahun) —
   konsisten dengan acuan sementara 149,4 mm/bulan (BPS 2024). Catatan: CSV ISD 2025
   hanya sampai **24 Agu 2025** (ketersediaan arsip NOAA).
2. **`build_db.py`:** tabel `evaporasi` kini berisi hitungan Penman (kolom
   `evap_mm`, `e0_mm_hari`, `t_c`, `rh_pct`, `u2_ms`, `rs_mj`); `Ap_kolam=1.200`
   **dihapus** dari `parameter_desain`; tabel `neraca_bulanan` punya kolom baru
   `p_pond_m3` (hujan langsung di kolam).
3. **`analisis_desain.py`:** neraca memakai **evaporasi Penman + hujan langsung
   `P × Ap`** sebagai pemasukan (keputusan 1); **iterasi konvergen Vs ↔ Ap**
   (5 langkah, titik tetap **Ap = 5.292,5 m²**) menggantikan pass-1/2/3 yang dulu
   divergen; basis neraca SEMUA fraksi = Ap titik tetap.
4. **`analisis2.py`:** chi-kuadrat bin **0,50/0,20/0,10/0,06/0,14 (jumlah 1,00)**
   → **χ² = 2,3673** (≈ 2,37) untuk ketiga distribusi, LP3 tetap terpilih; uji
   tambahan syarat **E ≥ 5** (kelas 2–5 digabung: O=[9,5], E=[7,7], χ²=1,143) ada
   di field `chi.*.e5`. Field lama `to/td/tc/I/Q/Vch/C/A_km2` (parameter Lo=200)
   **dihapus** dari `hasil_validasi.json` (keputusan 4) — bonus: bug bayangan
   `kons.Q` (statistik konsistensi tertimpa debit) ikut teratasi.
5. **Tool disinkronkan:** `buat_excel.py` (sheet Evaporasi baru + detail iklim,
   Neraca_Air 15 kolom dgn hujan kolam, Desain_Kolam B9 = hasil iterasi + blok
   catatan iterasi + cek **KONVERGEN live** di B42, Debit_Rencana jadi ringkasan
   tautan silang tanpa parameter lama, Koefisien p=0,14), `verifikasi_excel.py`,
   `buat_diagram.py`.
6. **Pipeline penuh dijalankan + recalc LibreOffice:** `verifikasi_excel.py`
   **LULUS 6.807 pemeriksaan, 0 gagal** (6.720 nilai deret neraca vs DB).

## SESI 29 OKT 2026 — AUDIT, LITERATUR, DAN KEPUTUSAN

### Apa yang sudah dilakukan

1. **Audit ulang pipeline Tahap 1–2** (baca kode + JSON + DB): statistik, uji
   homogenitas/konsistensi, frekuensi LP3 (R24 T=10 = 163,236 mm), hidrolika
   (Q = 0,8862 m³/dtk → DN900), Va = 3.190,4 m³, Vs = 15.148,4 m³, kolam
   71 × 71,5 × 3,0 m, reliability 65% = 99,4%.
2. **Audit data hilang:** 12 dari 5.114 hari (0,23%). Empat sel kosong + delapan
   sel bertanda “-” (legenda BWSK: “-” = Tidak Ada Data). Maret 2023 memuat 8 hari
   hilang; xmax 2023 = 100 mm pada 31 Maret (maksimum teramati).
3. **Literatur baru disalin ke repo:**
   - `manuscript/referensi/penman-1948-tabel6.md` — Tabel 6 Penman (1948), hlm. 137.
   - `manuscript/referensi/priestley-taylor-1972-lengkap-en.md` — teks lengkap 12 halaman.
   - `manuscript/referensi/priestley-taylor-1972-lengkap-id.md` — terjemahan lengkap.
   - `manuscript/referensi/priestley-taylor-1972-bagian6-en.md` dan `-id.md` — versi ringkas Bagian 6.
4. **Investigasi sumber data iklim (untuk Penman):**
   - **NOAA ISD Supadio** `96581099999` (USAF 965810, WBAN 99999, ICAO WIOO):
     CSV per tahun di `https://noaa-global-hourly-pds.s3.amazonaws.com/{tahun}/96581099999.csv`.
     Isi: TMP, DEW (→RH), WND, SLP, CIG/VIS, tutupan awan — 100% terisi.
     `AA1` (presipitasi) hanya 4,7%; **tidak ada sunshine** dan tidak ada evaporasi panci.
   - **SACAD BMKG** (`sacad.bmkg.go.id`): Supadio tercatat di file metadata
     (STAID 34) tetapi **tidak muncul di dropdown**; yang tersedia hanya
     **STASIUN METEOROLOGI MARITIM PONTIANAK** (STAID 100), dan untuk stasiun itu
     elemen yang tersedia **hanya Precipitation amount**. Jadi **tidak ada `ss`
     untuk Pontianak** di SACAD.
   - **BMKG Data Online** (`dataonline.bmkg.go.id`): memerlukan login; akses
     otomatis ditolak (403/timeout). Tidak dipakai.
   - **NASA POWER** (CERES + MERRA-2): berhasil diunduh 2012–2025 di koordinat
     tapak (−0,15 ; 109,45): `ALLSKY_SFC_SW_DWN` (Rs), `T2M`, `RH2M`, `WS2M`.
     5.114 hari, **0 nilai hilang**; Rs rata-rata 18,37 MJ/m²/hari.
     Disimpan di `data/raw/nasa_power/NASA_POWER_daily_2012-2025.csv` (di-ignore Git).
5. **Keputusan 1–16 dicatat** di `REVISI.md` (root repo), termasuk status
   “disetujui / menunggu eksekusi / dicatat”.

### Keputusan yang mengikat (ringkas)

| No | Keputusan |
|---|---|
| 1 | Evaporasi kolam = **metode Penman muka air**, plus **hujan langsung di permukaan kolam**. Tidak memakai istilah ET0/E0; tulis **“evaporasi”**. |
| 2 | `Ap_kolam = 1.200 m²` **dihapus** (placeholder tahap Va, bukan luas desain 5.076,5 m²). Belum dieksekusi. |
| 3 | Data harian kosong tetap **NULL**; tidak diisi M2 untuk sementara; asistensi dosen. Keputusan M2 di arsip Tahap 1b ditangguhkan. |
| 4 | Field lama `to/td/tc/I/Q` di `hasil_validasi.json` dihapus/ditandai; sheet `Debit_Rencana` dan diagram disinkronkan. Belum dieksekusi. |
| 5 | Uji chi-kuadrat memakai hitungan terakhir: bin 0,50/0,20/0,10/0,06/0,14 (jumlah 1) dan E ≥ 5; χ² ≈ 2,37; LP3 tetap terpilih. Belum dieksekusi. |
| 6 | Uji homogenitas: **2 arah, α = 5%** (t kritis 2,179) → t = 1,851 → **homogen**. Tulis eksplisit. |
| 7 | Pipa dianggap **kontinu** dulu; kemiringan tetap; atap → kolam **gravitasi**, kolam → warga **pompa** (dihitung nanti). |
| 8 | Dasar T = 10 mengikuti jurnal: Bangkinang, Sekuting, Gerilya Soedirman, Roy dkk. (2019). File ada di `data/raw/arsip-tesis-lengkap/05_Jurnal_dan_Referensi/Jurnal/`. |
| 9 | Supadio **tidak dipakai untuk hujan**; hari kosong tetap NULL. |
| 10 | Istilah “ET0/E0” tidak dipakai; gunakan **“evaporasi”**. |
| 11 | Sumber hujan: **BWSK 2012–2025 (14 tahun)**. |
| 12–16 | Bab IV/V angka baru, grafik Tahap 3, sinkron CAD, verifikasi lapangan, housekeeping — dicatat, belum dieksekusi. |

### Revisi Bab III yang WAJIB (catatan untuk penulisan naskah)

Bab III saat ini masih menyebut Supadio 2000–2024 + ERA5. Perlu diperbarui:

1. **Sumber hujan:** BWSK Sungai Ambawang 2012–2025 (14 tahun). Jelaskan alasan
   memilih 14 tahun: SNI 2415:2016 §4.2.1 menyarankan >20 tahun, tetapi pedoman
   PU Cipta Karya mensyaratkan minimum 10 tahun; data Supadio harian tidak tersedia
   di repo dan SACAD tidak menyediakan Supadio.
2. **Variabel iklim untuk evaporasi:** suhu, RH, angin, tekanan dari **NOAA ISD
   Supadio**; radiasi (Rs) dari **NASA POWER** (CERES). Tulis bahwa NASA POWER
   adalah produk satelit/reanalisis, bukan pengamatan stasiun, dan validasi
   terhadap pola musiman Supadio.
3. **Evaporasi:** metode **Penman muka air** (bukan ET0 rumput); masukkan **hujan
   langsung di permukaan kolam** (`P × Ap`) sebagai pemasukan. Hilangkan istilah
   ET0/E0 dari naskah; gunakan “evaporasi”.
4. **Data hilang:** 12 hari NULL, tidak diisi; sebut dasar SNI 2415:2016 §4.2.3
   (“data kosong tidak perlu dilakukan pengisian data”) dan WMO-168 §9.7.2
   (hindari pengisian sintetis). Sebut xmax 2023 sebagai **maksimum teramati**.
5. **Uji homogenitas:** tulis kriteria **2 arah, α = 5%**, t kritis 2,179.
6. **Chi-kuadrat:** tulis probabilitas bin yang menjumlah 1 dan syarat E ≥ 5.
7. **Kala ulang T = 10:** justifikasi dengan pedoman PU (Tabel 1: <10 ha → 2 tahun,
   jadi T = 10 konservatif), Tata Cara Kolam Retensi PU (pilih T berdasarkan risiko),
   jurnal Bangkinang/Sekuting/Roy, dan rumus risiko `r = 1 − (1 − 1/T)^n`
   (T = 10, n = 20 → 87,8%).
8. **Hidrolika pipa:** nyatakan pipa diperlakukan **kontinu** untuk sementara;
   kemiringan tetap; atap → kolam gravitasi; kolam → warga pompa (tahap V).
9. **Terminologi:** tidak memakai “ET0/E0”; cukup “evaporasi”.

### Direktori / file baru

```
REVISI.md                                      # keputusan 1–16 + status + blocker
manuscript/referensi/
├── penman-1948-tabel6.md                      # Tabel 6 Penman (1948)
├── priestley-taylor-1972-bagian6-en.md        # Bagian 6 (asli)
├── priestley-taylor-1972-bagian6-id.md        # Bagian 6 (terjemahan)
├── priestley-taylor-1972-lengkap-en.md        # teks lengkap 12 hlm (asli)
└── priestley-taylor-1972-lengkap-id.md        # teks lengkap (terjemahan)
data/raw/nasa_power/
└── NASA_POWER_daily_2012-2025.csv             # Rs, T2M, RH2M, WS2M (di-ignore Git)
```

Catatan: `manuscript/novelty.md` sudah ada dari **sesi lain (30 Okt 2026)** — bukan
hasil sesi ini. Jangan ditimpa tanpa membaca isinya.

### Yang belum dikerjakan — prioritas agen berikutnya

**Paket A (kode) — SELESAI sesi ini:** butir 1–5 (Penman + hujan kolam, hapus
`Ap_kolam`, bersihkan field lama, chi-kuadrat, pipeline + verifikasi) sudah
dieksekusi dan LULUS. Jangan dikerjakan ulang.

**Paket B (naskah & grafik) — BERIKUTNYA:**
6. Perbarui Bab IV/V dengan angka baru (jangan campur angka lama).
7. Buat `tools/buat_grafik.py` + 7 grafik `figures/gambar4-*.png`.

**Paket C (deliverable lain):**
8. Sinkronkan `sket_lengkap.dxf` (Ø800 → DN900; anotasi kolam lama).
9. Verifikasi lapangan (Lo, S_atap, S_pipa, he).
10. Housekeeping README/HANDOFF, hapus file temp.

### Blocker / pertanyaan yang harus dijawab dosen

1. **Sumber iklim untuk Penman:** rekomendasi sesi ini = **NOAA ISD Supadio +
   NASA POWER (Rs)**. Alternatif: ERA5 untuk semua variabel. NASA POWER/ERA5
   adalah produk reanalisis/satelit; ISD adalah pengamatan stasiun.
2. **Homogenitas:** 2 arah α = 5% (homogen) vs 1 arah (tidak homogen). Sudah
   dipilih 2 arah; pastikan dosen menyetujui.
3. **M2 dibatalkan?** Butir 3 menangguhkan pengisian M2 sampai asistensi. Selama
   itu neraca memakai deret NULL (Maret 2023 = 309 mm, bukan 413,9 mm).

### Jangan dilakukan

- Jangan mencampur angka lama (Supadio 25 th, Vs = 517 m³, kolam 814 m²) dengan
  angka pipeline baru.
- Jangan memakai SACAD untuk `ss` Pontianak — tidak tersedia.
- Jangan memakai hujan Supadio; sumber hujan tetap BWSK.
- Jangan mengubah DB/JSON terverifikasi tanpa menjalankan ulang pipeline penuh.

## Peta tahap (pembagian kerja sesuai kesepakatan)

**Restukturisasi (akhir Tahap 2):** repositori sudah ditata ulang ke struktur standar
riset Python/GitHub (`src/`, `tools/`, `data/{raw,sample,processed}`, `manuscript/`,
`figures/`, `notebooks/`), Git sudah di-init dengan `.gitignore` (data mentah ~1,2 GB
di-ignore; `manuscript/*.docx` dikecualikan agar ter-commit), `requirements.txt` dan
`README.md` (peta tahap resmi) tersedia di root. Path folder bernomor lama sudah
dihapus. Repo sudah dipush ke **https://github.com/razifaisal-design/tesis**
(private, branch `main`, remote `origin`).

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

### Angka desain terakhir (Paket A — Penman + hujan kolam; TERVERIFIKASI 6.807 cek)
- R24 (T=10 th, LP3) = 163,236 mm; to = 0,154 mnt; td = 3,25 mnt; tc = 0,0568 jam; I = 383,15 mm/jam
- Q desain (maks iterasi) = 0,8862 m3/dtk; D teoritis = 810 mm -> **DN900**;
  v = 1,393 m/dtk; kapasitas Manning penuh = 1,1718 m3/dtk (AMAN)
- Q per unit = 5,54 l/dtk -> pipa DN160; talang 0,15x0,10 m kapasitas 10,82 l/dtk; bak 0,5 m3
- Evaporasi Penman muka air = 142,3-166,2 mm/bulan (rata-rata 154,3 mm/bulan; NOAA ISD + NASA POWER)
- Iterasi Vs<->Ap **KONVERGEN** 5 langkah (Ap 1.072,5 -> 4.257,5 -> 5.041 -> 5.220 -> 5.292,5 m2)
- Va (th=1 jam) = 3.190,4 m3; Vs = 15.823,6 m3 -> **V desain = 15.823,6 m3**
  -> kolam 72,5 x 73,0 x 3,0 m (+freeboard 0,5 m = 3,5 m); Ap = 5.292,5 m2
- Reliability: f=1,00: 88,7% | 0,70: 98,8% | **0,65: 100%** | 0,60: 100% | 0,50: 100%

## Peta file (setelah restukturisasi akhir Tahap 2)

Struktur repo standar riset Python (detail di `README.md`):

- `src/` — komputasi inti: `evaporasi_penman.py` (NOAA ISD + NASA POWER ->
  evaporasi Penman bulanan), `build_db.py` (raw/sample -> DB), `analisis2.py` (statistik,
  uji, frekuensi, chi-kuadrat -> hasil_validasi.json), `analisis_desain.py`
  (-> hasil_desain.json + tabel hasil_desain/neraca_bulanan);
  `legacy/analisis_hujan.py` (sudah digantikan analisis2.py)
- `tools/` — `buat_excel.py` (workbook 14 sheet formula hidup), `buat_diagram.py`
  (-> figures/diagram-alur-hidrologi.html), `verifikasi_excel.py` (recalc + verifikasi
  silang, JALANKAN TERAKHIR), `recalc_excel.py` (bake cached values via LibreOffice),
  generator docx dari proyek lama
- `data/processed/` — SUMBER KEBENARAN: `hidrologi.db` + `hasil_validasi.json` +
  `hasil_desain.json` + `evaporasi_penman.csv/.json` +
  `Perhitungan_Hidrologi.xlsx` (semua ter-commit Git)
- `data/raw/` — data mentah & arsip ~1,2 GB (DI-IGNORE git; ada README di dalamnya):
  curah hujan BWSK, `isd_supadio/` (NOAA ISD 2012-2025), `nasa_power/` (NASA POWER Rs),
  `arsip-tesis-lengkap/`, PDF SNI/BSN, `tesis_extract/` (OMML)
- `data/sample/` — salinan data curah hujan (68 KB) -> pipeline jalan penuh di cloud
- `manuscript/` — naskah utama .docx/.pdf (proposal aktif, draft Bab 4 & Bab V,
  Proposal (7), tesis_text.txt) — WAJIB ter-commit, dikecualikan dari .gitignore
- `figures/` — output grafik (diagram alur + grafik Tahap 3: gambar4-*.png)
- `notebooks/` — eksplorasi Tahap 3+; `README.md` — peta tahap resmi + panduan run

Path lama sudah TIDAK dipakai: 01_Data, 02_Database, 03_Skrip_Analisis, 04_Hasil,
05_Dokumen (semua sudah dipindahkan ke struktur di atas).

## Perintah pipeline (urutan wajib, dari root repo)

```bash
python src/evaporasi_penman.py    # (hanya bila data iklim berubah) -> data/processed/evaporasi_penman.csv
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

1. ~~Evaporasi masih asumsi 120 mm/bulan~~ **SELESAI**: evaporasi kini Penman muka
   air 142,3-166,2 mm/bulan (src/evaporasi_penman.py; NOAA ISD Supadio + NASA POWER).
   Validasi silang dengan ERA5/panci evaporasi tetap bisa dibahas di Bab 4 (opsional).
2. ~~parameter_desain.Ap_kolam = 1200 m2~~ **SELESAI**: parameter dihapus (keputusan 2);
   Ap desain = 5.292,5 m2 dari iterasi (tabel hasil_desain), cek konvergensi live di
   Desain_Kolam B42.
3. **Asumsi lapangan WAJIB diverifikasi survei/waterpass**: Lo=8 m, S_atap=30%,
   S_pipa=0,30%, he=3 m (parameter_desain).
4. Selisih sumber data: proposal menyebut hujan Supadio 2000-2024 + ERA5 untuk
   bulanan/ET0; database memakai BWSK 2012-2025 — putuskan narasi & konsistensi di Bab 4
   (lihat revisi Bab III wajib di atas).
5. `alur-hidrologi-I-R-Q.html` = aset lama, belum dipakai tahap berjalan.
6. CSV NOAA ISD 2025 hanya sampai 24 Agu 2025 (arsip NOAA) — bila kelak arsip
   lengkap, jalankan ulang `src/evaporasi_penman.py` (dampak kecil pada klimatologi).

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
