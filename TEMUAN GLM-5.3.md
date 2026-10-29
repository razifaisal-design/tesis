# TEMUAN GLM-5.3 — Catatan Review Sesi 2026-10-29/30

**Peran sesi ini:** reviewer/auditor (tidak mengubah dokumen asli; hanya membaca, mengekstrak, dan membuat catatan). Tugas utama (penulisan naskah, pipeline) dikerjakan agent/sesi lain.

**Lingkup pemeriksaan:** kesesuaian "Tesis Penuh" terhadap Proposal Tesis (claude) (Revisi Antigravity) 2.docx, keandalan file-file naskah, novelty, dan kesesuaian format terhadap *Pedoman Penulisan Tesis Magister Teknik Sipil Untan (1).pdf* (Okt 2017).

---

## 1. STATUS DAN IDENTITAS FILE (penting untuk sesi berikutnya)

| File | Lokasi | Keadaan terlihat |
|---|---|---|
| `Proposal Tesis (claude) (Revisi Antigravity) 2.docx` | `manuscript/` | HANYA memuat **Bab I–III + Daftar Pustaka** (cover masih "PROPOSAL TESIS"). Ini yang dianggap "Tesis Penuh" oleh user. |
| `manuscript/tesis_text.txt` | `manuscript/` | Ekstraksi teks proposal docx; sudah diverifikasi deviasi vs docx hanya format/whitespace. **Bukan tesis penuh.** |
| `manuscript/bab 4 claude (Revisi Antigravity).docx` | `manuscript/` | Draft Bab IV, berisi dua lapisan: perhitungan bertahap + blok "[REVISI ANTIGRAVITY ...]" (dibahas Bag. 3). |
| `manuscript/BAB_V_KESIMPULAN_DAN_SARAN.docx` | `manuscript/` | **Draf LAMA** — identik bit-per-bit dengan `data/raw/arsip-tesis-lengkap/02_Bab_dan_Revisi_Parsial/BAB_V_KESIMPULAN_DAN_SARAN.docx` (diverifikasi via diff). Memiliki kesimpulan+saran lengkap tapi dengan angka proyek lama (Supadio, neraca harian, 87,4%). **TIDAK relevan untuk tesis baru.** |
| `Tesis (3).docx` | `data/raw/arsip-tesis-lengkap/02_Bab_dan_Revisi_Parsial/` | **Skripsi lama 2014 (Jembatan Lengkung Rangka Baja) secara utuh.** XML-nya `document.xml` tidak mengandung satu kata pun tentang Rajawali/RWH; docProps internal: last-modified 2025-05-27, revision 899. **JANGAN diperlakukan sebagai tesis.** |
| Lock file `~$oposal Tesis (claude) (Revisi Antigravity) 2.docx` | root repo (dan di salinan GDrive `Tesis-update/Hidrologi/`) | Tanda dokumen proposal **sedang terbuka di Word** (dibuat 19:04). Salinan disk mtime 2026-10-26 21:08 = belum tersimpan versi edit yang jalan. |
| Salinan repo GDrive | `GoogleDrive-.../My Drive/Tesis-update/Hidrologi/` | Mirror repo, sinkron 2026-10-29 23:11, isi sama. |
| PEDOMAN | `/Users/razi/Downloads/pedoman tesis magister teknik sipil untan (1).pdf` | Acuan format resmi (Okt 2017); dibahas Bag. 5. |
| `manuscript/novelty.md` | `manuscript/` (dibuat sesi ini, disetujui user) | Gabungan `novelty.docx` lama + cek literatur internasional 2023–2026. |

---

## 2. PEMERIKSAAN "TESIS PENUH" vs PROPOSAL — yang SUDAH sesuai

Bab I–III dikonfirmasi lebih dahulu:
- Sumber data: Stasiun Supadio WMO 96581 2000–2024 (25 th) untuk hujan harian maks, + ERA5 untuk hujan bulanan/ET0 — **konsisten antara 3.3.2 dan 4.2.1 Bab IV**.
- Kebutuhan air: 160 unit × 4 jiwa × 120 L/jiwa/hari (SNI 03-7065-2005) = 76,8 m³/hari = 28.032 m³/th — cocok.
- Fraksi kebutuhan yang dilayani: 100/70/65/60/50%, desain 65% (rujuk Vovk dkk. 2023) — cocok dengan 3.4.1.
- Hujan rencana T = 10 th (Mononobe–Rasional); tiga kandidat distribusi + Chi-Kuadrat 5 kelas batas T = 2/5/10/25 — cocok dengan 2.3.1b dan 3.4.1.
- Kriteria ganda Vdesain = maks(Vs, Va), th = 1 jam (3.4.3) — secara literal masih muncul di Bab IV (Tabel 4.19/4.20).
- Evaporasi Ei = ET0 × 1,0 × luas muka kolam — sudah diterapkan (tabel 4.15).
- Batasan: air hujan non-potabel, tanpa sumur bor (baseline) — terpelihara.

