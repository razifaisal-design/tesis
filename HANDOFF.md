# HANDOFF — Tesis Hidrologi Razi (Sistem Pemanenan Air Hujan Rajawali Residence)

Dokumen keadaan proyek untuk dilanjutkan sesi berikutnya. Jangan mulai dari nol —
baca bagian "Status" dan "Pekerjaan berikutnya" dulu.

> **⚠️ SESI 29 OKT 2026 (LANJUTAN, PAKET A SELESAI + TRANSPARANSI EVAPORASI) — BACA DULU.**
> **Paket A selesai** (Penman muka air + hujan langsung kolam; `Ap_kolam=1.200` dihapus;
> field lama `to/td/tc/I/Q` dibersihkan; chi-kuadrat diperbaiki χ² ≈ 2,37) dan **seluruh
> rantai hitung evaporasi kini tampil LIVE di workbook** — sheet `Iklim_Harian`
> (data mentah harian) + sheet `Evaporasi` (SEMUA langkah kali/bagi Penman sebagai
> kolom formula, bisa diaudit dosen). Pipeline penuh + `verifikasi_excel.py`
> **LULUS (7.152 cek, 0 gagal)** termasuk 342 cek rantai Penman. Angka desain final:
> **Vs = 15.751,7 m³, kolam 72,5 × 72,5 × 3,0 m, reliability 65% = 99,4%**.
> Data iklim NOAA ISD Supadio 2012–2025 di `data/raw/isd_supadio/` (di-ignore Git);
> output ter-commit: `data/processed/iklim_harian.csv` + `evaporasi_penman.csv/.json`.
> **Pekerjaan berikutnya = TAHAP 5** (lihat bagian bawah).

## SESI 29–30 OKT 2026 (LANJUTAN-3) — TAHAP 5: NASKAH BAB 4 (docx)

Melanjutkan sesi `5007b4ae` yang berhenti tepat setelah grafik Tahap 3 selesai.

1. **`tools/buat_grafik.py` + `figures/gambar4-1..8.png`** sudah ada dari sesi
   sebelumnya (Tahap 3 = 8 grafik, dpi 300) — TIDAK diubah, kini ikut ter-commit.
2. **`tools/buat_bab4_docx.py` (BARU):** generator naskah **BAB IV HASIL DAN
   PEMBAHASAN**. Seluruh angka dibaca dari sumber kebenaran (`hasil_validasi.json`,
   `hasil_desain.json`, tabel `kawasan`/`evaporasi`/`neraca_bulanan`/
   `curah_hujan_bulanan` di DB) — tidak ada nilai hardcode dan **tidak ada angka
   lama** (Supadio 25 th / Vs 517 m³ / kolam 814 m²) yang tercampur.
3. **Naskah keluaran:** `manuscript/BAB_IV_HASIL_DAN_PEMBAHASAN.docx` (20 tabel,
   8 gambar). Struktur mengikuti usulan TEMUAN GLM-5.3 §6: 4.1 karakteristik
   kawasan · 4.2 data hujan (uji-t, konsistensi) · 4.3 frekuensi & R24 (3 dist,
   χ², LP3) · 4.4 tc & IDF Mononobe · 4.5 debit puncak Rasional · 4.6 hidrolika pipa
   · 4.7 kebutuhan & neraca air + evaporasi (Rippl → Vs, keandalan) · 4.8 Va &
   Vdesain = maks(Vs, Va) · 4.9 sensitivitas · 4.10 pembahasan · 4.11 rekap + keterbatasan.
4. **Kepatuhan format Pedoman Untan (Okt 2017):** margin kiri 4 cm (termasuk
   1 cm penjilidan), atas/kanan/bawah 3 cm; TNR 12 pt; spasi 1,5; justify; judul
   tabel di ATAS, sumber ditulis pada kalimat yang merujuk; keterangan gambar di
   BAWAH (huruf pertama kapital).
