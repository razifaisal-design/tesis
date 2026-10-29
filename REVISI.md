# Catatan Revisi Tesis — Keputusan 29 Oktober 2026

Dokumen ini merangkum keputusan revisi berdasarkan hasil audit pipeline Tahap 2.
Status: **keputusan 1, 2, 4, 5 sudah DIEKSEKUSI (sesi Paket A, 29 Okt 2026 lanjutan);
pipeline penuh LULUS verifikasi (6.807 cek, 0 gagal).** Keputusan 3, 6-16 berlaku
sebagaimana dicatat.

## Ringkasan

| No | Topik | Keputusan | Status |
|---|---|---|---|
| 1 | Evaporasi kolam | Dikunci memakai **metode Penman**; hujan langsung di permukaan kolam dimasukkan | **DIEKSEKUSI** — Penman 142,3-166,2 mm/bulan + P×Ap; iterasi Vs↔Ap konvergen |
| 2 | `Ap_kolam = 1.200 m²` | **Dihapus** | **DIEKSEKUSI** — dihapus dari DB; B9 Desain_Kolam = hasil iterasi (5.292,5 m²) |
| 3 | Data harian kosong | Tetap **NULL**, tidak diisi; asistensi dosen | Berlaku sekarang |
| 4 | `hasil_validasi.json` | Field lama `to/td/tc/I/Q` dihapus/ditandai; sheet `Debit_Rencana` & diagram disinkronkan | **DIEKSEKUSI** — field dihapus; Debit_Rencana = ringkasan tautan silang |
| 5 | Uji chi-kuadrat | Pakai **hitungan terakhir** (bin 0,50/0,20/0,10/0,06/0,14; E ≥ 5) | **DIEKSEKUSI** — χ² = 2,3673; LP3 terpilih; uji gabungan E≥5 di chi.e5 |
| 6 | Uji homogenitas | Satu kriteria: **2 arah, α = 5%** (t kritis 2,179) → t = 1,851 → homogen | Dikunci |
| 7 | Desain pipa | Anggap **kontinu** dulu; kemiringan tetap; detail kehilangan energi/ujung/pompa nanti | Dicatat |
| 8 | Dasar T = 10 | Ikut jurnal (Bangkinang; Roy dkk.) | Dikunci |
| 9 | Data Supadio | **Tidak dipakai**; hari kosong tetap NULL | Dicatat |
| 10 | Istilah | Tidak memakai “ET0/E0”; gunakan **“evaporasi”** | Dikunci |
| 11 | Sumber hujan | **BWSK 14 tahun** (2012–2025) | Dikunci |
| 12 | Bab IV/V | Perbarui dengan angka baru | Dicatat untuk revisi |
| 13 | Grafik Tahap 3 | 7 gambar dari DB/JSON | Dicatat untuk revisi |
| 14 | CAD | Sinkronkan DXF (Ø800 → DN900, anotasi kolam) | Dicatat untuk revisi |
| 15 | Verifikasi lapangan | Lo, S_atap, S_pipa, he | Dicatat untuk revisi |
| 16 | Housekeeping | README/HANDOFF, file temp, struktur folder | Dicatat untuk revisi |

---

## 1. Evaporasi kolam — dikunci metode Penman

- **Keputusan:** evaporasi kolam dihitung dengan **metode Penman** (bukan ET0 rumput), dan **hujan langsung di permukaan kolam** (`P × Ap`) dimasukkan sebagai pemasukan.
- **Istilah:** naskah dan kode tidak memakai “ET0/E0”; cukup **“evaporasi”** (lihat butir 10).
- **Alasan:** ET0 adalah evapotranspirasi tanaman acuan (rumput, albedo 0,23, rs 70 s/m), bukan muka air. Tanpa suku hujan langsung, neraca meledak (35.121 → 139.673 → 844.023 m³).
- **Angka acuan sementara** (data iklim BPS Kubu Raya 2024):
  - evaporasi Penman ≈ **149 mm/bulan**;
  - dengan hujan langsung di kolam, iterasi konvergen pada **Vs ≈ 15.085 m³**, Ap ≈ 5.041 m², kolam **71 × 71 × 3,0 m**;
  - sebagai pembanding, dengan ET0 ≈ 117 mm/bulan: Vs ≈ 11.208 m³, kolam 61 × 61,5 × 3,0 m.
- **Status:** **DIEKSEKUSI** (sesi Paket A). `src/evaporasi_penman.py` menghitung
  Penman muka air harian 2012–2025 (NOAA ISD Supadio + NASA POWER Rs) →
  **142,3–166,2 mm/bulan** (rata-rata 154,3), tabel `evaporasi` di DB terisi,
  hujan langsung `P × Ap` masuk neraca sebagai pemasukan, iterasi Vs ↔ Ap
  **konvergen** (5 langkah, Ap = 5.292,5 m², Vs = 15.823,6 m³).

