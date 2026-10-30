# HANDOFF BAB V TAHAP 1 — Jaringan Distribusi Bertekanan + Pompa

> Dokumen transisi sesi. Master status: [`HANDOFF.md`](HANDOFF.md); peta tahap resmi:
> [`README.md`](README.md). Dokumen ini membingkai **apa yang sudah & belum dikerjakan
> di Bab V Tahap 1**, plus pintu ke Tahap 2 (ekonomi).

## 1. Posisi sekarang

| Bidang | Status terkini |
|---|---|
| Bab IV Tahap 1–5 | SELESAI (naskah + lampiran + 8 grafik + PDF terbit) |
| Tahap 6 (finishing) | PDF naskah + render CAD + housekeeping SELESAI; **keputusan lahan kolam DITUNDA ke asistensi dosen** |
| **Bab V Tahap 1 (dokumen ini)** | **KOMPUTASI SELESAI + TERVERIFIKASI 7.225 cek**; angka memakai **asumsi awal yang BELUM di-asistensi** |
| Bab V Tahap 2 (ekonomi) | belum mulai |

**Keputusan user (30 Okt 2026):** Bab V Tahap 1 dikerjakan **dengan angka awal**
(asumsi jam operasi 8 jam, elevasi bak +2,5 m, dst.) tanpa menunggu asistensi.
Asumsi ditandai eksplisit di `parameter_desain` + sheet `Jaringan_Distribusi`
(sepenuhnya live — bila dosen mengubah asumsi, cukup ubah sel kuning / jalankan
ulang `src/jaringan_distribusi.py`, tanpa menyentuh Bab IV).

## 2. Hasil Bab V Tahap 1 (semua tervalidasi)

| Besaran | Nilai | Keterangan |
|---|---|---|
| Q kebutuhan desain | 49,92 m³/hari | fraksi 0,65 × 76,8 m³/hari (link sheet Kawasan) |
| Q pompa | **6,24 m³/jam** (1,733 l/dtk) | ÷ 8 jam operasi (ASUMSI) |
| Lift statis + tekanan sisa | 5,00 m | elev bak +2,5 − muka air −0,5 + sisa 2,0 m |
| Los gesek jalur terburuk | 15,72 m | Hazen-Williams PVC C=140, L = 341,8 m (jalur) |
| H kerja | **22,29 m** | + rugi minor 10% (1,57 m) |
| H pompa terpilih | **28 m** | margin 20%, pembulatan 2 m |
| Daya | P_shaft 688 W → motor **740 W** | η = 0,55 (ASUMSI katalog) |
| Unit pompa | **2** (1 aktif + 1 cadangan) | sentrifugal permukaan, rumah pompa di FASOS |
| Pipa | suction DN63 → induk **DN32** (10×33 m) → lateral **DN25** ×5 → sambungan DN25 ×160 | kriteria v 0,6–1,5 m/s |
| L total pipa | **431,8 m** | |

## 3. Artefak sesi ini

```
src/jaringan_distribusi.py            # mesin desain jaringan+pompa (baca DB -> DB + JSON)
data/processed/hasil_jaringan.json    # hasil terverifikasi (TER-COMMIT)
data/processed/hidrologi.db           # tabel BARU: jaringan_distribusi (13 segmen), pipa_tekan;
                                      # 19 baris parameter_desain baru (asumsi + spes pompa)
tools/buat_excel.py                   # sheet 15 Jaringan_Distribusi (formula hidup silang-sheet)
tools/verifikasi_excel.py             # +73 cek sheet jaringan vs DB/JSON -> LULUS 7.225
tools/buat_gambar_bab5.py             # -> figures/gambar5-1.png (diagram skematik),
                                      #    figures/gambar5-2.png (profil los gesek)
```

Sheet `Jaringan_Distribusi` (workbook 16 sheet): parameter asumsi = sel kuning
bisa diubah → Q, DN, v, hf, H kerja, daya, cek status menghitung ulang live
(formula Hazen-Williams per segmen, bukan nilai tempel).

## 4. Asumsi yang BELUM di-asistensi (minta persetujuan dosen)