5. **Kepatuhan TEMUAN GLM-5.3:** tanpa blok "[REVISI …]"; istilah hanya
   "evaporasi" (bukan ET0/E0); chi-kuadrat bin menjumlah 1 (0,50/0,20/0,10/0,06/0,14)
   + syarat E ≥ 5; satu tabel satu angka; pipa diperlakukan kontinu.
6. **Angka desain pada naskah (terverifikasi vs DB/JSON):** R24 T=10 = 163,236 mm
   (LP3) · I = 383,15 mm/jam · Q = 0,8862 m³/dtk → DN900 (v = 1,393 m/dtk, kapasitas
   1,1718 m³/dtk) · evaporasi Penman 142,6–166,2 mm/bulan (total 1.847,2 mm/th) ·
   Vs = 15.751,7 m³, **Vdesain = maks(Vs, Va) = 15.751,7 m³** (Vs > Va = 3.190,4 m³)
   → kolam 72,5 × 72,5 × 3,0 m (+0,5 m freeboard) · keandalan f65% = 99,4%.
7. **Belum dikerjakan (lihat bagian bawah):** lampiran Bab IV, perbarui Bab III
   (Supadio/ERA5 → BWSK/Penman), reformat Daftar Pustaka ke pedoman, muka-muka
   (abstrak 2 bahasa, daftar istilah/simbol), sinkron CAD, verifikasi lapangan,
   housekeeping, dan Bab V baru. PDF belum diekspor (LibreOffice `/Volumes/Lexar`
   tidak ter-mount saat sesi ini).

## SESI 30 OKT 2026 (LANJUTAN-4) — BAB III, LAMPIRAN, BAB V, CAD

1. **`tools/naskah_util.py` (BARU):** utilitas bersama generator naskah (margin
   Pedoman Untan, TNR 12, spasi 1,5, helper tabel/gambar/kapital).
2. **`tools/buat_bab3_docx.py` → `manuscript/BAB_III_REVISI.docx`:** Bab III
   direvisi sesuai 9 butir REVISI.md — sumber hujan BWSK 2012–2025 (justifikasi
   14 th), variabel iklim NOAA ISD Supadio + NASA POWER, **evaporasi** Penman +
   hujan langsung kolam (istilah ET0/E0 dihapus), data hilang 12 hari NULL
   (SNI 2415:2016 §4.2.3; WMO-168 §9.7.2), uji homogenitas 2 arah α = 5% (t kritis
   2,179), chi-kuadrat bin 0,50/0,20/0,10/0,06/0,14 + E ≥ 5, justifikasi T = 10
   (termasuk r = 1 − (1 − 1/T)^n → 87,8%), dan pipa kontinu (atap→kolam gravitasi,
   kolam→warga pompa).
3. **`tools/buat_lampiran_bab4_docx.py` → `manuscript/LAMPIRAN_BAB_IV.docx`:**
   Lampiran A (data hujan + QC + uji), B (analisis frekuensi + χ²), C (IDF Mononobe
   5–1.440 mnt + debit), D (iterasi hidrolika penuh + pipa standar), E (neraca
   bulanan 168 bulan fraksi 65%), F (rantai hitung evaporasi Penman), G (rekapitulasi
   hasil desain).
4. **`tools/buat_bab5_docx_baru.py` → `manuscript/BAB_V_KESIMPULAN.docx`:** Bab V
   baru (kesimpulan per rumusan masalah 1–4 + saran). RM4 (BEP) ditulis sebagai
   pekerjaan perancangan lanjutan — tidak mengarang angka ekonomi. Draf lama
   (`BAB_V_KESIMPULAN_DAN_SARAN.docx`) tidak dipakai.
5. **CAD disinkronkan:** `sket_lengkap.dxf` — “PIPA OUTFALL Ø800” → **DN900**;
   anotasi kolam → **15.751,7 M3 (H = 3.0 M) | AP = 5.256,25 M2**. Label
   “L = 814 m²” **tidak diubah** (itu luas lahan FASOS, bukan kolam). Backup:
   `sket_lengkap.dxf.bak`.