---

## 3. PEMERIKSAAN "TESIS PENUH" vs PROPOSAL — yang TIDAK sesuai / bermasalah

### 3a. Bab IV — dua lapisan metodologi bertabrakan
1. **Pipa**: tabel 4.11 memilih pipa beton Ø914,4 mm (36") dari basis Mononobe pada tc ≈ 2,04 mnt (I = 506,7 mm/jam, Q = 1,172 m³/th), tetapi blok catatan revisi menetapkan PVC Ø350 mm basis **durasi 1 jam** (I = 53,22 mm/jam, Q = 0,123 m³/th). Basis durasi 1 jam **tidak ada di Persamaan 2.18 dan 3.4.2** yang fix di Bab II/III. → perlu konsilasi: satu metode durasi, satu set tabel.
2. **Va**: tabel 4.19 pakai Va = 4.219 m³ (Qout = 0, konservatif, sesuai Persamaan 2.31), tapi blok revisi menetapkan Va = 350 m³ dengan **Qout = 50 L/s (weir)** — mekanisme pelepasan ini tidak direpresentasikan di Persamaan 2.30–2.31 Bab II. Kalau mau dipertahankan, Persamaan Bab II/III harus diubah dulu (tapi Bab I–III dinyatakan fix oleh user → berarti blok revisi harus dipindah ke subbab "pembahasan/peninjauan", bukan mengganti metode).
3. **Kriteria ganda berubah diam-diam**: Persamaan 2.32 (fix) = maks(Vs, Va); revisi memakai penjumlahan Vs + Va + Vsedimen = 921,4 m³, dan di kalimat yang sama ditulis 876,8 m³ (inkonsistensi internal — satu dari dua angka salah).
4. **Freeboard**: proposal 2.7 menetapkan 0,50 m; blok revisi kolam FASOS memakai 0,30 m.
5. **Evaporasi tidak dihitung ulang**: Tabel 4.15 masih menghitung Ei dengan luas muka kolam iterasi lama (2.110 m²), padahal label parameter sudah diganti 646 m² (HWL FASOS 19×34). Kalau FASOS permanen → semua Ei dan kumulatif Rippl (4.16) perlu dihitung ulang (bisa menggeser nilai Vs).
6. **Keterbatasan Bab IV**: penomoran butir rusak (1–4 → lompat ke 7 → item 6–7) dan ada item "7. Perancangan teknis ... pada Subbab 4.10" yang tidak formal.
7. **Rujukan tambahan Bab IV** (Menne, Zippenfenig, Open-Meteo) **belum masuk Daftar Pustaka** dan belum disitasi di Bab III (3.3.2) tempat sumber data pertama diperkenalkan.
8. Excel deliverable dirujuk "Excel Analisis Tesis (claude).xlsx" yang saat ini berada di folder `Downloads/` — melanggar konvensi repo (FILE DELIVERABLE HARUS DI REPO) — perlu dimasukkan ke `data/processed/` sesuai konvensi HANDOFF.

### 3b. BAB V file — paling lepas dari proposal (dan BUKAN tesis baru)
1. Kesimpulan menyebut "**simulasi neraca air harian** (daily water balance)" — melanggar 3.4.1 (fix): **neraca bulanan** via kurva massa Rippl; Bab IV juga bulanan (simulasi 300 bulan).
2. Keandalan **87,4%** vs kesimpulan Bab IV **99,7%** — dua angka berbeda untuk fungsi keandalan sama.
3. Kebutuhan air 60 L/jiwa/hari (= 38,4 m³/hari) = **fraksi 50%**, bukan fraksi desain 65% (39,92 m³/hari per 3.4.1) — melanggar kriteria desain fix.
4. Vdesain ditulis "921,4 m³ (~876,8 m³ muka air efektif)" dalam satu kalimat — angka internal saling bertabrakan (band. Bag. 3a poin 3).
5. **Overlap lingkup Bab IV 4.10**: pembahasan ekonomi (CAPEX/NPV/BCR/tarif impas) di 4.10 diulang kembali sebagai kesimpulan BAB V — kesimpulan seharusnya tidak memperkenalkan metodologi maupun angka yang baru.

### 3c. Konflik sumber data (flag lama HANDOFF #4, belum selesai)
- Proposal (fix) menyebut **Supadio + ERA5**; pipeline tervalidasi repo (`data/processed/hidrologi.db`, `hasil_desain.json`) memakai **BWSK Sungai Ambawang 2012–2025**: R24 = 163,236 mm; Vdesain = 15.148,4 m³; kolam 71 × 71,5 m; DN900; keandalan f65% = 99,4%.
- Draft Bab IV/BAB V lama memakai Supadio: R24 = 153,46 mm; Vs = 517 m³; keandalan 99,7% (Bab IV) / 87,4% (BAB V).
- Per HANDOFF: **pipeline = sumber kebenaran angka**; jika user sudah putuskan Bab I–III fix dengan Supadio, maka pipeline (dan handoff) yang perlu diarahkan ulang/rekonciliasi — keputusan ini **wajib ditutup sebelum Bab IV final**; dilarang mencampur angka lama & baru dalam satu tabel.

---

## 4. NOVELTY (dibahas & disimpan ke `manuscript/novelty.md`)

- Sumber ada: `data/raw/arsip-tesis-lengkap/02_Bab_dan_Revisi_Parsial/novelty.docx` (review jurnal Indonesia: Unsrat 2023, UB 2022, ITENAS 2024, Unila, ITERA, UNY) + cek internasional (Water Research 2023 robust optim RWH+flood; MDPI Water 2024 hybrid detention+RWH; studi skala kota 2026; Vovk 2023).
- **Bukan** novelty: metode hidrologi standar; konsep dual-benefit kolam; RWH non-potabel.
- **Novelty** (4 lapis): (1) rantai tertutup penuh skala kawasan 160 unit → kolam komunal; (2) kriteria desain fraksi kebutuhan (5 fraksi, desain 65%) + kriteria ganda maks(Vs,Va) + iterasi envelope hidrolika pipa; (3) evaluasi investasi dari sudut pengembang (BEP/Payback); (4) konteks lahan gambut peri-urban Kubu Raya (tanpa infiltrasi yang justru tidak diinginkan).
- Inti satu kalimat + paragraf "Kebaruan Penelitian" siap tempel ada di `manuscript/novelty.md` Bag. 4.

---

## 5. PEMERIKSAAN FORMAT vs PEDOMAN UNTAN (Okt 2017) — *bahan audit tata tulis*

### 5a. Konflik struktur bab (paling penting)
- Pedoman **5 bab**: Bab I Pendahuluan, II Tinjauan Pustaka, III Metodologi, **IV Hasil dan Pembahasan, V Kesimpulan dan Saran** (§3.2.4–3.2.5).
- Batas Bab III thesis (fix) domain "perancangan teknis + ekonomi di Bab V" → **bertabrakan** dengan pedoman.
- **Dua opsi**: (a) geser perancangan & ekonomi ke Bab IV (misalnya "Bab IV Hasil, Pembahasan dan Perancangan") dan BAB V = Kesimpulan/Saran; atau (b) ubah batas Bab III. Rekomendasi saya: **opsi (a)**.
- Pemetaan subbab yang saya usulkan (versi opsi a) sudah diposting di chat sesi ini; outline: 4.1 → 4.11 analisis; 4.x perancangan; 5. Kesimpulan & Saran per RM 1–4.

### 5b. Daftar Pustaka — format BUKAN APA
- Pedoman §3.3.1 & Lampiran O: `Nama Belakang, Tahun, Judul, Penerbit, Kota.` — jurnal: `Nama, Tahun, Judul Artikel, Nama Jurnal, Vol(x), Hal. a-b.`
- Semua entri daftar pustaka tesis sekarang APA (`Azis, S. U., ... (2019). ...`) → **harus direformat total**; plus: hanging indent 1 cm, 1,5 spasi, tanpa gelar, tautan digital "diunduh pada tanggal".

### 5c. Bagian muka yang wajib (§3.1) dan keadaannya
- Wajib: Hal Pernyataan Keaslian (Lampiran C), Hal Pengesahan (D), Persembahan opsional ≤½ hal.; Kata Pengantar ≤1 hal.; **Abstrak ≤1 hal, TNR 10 pt, 1 spasi, dua bahasa (Ind+Eng) + Kata kunci**; sampul: judul kapital semua, tanpa gelar, NIM D2xxxx, Program Studi Magister Teknik Sipil, logo Untan segilima Ø 4 cm (bukan bulat).
- **Daftar Istilah/Simbol = praktis wajib** di tesis ini (banyak simbol: Vs, Va, tc, th, C, Ei, ...) — belum ada.
- Sitasi: pedoman pakai author-year dalam teks (sudah cocok dengan draf).

### 5d. Tata tulis detail yang beda dari draf
- tabel: judul di atas; "Tabel X.Y." bold; tiap kata judul kapital kecuali sambung/depan; **sumber ditulis di kalimat yang merujuk**, BUKAN di bawah tabel ("Sumber: ..." yang naskah lakukan harus diubah);
- gambar: keterangan di bawah, hanya huruf pertama kapital, sumber TNR 10 pt di bawah keterangan;
- nomor halaman: Arab tanpa imbuhan, kanan atas, halaman pertama setiap bab di tengah bawah; ambiguitas pedoman: §2.3 bilang Arab mulai hal. 1 Bab I, contoh Lampiran I memakai Romawi untuk muka-muka — tanyakan ke prodi / ikuti contoh lampiran;
- isi: TNR 12, 1½ spasi, rata kiri (align left) atau justify, margin kiri 4 cm (termasuk 1 cm penjilidan) & 3-3-3;
- kode program (jika ditampilkan): monospace.
- Kesimpulan wajib **paragraf pengantar sebelum butir** (draf BAB V lama sudah punya); kesimpulan HARUS sudah dipaparkan di Bab IV (pedoman §3.2.5).

---

## 6. USULAN STRUKTUR BAB IV–V (keputusan tampil di chat sesi ini; dicatat agar tidak hilang)

**BAB IV — HASIL ANALISIS...**
4.1 Karakteristik kawasan (rekap param + status naskah/data/desain) · 4.2 Data hujan (kompilasi+QC, Uji-t, konsistensi) · 4.3 Frekuensi & R24 (param, 3 dist, Chi², penetapan) · 4.4 tc & IDF Mononobe · 4.5 Debit puncak Rasional + sensitivitas C · 4.6 Hidrolika pipa penyalur (envelope v–td–tc–I–Q–D; pipa unit/talang/bak) · 4.7 Kebutuhan & neraca air (fraksi, pasokan, Rippl → Vs, keandalan) · 4.8 Va & Vdesain = maks(Vs,Va), dimensi prelim · 4.9 Analisis sensitivitas · 4.10 **Pembahasan** (konsilasi Qout-weir, evaporasi, alokasi lahan/FASOS, verifikasi asumsi lapangan) · 4.11 Rekapitulasi + keterbatasan.

**BAB V — KESIMPULAN DAN SARAN** *(per pedoman §3.2.5, bukan Bab VI)*
5.1 paragraf pengantar → kesimpulan **per rumusan masalah 1–4**; 5.2 saran (survei asumsi lapangan, evaporasi data nyata/ERA5, sumber data, dll). Subbab perancangan teknis (jaringan, pompa, RAB/BEP) masuk sebagai bagian perancangan di akhir Bab IV.

---

## 7. DAFTAR TUGAS UNTUK SESI BERIKUTNYA (urutan disarankan)

1. [BLOCKER] Tutup keputusan sumber data (Supadio+ERA5 vs BWSK pipeline) — rekonciliasi naskah & pipeline, satu sumber angka final (flag #4 HANDOFF).
2. Konsolidasi lapisan revisi Bab IV: hilangkan blok "[REVISI ...]"; tempatkan Qout-weir & FASOS sebagai pembahasan (4.10) JANGAN mengganti metode; hitung ulang Ei dengan 646 m²; selesaikan 921,4 vs 876,8.
3. Terapkan keputusan sumber data: satu tabel, satu angka; angka DN900/BWSK vs PVC350/Supadio tidak dibaurkan.
4. [BAB I–III SUDAH FIX] pastikan struktur kembali ke 5-bab pedoman; pindah perancangan+ekonomi → Bab IV; kesimpulan → Bab V (Bag. 5a).
5. Reformat Daftar Pustaka ke standar pedoman; masukkan rujukan tambahan Bab IV.
6. Lengkapi muka-muka: pernyataan (jangan ulang dari skripsi jembatan!), pengesahan, persembahan, kata pengantar, abstrak 2 bahasa, daftar istilah/simbol.
7. Tabel: pindah "Sumber:" ke kalimat yang merujuk; patuhi aturan kapitalisasi judul gambar/tabel.
8. Susun kesimpulan+saran Bab V baru dari pipeline (`hasil_desain.json`), BUKAN dari draf lama.
9. Pindahkan Excel deliverable ke repo; jalankan `verifikasi_excel.py` (WAJIB 0 gagal).
10. Sisihkan/hapus/ganti nama file `Tesis (3).docx` di arsip (masih skripsi Jembatan) supaya tidak dikira tesis.

---

## 8. FILE YANG DIBUAT / DIUBAH SESI INI (hanya ini)

- `manuscript/novelty.md` — BARU (atas permintaan user; penggabungan novelty lama + cek internasional). Dokumen asli **tidak** disentuh.
- `TEMUAN GLM-5.3.md` (file ini) — BARU, di root repo.