## 2. `Ap_kolam = 1.200 m²` dihapus

- **Keputusan:** hapus nilai placeholder 1.200 m².
- **Alasan:** 1.200 adalah pembulatan luas kriteria atenuasi (1.072,5 m²), bukan luas desain final (5.076,5 m²).
- **Perubahan yang diperlukan (4 file):**
  1. `src/build_db.py` — hapus baris `("Ap_kolam", 1200.0, ...)`.
  2. `src/analisis_desain.py` — hapus `Ap = num(par, "Ap_kolam")` (nilai ini toh ditimpa oleh hasil dimensi).
  3. `tools/buat_excel.py` — sel `Desain_Kolam!B9` diambil dari tabel `hasil_desain` (nilai terhitung), bukan `parameter_desain`; catatan konsistensi `B42` disesuaikan.
  4. `tools/verifikasi_excel.py` — cek `B42` disesuaikan.
- **Status:** **DIEKSEKUSI** — `Ap_kolam` dihapus dari `build_db.py` dan
  `analisis_desain.py`; `Desain_Kolam!B9` diisi dari tabel `hasil_desain`
  (Ap iterasi 5.292,5 m²); cek B42 kini memverifikasi konvergensi iterasi secara live.

## 3. Data harian kosong tetap NULL

- **Keputusan:** 12 hari hilang dibiarkan `NULL`; **tidak** diisi M2 untuk sementara; akan diasistensikan ke dosen.
- **Konsekuensi:** keputusan pengisian M2 pada arsip `Tahap_1b_Analisis_Data_Hilang_Ambawang_2012-2025.xlsx` **ditangguhkan** dan tidak diterapkan di `build_db.py`.
- **Catatan teknis:** untuk Tahap 1 (frekuensi) ini sudah benar; untuk Tahap 2 (neraca) hanya berdampak pada Maret 2023 (309 mm vs 413,9 mm bila M2 diterapkan).
- **Status:** berlaku sekarang (kode memang sudah NULL).

## 4. `hasil_validasi.json` — bersihkan field lama

- **Keputusan:** field `to/td/tc/I/Q` yang berasal dari parameter lama (Lo=200, Ss=0,002, Ld=300; Q=0,286) **dihapus atau ditandai legacy**, lalu sheet `Debit_Rencana` dan `tools/buat_diagram.py` disinkronkan.
- **Alasan:** field tersebut tidak dipakai mesin desain (hanya R24 dan distribusi), tetapi dipakai verifikasi dan diagram sehingga menyesatkan.
- **Status:** **DIEKSEKUSI** — field `to/td/tc/I/Q/Vch/C/A_km2` dihapus dari
  `hasil_validasi.json`; sheet `Debit_Rencana` menjadi ringkasan tautan silang ke
  `Hidrolika_Pipa` (parameter lama Lo=200/B/y ikut dihapus); `buat_diagram.py`
  memakai `hasil_desain.json`. Bonus: bug bayangan `kons.Q` ikut teratasi.

## 5. Uji chi-kuadrat — pakai hitungan terakhir

- **Keputusan:** gunakan perhitungan terakhir dengan probabilitas bin yang menjumlah 1:
  `0,50 + 0,20 + 0,10 + 0,06 + 0,14 = 1,00`.
- **Tambahan:** gabungkan bin agar frekuensi harapan `E ≥ 5`.
- **Hasil uji ulang:** χ² ≈ **2,37** (sebelumnya 2,2429 dengan E = 12,6 dari 14); kesimpulan tetap **lolos**, distribusi terpilih tetap **LP3**.
- **Status:** **DIEKSEKUSI** — bin 0,50/0,20/0,10/0,06/0,14 di `analisis2.py` dan
  sheet `Koefisien`; χ² = 2,3673 (LP3 terpilih). Syarat E ≥ 5 ditinjau dengan kelas
  gabungan (O=[9,5], E=[7,7], χ²=1,143) di field `chi.*.e5`.

## 6. Uji homogenitas — satu kriteria

- **Keputusan:** gunakan **uji 2 arah, α = 5%**, t kritis (dk = 12) = **2,179**.
- **Hasil:** t hitung = **1,851** < 2,179 → **homogen**.
- **Catatan:** bila memakai 1 arah (t kritis 1,782) hasilnya **tidak homogen**. Kriteria yang dipilih harus ditulis eksplisit di naskah agar tidak ambigu.
- **Status:** dikunci.

