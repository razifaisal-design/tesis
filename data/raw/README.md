# data/raw/ — DATA MENTAH & ARSIP BESAR (~1,2 GB)

Folder ini DI-IGNORE oleh Git (lihat `.gitignore`) agar ukuran repo tetap < 100 MB.
Isinya hanya ada di mesin lokal; environment cloud (Codespaces/Runner) tidak melihat
folder ini.

Isi lokal:

| File/folder | Ukuran | Keterangan |
|---|---|---|
| `Curah_Hujan_Sungai_Ambawang_BWSK_2012-2025.xlsx` | 68 KB | Data mentah curah hujan harian BWSK (sumber `src/build_db.py`) |
| `arsip-tesis-lengkap/` | ~1,2 GB | Arsip proyek tesis lama (proposal v7, draft Bab 4/5, CAD/GIS, jurnal, foto survei). Naskah utamanya sudah disalin ke `manuscript/` |
| `Tata Cara Perhitungan Debit Banjir Rencana.pdf` | 5,2 MB | Referensi perhitungan debit banjir (SNI) |
| `[ABS 3] ROBBY ...xlsx` | 4,6 MB | Berkas akademik referensi |
| `sni2415.txt` | 156 KB | Teks SNI 2415:2016 (analisis frekuensi hidrologi) |
| `tesis_extract/` | kecil | Ekstraksi XML/OMML dari proposal (dipakai verifikasi rumus Tahap 1) |

Catatan: karena file curah hujan mentah hanya 68 KB, salinannya ikut dikomit di
`data/sample/` sehingga seluruh pipeline (termasuk `build_db.py`) bisa dijalankan
penuh di environment cloud.