1. **jam_operasi_pompa = 8 jam/hari** — menentukan Q pompa & semua DN.
2. **elev_bak_unit = +2,5 m** (tandon 0,5 m³ di tower tipe 36).
3. **tekanan_sisa_min = 2,0 m** di unit terjauh.
4. **eta_pompa = 0,55** (katalog sentrifugal kecil) → daya motor.
5. **Layout:** induk 330 m mengikuti jalan utama, 5 lateral (lebar kawasan 85,78 m),
   sambungan 12 m/unit — diturunkan dari siteplan, bukan survei.
6. **Lateral = 12,5% Q per baris blok** (pembagian merata 5 baris) — idealnya
   diverifikasi unit count per blok di lapangan.

Konsekuensi bila asumsi berubah: jalankan `python src/jaringan_distribusi.py` →
`python tools/buat_excel.py` → `python tools/verifikasi_excel.py` (WAJIB LULUS) →
`python tools/buat_gambar_bab5.py`. Bab IV TIDAK berubah (jaringan tidak
mempengaruhi neraca/kolam/hidrolika induk).

## 5. Quick start

```bash
git status -sb          # harus bersih & sinkron origin/main
source .venv/bin/activate
python tools/verifikasi_excel.py    # harus LULUS (7.225 cek, 0 gagal)
```

Catatan LibreOffice: `tools/recalc_excel.py` melewati bila soffice tidak ada
(workbook tetap valid; Excel recalc saat dibuka). Bila butuh baked values:
mount SSD Lexar (atau install LibreOffice) lalu jalankan `recalc_excel.py`.

## 6. Misi Tahap 2 — Ekonomi teknik (RAB, operasional, retribusi, BEP)

Lingkup awal (usulan; sesuaikan dengan dosen):

1. **RAB investasi:** pompa (2 unit + cadangan), pipa (per DN & total L),
   bak/bangunan rumah pompa, instalasi. Harga material → tabel baru
   `harga_satuan` di DB (sumber: harga pasar Pontianak, tanggal + URL foto
   toko dicatat sebagai sumber).
2. **Biaya operasional tahunan:** listrik pompa (740 W × 8 jam × 365 hari ×
   tarif PLN terkin), perawatan pipa/pompa, gaji operator (opsional).
3. **Retribusi:** tarif per m³ ke warga (mis. ikut/PDAM benchmark) × volume
   tahunan pada fraksi 65%.
4. **BEP:** volume/tahun & tahun balik modal; analisis sensitivitas tarif
   (mis. 3 skenario).
5. **Deliverable:** `src/analisis_ekonomi.py` → tabel `ekonomi` + JSON →
   sheet `Ekonomi` (formula hidup) → cek di `verifikasi_excel.py` →
   gambar5-3 (BEP/sensitivitas) → naskah Bab V (docx, Pedoman Untan, angka
   dari DB, ikuti pola `tools/buat_bab5_docx_baru.py`).

## 7. Definisi selesai Bab V ( Tahap 1–3 )

1. Tahap 1: **SELESAI** (dokumen ini) — asumsi disepakati dosen (butir §4) atau
   diverifikasi, naskah subbab jaringan+pompa ditulis.
2. Tahap 2: RAB/operasional/retribusi/BEP tervalidasi + naskah ekonomi.
3. Tahap 3: dashboard web lokal (pipeline + test suite dari verifikasi) —
   opsional sesuai kesepakatan awal.

## 8. Jangan dilakukan

- Jangan mengubah sheet `Jaringan_Distribusi` secara manual tanpa lewat
  `src/jaringan_distribusi.py` (DB & JSON = sumber kebenaran).
- Jangan mencampur angka Bab IV (Q puncak 0,8862 m³/dtk, kolam 72,5 m) dengan
  asumsi jaringan — itu sistem gravitasi masuk; ini distribusi bertekanan keluar.
- Jangan menghapus tabel `jaringan_distribusi`/`pipa_tekan` tanpa menjalankan
  ulang skripnya (akan hilang bila `build_db.py` dijalankan — jalankan ulang
  `jaringan_distribusi.py` setelah rebuild).