6. **Konsistensi angka:** kebutuhan desain 65% = 18.221 m³/tahun (rumus 76,8 × 0,65
   × 365); pasokan atap 25.132 m³/tahun; total pemasukan 41.010 m³/tahun. Catatan
   selisih bulan nyata vs 365 hari (18.235 vs 18.221; < 0,1%) diletakkan di Bab IV.

## SESI 29 OKT 2026 (LANJUTAN-2) — TRANSPARANSI EVAPORASI DI WORKBOOK

Permintaan: angka evaporasi Penman tidak boleh muncul begitu saja — semua langkah
kali/bagi harus tampil di sheet, ter-link, berformula, bisa divalidasi dosen.

1. **Sheet `Iklim_Harian` (baru, 15 sheet total):** data mentah harian NOAA ISD
   Supadio (T, Tmax, Tmin, Td, u10, SLP) + NASA POWER (Rs), 4.977 hari
   2012-01-01 s.d. 2025-08-24 (`data/processed/iklim_harian.csv`, ter-commit).
2. **Sheet `Evaporasi` dirombak total:** blok konstanta (alfa, z, k_ea, f_u2, phi,
   Gsc, G — dirujuk sel formula), parameter bulanan via SUMIFS/COUNTIFS atas
   `Iklim_Harian`, lalu **kolom formula langkah demi langkah**: es, ea, RH, delta,
   gamma, u2, J, dr, deklinasi, omega_s, Ra, Rso, Rs/Rso, Rns, Rnl, Rn, lambda,
   Ea, E0, evap mm/bulan. Tidak ada angka hasil hitung yang di-hardcode.
3. **Metode diseragamkan:** Python (`src/evaporasi_penman.py`) kini menghitung
   Penman dari **parameter iklim bulanan** (rata-rata harian per bulan kalender) —
   rute yang sama persis dengan formula Excel; nilai harian dibulatkan 2 desimal
   di sumbernya supaya agregasi identik. `build_db.py` membawa seluruh kolom
   rantai ke tabel `evaporasi`.
4. **Validasi silang:** `verifikasi_excel.py` memeriksa **setiap kolom rantai ×
   12 bulan** (342 cek) + spot-check `Iklim_Harian` terhadap CSV → LULUS.
5. Angka akibat rute bulanan (sedikit berubah vs rute harian): evaporasi
   **142,6–166,2 mm/bulan** (total 1.847,2 mm/tahun); iterasi Vs↔Ap tetap
   konvergen 5 langkah dengan titik tetap **Ap = 5.256,25 m²**.

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
| 3 | IV | Visualisasi hasil siap naskah (grafik Bab 4) | dikerjakan bersama Tahap 5 |
| 4 | IV | Analisis sensitivitas + pembahasan + verifikasi asumsi lapangan | dikerjakan bersama Tahap 5 |
| 5 | IV | Naskah Bab 4 final (docx) + lampiran | **NASKAH SELESAI** (`manuscript/BAB_IV_HASIL_DAN_PEMBAHASAN.docx`); lampiran menyusul |
| 1 | V | Jaringan distribusi bertekanan + pompa | **SELESAI (komputasi)** — `src/jaringan_distribusi.py`, `hasil_jaringan.json`; angka menunggu asistensi (jam operasi, elevasi bak) |
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

### Angka desain terakhir (Paket A — Penman + hujan kolam; TERVERIFIKASI 7.152 cek)
- R24 (T=10 th, LP3) = 163,236 mm; to = 0,154 mnt; td = 3,25 mnt; tc = 0,0568 jam; I = 383,15 mm/jam
- Q desain (maks iterasi) = 0,8862 m3/dtk; D teoritis = 810 mm -> **DN900**;
  v = 1,393 m/dtk; kapasitas Manning penuh = 1,1718 m3/dtk (AMAN)