## 7. Desain pipa — kontinu dulu

- **Keputusan:** untuk sementara pipa diperlakukan **kontinu**; kemiringan pipa **tetap diperlukan**.
- **Skema yang dituju:**
  - atap → kolam: **gravitasi**;
  - kolam → warga: **pompa**, dihitung pada tahap teknis berikutnya.
- **Detail yang ditunda:** kehilangan energi di ujung pipa, kehilangan gesekan lokal, pemilihan pompa, dan iterasi diameter diskrit.
- **Status:** dicatat; tidak ada perubahan kode sekarang.

## 8. Dasar T = 10 — ikut jurnal

- **Keputusan:** T = 10 tahun dipertahankan dengan dukungan jurnal.
- **Ketersediaan di repo (lokal):**
  - Bangkinang: `data/raw/arsip-tesis-lengkap/05_Jurnal_dan_Referensi/Jurnal/200993-simulasi-kolam-retensi-untuk-mengatasi-b.pdf` — Rachman, Mudjiatko, Trimaijon, “Simulasi Kolam Retensi untuk Mengatasi Banjir Genangan di Kota Bangkinang Bagian Barat”, Universitas Riau.
  - Roy dkk.: `data/raw/arsip-tesis-lengkap/05_Jurnal_dan_Referensi/Jurnal/1317-ArticleText-2345-1-10-20190326.pdf` — “Pemanfaatan Kolam Retensi dan Sumur Resapan pada Sistem Drainase Kawasan Padat Penduduk”, *Jurnal Teknik Sipil* 5(2), 2019, DOI 10.28932/jts.v5i2.1317.
- **Catatan:** `data/raw` di-*gitignore*; kedua PDF hanya ada di mesin lokal, tidak ikut commit.
- **Status:** dikunci.

## 9. Supadio tidak dipakai; hari kosong NULL

- **Keputusan:** data hujan Supadio **tidak dipakai**; hari kosong tetap `NULL`.
- **Status:** dicatat.

## 10. Terminologi dan isi data Supadio

- **Keputusan:** tidak memakai istilah “ET0” atau “E0”; gunakan **“evaporasi”** (dengan metode Penman).
- **Isi data harian BMKG Supadio (WMO 96581):** curah hujan, suhu minimum/rata-rata/maksimum, kelembapan, kecepatan dan arah angin, lama penyinaran matahari, tekanan udara, dan penutupan awan.
- **Yang ada di repo:** tidak ada file harian Supadio. Yang tersedia hanya tabel iklim **bulanan** BPS Kubu Raya Dalam Angka 2025/2026 (sumber: BMKG Supadio), memuat suhu, kelembapan, angin, tekanan, penyinaran, hujan, dan hari hujan.
- **Implikasi:** bila Supadio benar-benar tidak dipakai untuk **variabel iklim**, metode Penman tidak dapat dihitung dari data BWSK (BWSK hanya hujan). Perlu sumber lain (ERA5) atau asumsi eksplisit.
- **Status:** dikunci; pertanyaan dijawab.

## 11. Sumber data hujan

- **Keputusan:** **BWSK 2012–2025 (14 tahun)**; Supadio tidak dipakai (tidak ada data harian di repo).
- **Status:** dikunci.

---

## 12–16. Catatan untuk revisi (belum dieksekusi)

### 12. Perbarui Bab IV dan Bab V
- Ganti seluruh angka lama di `manuscript/bab 4 claude (Revisi Antigravity).docx` dan `manuscript/BAB_V_KESIMPULAN_DAN_SARAN.docx`.
- Angka lama yang harus diganti: R24 153,46 → 163,236 mm; Q 1,172 → 0,8862 m³/dtk; Vs 517 → 15.148,4 m³; kolam 814 m² → 5.076,5 m².
- Jangan mencampur angka lama dan baru dalam satu tabel.
- Sesuaikan narasi dominasi: dahulu Va > Vs, sekarang **Vs > Va**.

### 13. Grafik Tahap 3
- Buat `tools/buat_grafik.py` yang membaca DB/JSON (tidak menghitung ulang).
- Output `figures/gambar4-*.png`, dpi 300, label Bahasa Indonesia.
- Tujuh grafik: hujan tahunan; uji konsistensi kumulatif; kurva frekuensi XT; kurva Rippl (penanda Va, Vs, V desain); neraca bulanan; sensitivitas Vs/Va; osilasi iterasi hidrolika.