- Q per unit = 5,54 l/dtk -> pipa DN160; talang 0,15x0,10 m kapasitas 10,82 l/dtk; bak 0,5 m3
- Evaporasi Penman muka air = 142,6-166,2 mm/bulan (total 1.847,2 mm/tahun; NOAA ISD + NASA POWER; rantai hitung live di sheet Evaporasi)
- Iterasi Vs<->Ap **KONVERGEN** 5 langkah (Ap 1.072,5 -> 4.257,5 -> 5.041 -> 5.220 -> 5.256,25 m2)
- Va (th=1 jam) = 3.190,4 m3; Vs = 15.751,7 m3 -> **V desain = 15.751,7 m3**
  -> kolam 72,5 x 72,5 x 3,0 m (+freeboard 0,5 m = 3,5 m); Ap = 5.256,25 m2
- Reliability: f=1,00: 88,7% | 0,70: 98,8% | **0,65: 99,4%** | 0,60: 100% | 0,50: 100%

## Peta file (setelah restukturisasi akhir Tahap 2)

Struktur repo standar riset Python (detail di `README.md`):

- `src/` — komputasi inti: `evaporasi_penman.py` (NOAA ISD + NASA POWER ->
  evaporasi Penman bulanan), `build_db.py` (raw/sample -> DB), `analisis2.py` (statistik,
  uji, frekuensi, chi-kuadrat -> hasil_validasi.json), `analisis_desain.py`
  (-> hasil_desain.json + tabel hasil_desain/neraca_bulanan);
  `legacy/analisis_hujan.py` (sudah digantikan analisis2.py)
- `tools/` — `buat_excel.py` (workbook 15 sheet formula hidup, termasuk Iklim_Harian
  + rantai hitung Penman langkah demi langkah di sheet Evaporasi), `buat_diagram.py`
  (-> figures/diagram-alur-hidrologi.html), `verifikasi_excel.py` (recalc + verifikasi
  silang, JALANKAN TERAKHIR), `recalc_excel.py` (bake cached values via LibreOffice),
  generator docx dari proyek lama
- `data/processed/` — SUMBER KEBENARAN: `hidrologi.db` + `hasil_validasi.json` +
  `hasil_desain.json` + `iklim_harian.csv` + `evaporasi_penman.csv/.json` +
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
python src/jaringan_distribusi.py   # Bab V Tahap 1: jaringan tekan + pompa (jalankan lagi setelah build_db)
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

## SESI 30 OKT 2026 (TAHAP 6) — FINISHING: PDF, CAD, ANALISIS LAHAN, HOUSEKEEPING

1. **PDF naskah SELESAI** (LibreOffice via `/Volumes/Lexar`): `manuscript/BAB_III_REVISI.pdf`,
   `BAB_IV_HASIL_DAN_PEMBAHASAN.pdf`, `LAMPIRAN_BAB_IV.pdf`, `BAB_V_KESIMPULAN.pdf`
   — ikut ter-commit (`!manuscript/*.pdf`).
2. **Render CAD SELESAI**: `tools/render_cad.py` (ezdxf + matplotlib) →
   `figures/sket_lengkap_dxf.png/.pdf` (vektor saja, latar putih) +
   `figures/sket_lengkap_dxf_satelit.png/.pdf` (vektor di atas citra satelit).
   Anotasi DN900 + kolam 15.751,7 M3 tampil; zoom ke blok siteplan.
3. **Analisis rekonsiliasi lahan (MENUNGGU KEPUTUSAN USER — jangan ubah workbook/DB
   sebelum disepakati):** Ap rencana 5.256,25 m² vs lahan FASOS 814 m². Hitungan
   (Rippl peak-to-trough tereplikasi persis thd `neraca_bulanan`; p_pond & evaporasi
   diskalakan linier ke Ap=814):
   - **Defisit lahan = 4.442,25 m²** (~6,5× luas FASOS).
   - Skenario **FASOS 814 m², he = 3,0 m → V = 2.442 m³** (he 3,5 m → 2.849 m³):
     fraksi 65% butuh **he ≈ 15,4 m** (Vs = 12.522,6 m³) — **tidak layak**.
   - **Fraksi maksimum yang muat di 814 m²:** f ≈ **0,45** (Vs = 2.747 m³ → he 3,37 m;
     54 l/hari/jiwa dari 120) — reliability 100% dgn V = 2.849 m³; f = 0,50
     (Vs = 4.558 m³) butuh he ≈ 5,6 m.
   - **Va atenuasi:** th = 0,5 jam = 1.595,2 m³ **muat** di 814 × 3,5 m;
     th = 1 jam = 3.190,4 m³ **tidak muat**.
   - **Opsi dibawa ke user:** (A) tambah lahan ~4.442 m² → desain tetap;
     (B) lahan FASOS saja, fraksi turun ke ~45% (Vs ≈ 2.747 m³, kolam 28,5 × 28,5 × 3,4 m);
     (C) kolam terdistribusi (FASOS + lahan tambahan di beberapa titik, total V tetap 15.751,7 m³);
     (D) kombinasi B + tambah he/bebas evap. Keputusan → dokumentasi di HANDOFF.md +
     konsekuensi (pipeline ulang + verifikasi) bila desain berubah.
   - **KEPUTUSAN USER (30 Okt 2026): opsi di atas DITUNDA untuk dibahas dengan dosen
     dulu (asistensi).** Selama menunggu: workbook/DB/naskah TIDAK diubah; angka desain
     tetap fraksi 65% (Vs = 15.751,7 m³). Bila dosen memilih salah satu opsi → eksekusi
     konsekuensinya (untuk B/C/D: pipeline penuh + `verifikasi_excel.py` LULUS +
     regenerasi naskah Bab IV + sinkron CAD).
4. **Housekeeping SELESAI**: lock `~$oposal Tesis (claude) (Revisi Antigravity) 2.docx`
   dihapus; `README.md` diperbarui (angka final: Vs 15.751,7 m³, kolam 72,5 × 72,5 × 3,0 m,
   evaporasi Penman, verifikasi 7.152 cek; isu terbuka disesuaikan).
5. **Checklist verifikasi lapangan (untuk user — survei/waterpass):**
   - Lo = 8 m: ukur panjang talang satu unit rumah contoh (2–3 unit beda blok).
   - S_atap = 30%: waterpass elevasi bibir vs titik rendah atap; catat elevasi ±cm.
   - S_pipa = 0,30%: waterpass tiap 5–10 m sepanjang saluran atap→kolam; foto profil.
   - he = 3 m: cek elevasi dasar rencana kolam vs elevasi inlet/outlet DN900.
   - Koordinat (GPS/WGS84): titik inlet kolam, outlet pelimpah, ujung outfall;
     lampirkan ke lampiran survei. Hasil → parameter_desain bila menyimpang (>10%:
     pipeline ulang + verifikasi).

## SESI 30 OKT 2026 (TAHAP 6 LANJUTAN) — BAB V TAHAP 1: JARINGAN DISTRIBUSI + POMPA

> **Detail lengkap + misi Tahap 2: [`HANDOFF_BAB_V_TAHAP_1.md`](HANDOFF_BAB_V_TAHAP_1.md).**
> Keputusan user: kerjakan dengan **angka awal (asumsi belum di-asistensi)** —
> asumsi ditandai kuning di workbook & `parameter_desain`, semuanya live.

Lingkup sesuai `HANDOFF_TAHAP_6.md` butir 6 (layout, tekanan/los, pompa →
`parameter_desain` + skrip `src/`).

1. **`src/jaringan_distribusi.py` (BARU):** mesin desain jaringan bertekanan
   kolam → 160 unit. Baca DB (kawasan/parameter_desain/hasil_desain), hitung
   Hazen-Williams (PVC C=140), pilih DN (pipa tekan, kriteria v 0,6–1,5 m/s),
   titik kerja pompa + daya. Output: tabel `jaringan_distribusi` (13 segmen),
   tabel `pipa_tekan` (DN25–DN160), 19 baris `parameter_desain`
   (asumsi + spesifikasi pompa — semua terdokumentasi kolom `ket`),
   `data/processed/hasil_jaringan.json` (TER-COMMIT).