### 14. Sinkronkan CAD
- `data/raw/arsip-tesis-lengkap/03_Desain_CAD_dan_Peta/sket_lengkap.dxf`:
  - “PIPA OUTFALL Ø800” → **DN900**;
  - “L = 814 m²” → luas kolam baru;
  - “VOL. TAMPUNGAN = 1.025 M3 (H = 1.6 M)” → volume/kedalaman baru.

### 15. Verifikasi lapangan
- Lo (8 m), S_atap (30%), S_pipa (0,30%), he (3,0 m) masih asumsi.
- Perlu waterpass untuk kemiringan pipa dan elevasi outlet.

### 16. Housekeeping
- Perbarui `README.md` dan `HANDOFF.md` agar sesuai keputusan 1–11.
- Hapus file temp `~$oposal Tesis (claude) (Revisi Antigravity) 2.docx`.
- Pastikan `figures/` dan `notebooks/` berisi.

---

## Revisi Bab III (wajib)

Bab III saat ini masih menyebut Supadio 2000–2024 + ERA5. Perlu diperbarui:

1. **Sumber hujan:** BWSK Sungai Ambawang 2012–2025 (14 tahun). Jelaskan bahwa SNI 2415:2016 §4.2.1 menyarankan >20 tahun, tetapi pedoman PU Cipta Karya mensyaratkan minimum 10 tahun; data harian Supadio tidak tersedia di repo.
2. **Variabel iklim:** suhu, RH, angin, tekanan dari **NOAA ISD Supadio**; radiasi (Rs) dari **NASA POWER** (CERES). Tulis bahwa NASA POWER adalah produk satelit/reanalisis, bukan pengamatan stasiun, dan validasi terhadap pola musiman.
3. **Evaporasi:** metode **Penman muka air**, bukan ET0 rumput; masukkan **hujan langsung di permukaan kolam** (`P × Ap`). Hilangkan istilah ET0/E0; gunakan “evaporasi”.
4. **Data hilang:** 12 hari NULL, tidak diisi; dasar SNI 2415:2016 §4.2.3 dan WMO-168 §9.7.2. Sebut xmax 2023 sebagai **maksimum teramati**.
5. **Uji homogenitas:** tulis kriteria **2 arah, α = 5%** (t kritis 2,179).
6. **Chi-kuadrat:** probabilitas bin menjumlah 1 (0,50/0,20/0,10/0,06/0,14) dan syarat E ≥ 5.
7. **Kala ulang T = 10:** justifikasi dengan pedoman PU (Tabel 1: <10 ha → 2 tahun; T = 10 konservatif), Tata Cara Kolam Retensi PU (pilih T berdasarkan risiko), jurnal Bangkinang/Sekuting/Roy, dan rumus risiko `r = 1 − (1 − 1/T)^n` (T = 10, n = 20 → 87,8%).
8. **Hidrolika pipa:** pipa dianggap **kontinu** untuk sementara; kemiringan tetap; atap → kolam gravitasi; kolam → warga pompa (tahap V).
9. **Terminologi:** tidak memakai “ET0/E0”; cukup “evaporasi”.

---

## Blocker yang harus diputuskan sebelum eksekusi kode

1. **Sumber data iklim untuk Penman — sudah ditemukan, tinggal persetujuan dosen.**
   - NOAA ISD Supadio `96581099999`: T, RH (dari titik embun), angin, tekanan, tutupan awan — CSV langsung 2012–2025.
   - NASA POWER: Rs harian 2012–2025, 5.114 hari, 0 hilang — `data/raw/nasa_power/NASA_POWER_daily_2012-2025.csv`.
   - SACAD BMKG **tidak punya `ss`** untuk Pontianak (Maritim Pontianak hanya presipitasi); BMKG Data Online memerlukan login.
   - Rekomendasi: **ISD Supadio + NASA POWER**. Pastikan dosen menyetujui penggunaan produk satelit/reanalisis untuk radiasi.

2. **Kriteria homogenitas** sudah dipilih 2 arah α = 5% (butir 6). Pastikan dosen menyetujui, karena dengan 1 arah kesimpulannya berubah.

3. **M2 benar-benar dibatalkan?** Butir 3 menangguhkan pengisian M2 sampai asistensi. Selama itu, neraca Tahap 2 memakai deret NULL (Maret 2023 = 309 mm).

## Urutan eksekusi yang disarankan

- **Paket A:** butir 1, 2, 4, 5 — **SELESAI** (sesi 29 Okt 2026 lanjutan; pipeline
  penuh + `tools/verifikasi_excel.py` lulus, 6.807 cek 0 gagal).
- **Paket B (berikutnya):** butir 12–14 — naskah dan grafik.
- **Paket C:** butir 15–16 — verifikasi lapangan dan housekeeping.