2. **Hasil:** Q pompa **6,24 m³/jam** (kebutuhan 49,92 m³/hari ÷ 8 jam operasi);
   H kerja **22,29 m** (statis+tekanan sisa 5,0 + los gesek 15,72 + minor 1,57)
   → H terpilih **28 m** (margin 20%); motor **740 W** (P_shaft 688 W, η 0,55),
   **2 unit** (1 aktif + 1 cadangan), sentrifugal permukaan self-priming di rumah
   pompa FASOS. Debit jalur: suction DN63 → induk DN32 (v 1,08 m/dtk) → lateral
   DN25 → sambungan unit DN25; L total pipa 431,8 m.
3. **Asumsi yang masuk `parameter_desain` (BELUM di-asistensi — user memilih tetap
   jalan dengan angka awal; semuanya sel kuning live di workbook):** jam operasi
   8 jam/hari; elevasi bak unit +2,5 m; tekanan sisa 2,0 m; muka air kolam −0,5 m;
   v ekonomis 0,6–1,5 m/s; η pompa 0,55.
4. **Sheet 15 `Jaringan_Distribusi` (workbook 16 sheet, formula hidup):** rantai
   Q → DN → v → hf (Hazen-Williams per segmen) → H kerja → daya, plus cek live
   (v maks, H terpilih ≥ H kerja). `tools/verifikasi_excel.py` kini **LULUS
   7.225 pemeriksaan** (+73 cek sheet jaringan vs tabel `jaringan_distribusi`
   + `hasil_jaringan.json`). Recalc LibreOffice dilewati bila soffice tidak ada
   (SSD Lexar tidak ter-mount saat sesi ini) — workbook tetap valid.
5. **Figur Bab V:** `tools/buat_gambar_bab5.py` → `figures/gambar5-1.png`
   (diagram skematik jaringan + pompa) + `figures/gambar5-2.png` (profil los
   gesek jalur terburuk).
6. **Handoff Bab V:** [`HANDOFF_BAB_V_TAHAP_1.md`](HANDOFF_BAB_V_TAHAP_1.md) —
   posisi, artefak, daftar asumsi untuk asistensi, misi Tahap 2 (ekonomi).
7. **Belum dikerjakan Bab V:** naskah subbab jaringan+pompa (menunggu asumsi
   disepakati), Tahap 2 (ekonomi: RAB, retribusi, BEP), Tahap 3 (dashboard web
   lokal + test suite).

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

## Pekerjaan berikutnya: TAHAP 5 — Naskah Bab 4 final (docx) + lampiran

(Grafik Tahap 3 dan pembahasan Tahap 4 dikerjakan sebagai bagian dari Tahap 5:
buat grafiknya dulu untuk ditempel, lalu naskah final.)

Tujuan: naskah Bab IV final + lampiran; semua angka ditarik dari
`hasil_validasi.json`, `hasil_desain.json`, tabel `neraca_bulanan`/`hasil_desain`/
`evaporasi` di DB, dan workbook `Perhitungan_Hidrologi.xlsx` (tervalidasi 7.152 cek,
rantai hitung Penman tampil live di sheet Iklim_Harian + Evaporasi).

Daftar grafik yang dibuat (usulan, boleh disesuaikan):
1. Curah hujan tahunan (total) + X maks harian per tahun — dari statistik/DB.
2. Uji konsistensi: S**k/Dy kumulatif + garis kritik 95% & 99% (Tabel 2.3 interpolasi).
3. Kurva frekuensi XT: Normal, Gumbel, LP3 + titik observasi + penanda R24 T=10 th.
4. Kurva massa Rippl: K kumulatif fraksi desain (65%) + penanda Vs, Va, dan V desain;
   opsional overlay 5 fraksi.
5. Neraca bulanan fraksi desain: supply atap + hujan kolam vs demand + evaporasi
   per bulan + garis kumulatif.
6. Sensitivitas: (a) Vs vs fraksi kebutuhan; (b) Va vs th (0,5-3 jam);
   (c) iterasi konvergensi Vs<->Ap (BUKAN pass-1/2/3 — sudah diganti Paket A).
7. Hidrolika pipa: Q per iterasi (menunjukkan osilasi + envelope) + Q desain vs
   kapasitas DN900.
8. (Opsional) evaporasi Penman bulanan: batang E0 mm/bulan + komponen iklim.

Checklist tahap 5:
- [x] Buat `tools/buat_grafik.py` (baca DB/JSON, jangan hitung ulang rumus)
- [x] Output PNG dpi 300 (+ SVG opsional) ke `figures/`, penomoran mengikuti
      urutan Bab 4 (mis. gambar4-1.png ...)
- [x] Semua angka pada grafik identik dengan json/DB (sudah tervalidasi)
- [x] Legenda/label Bahasa Indonesia, satuan lengkap, konsisten dgn sheet Excel
- [x] Pembahasan (Tahap 4): sensitivitas th/fraksi/evaporasi + verifikasi asumsi
      lapangan (flag #3) + konsistensi sumber data (flag #4) — masuk Subbab 4.9 & 4.10
- [x] Naskah Bab 4 final docx — `manuscript/BAB_IV_HASIL_DAN_PEMBAHASAN.docx`
      (generator `tools/buat_bab4_docx.py`); ikuti `TEMUAN GLM-5.3.md` + pedoman Untan
- [ ] **Lampiran Bab 4** (tabel iterasi lengkap, kurva IDF penuh, dsb.) — menyusul
- [x] Pipeline tidak diubah; `verifikasi_excel.py` tidak perlu dijalankan ulang
      (tidak ada perubahan pada DB/JSON/xlsx). Jika ragu, jalankan ulang dari root.
- [x] Perbarui tabel status di dokumen HANDOFF.md ini

## Sisa pekerjaan Tahap 5 / lanjutan (belum selesai)

1. ~~Lampiran Bab IV~~ **SELESAI** — `manuscript/LAMPIRAN_BAB_IV.docx`.
2. ~~Bab III~~ **SELESAI** — `manuscript/BAB_III_REVISI.docx` (9 butir REVISI.md).
3. **Daftar Pustaka** — reformat lewat **Mendeley** (diputuskan user).
4. **Muka-muka** (pernyataan, pengesahan, abstrak 2 bahasa, daftar istilah/simbol)
   — dikerjakan user.
5. ~~Bab V baru~~ **SELESAI** — `manuscript/BAB_V_KESIMPULAN.docx`.
6. ~~Sinkron CAD~~ **SELESAI** — `sket_lengkap.dxf` (+ backup .bak); render
   `sket_lengkap.pdf/.png` belum diperbarui.
7. **Verifikasi lapangan** (Lo, S_atap, S_pipa, he) + housekeeping
   (hapus file lock `~$oposal Tesis ...docx`, perbarui README).
8. **Ekspor PDF** naskah — butuh LibreOffice (`/Volumes/Lexar/APPS/LibreOffice.app`),
   belum ter-mount.
9. **Rekonsiliasi lahan kolam**: Ap rencana 5.256,25 m² vs lahan FASOS 814 m² —
   perlu keputusan alokasi lahan.

## Panduan memulai sesi baru

> Untuk sesi/Tahap 6 berikutnya ada handoff khusus:
> [`HANDOFF_TAHAP_6.md`](HANDOFF_TAHAP_6.md) (misi Bab IV Tahap 3 + checklist).

1. Baca HANDOFF.md ini + `README.md` + `data/processed/hasil_desain.json`.
2. Beri user ringkasan 2 kalimat (status: tahap 1 & 2 Bab IV selesai, lanjut tahap 3).
3. Kerjakan checklist tahap 3 di atas; semua perubahan skrip di `src/`/`tools/`,
   hasil di `data/processed/` & `figures/`, jangan ubah DB/JSON yang sudah
   tervalidasi kecuali memang ada perubahan input (lalu pipeline ulang penuh).
