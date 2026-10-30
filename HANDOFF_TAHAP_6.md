# HANDOFF TAHAP 6 — Sesi Berikutnya (Finishing Naskah & Transisi Bab V)

> Dokumen transisi sesi. Master status: [`HANDOFF.md`](HANDOFF.md); peta tahap resmi:
> [`README.md`](README.md). Dokumen ini membingkai **apa yang dikerjakan di Tahap 6**.

## 1. Posisi sekarang (hasil sesi 1–5)

| Peta tahap | Status terkini |
|---|---|
| Bab IV Tahap 1 (fondasi OMML + DB) | SELESAI |
| Bab IV Tahap 2 (mesin desain + Excel + verifikasi) | SELESAI (kini **7.152 cek**, rantai Penman live di workbook) |
| Bab IV Tahap 3 (grafik) | SELESAI — `figures/gambar4-1..8.png` (dikerjakan bersama Tahap 5) |
| Bab IV Tahap 4 (sensitivitas + pembahasan) | SELESAI — Subbab 4.9 & 4.10 |
| Bab IV Tahap 5 (naskah Bab 4 + lampiran) | **NASKAH SELESAI**: `manuscript/BAB_IV_HASIL_DAN_PEMBAHASAN.docx`, `LAMPIRAN_BAB_IV.docx`, plus `BAB_III_REVISI.docx`, `BAB_V_KESIMPULAN.docx` |
| Bab V Tahap 1–3 (distribusi+pompa / ekonomi / dashboard) | belum mulai |

Repo bersih & ter-push (branch `main`, private). Artefak sesi 5 (naskah docx,
8 grafik, `tools/buat_grafik.py`, `buat_bab3/4/5_docx.py`, `naskah_util.py`,
`kirim_telegram.py`, pembaruan HANDOFF/REVISI) **ikut ter-commit pada akhir sesi ini**
sebelum handoff dibuat — pastikan `git status` bersih saat mulai Tahap 6.

## 2. Misi Tahap 6 — sisa pekerjaan yang belum selesai

Diurutkan berdasarkan bagian "Sisa pekerjaan" di `HANDOFF.md`:

1. **Ekspor PDF naskah** (butuh LibreOffice — saat ini TER-MOUNT di
   `/Volumes/Lexar/APPS/LibreOffice.app`):
   ```bash
   SOF=/Volumes/Lexar/APPS/LibreOffice.app/Contents/MacOS/soffice
   for f in manuscript/BAB_III_REVISI.docx manuscript/BAB_IV_HASIL_DAN_PEMBAHASAN.docx \
            manuscript/LAMPIRAN_BAB_IV.docx manuscript/BAB_V_KESIMPULAN.docx; do
     "$SOF" --headless --norestore --convert-to pdf --outdir manuscript "$f"
   done
   ```
   (PDF ikut di-commit — aturan `!manuscript/*.pdf` sudah ada.) Jika SSD tidak
   ter-mount, cek `soffice` di PATH atau minta user mount dulu.
2. **Render ulang gambar CAD** — `sket_lengkap.pdf/.png` di
   `data/raw/arsip-tesis-lengkap/03_Desain_CAD_dan_Peta/` (folder di-ignore Git)
   belum diperbarui setelah sinkron `sket_lengkap.dxf`. Opsi: minta user export
   ulang dari AutoCAD, atau render DXF→PNG/PDF (mis. `ezdxf` + matplotlib) lalu
   simpan hasilnya ke `figures/` agar ter-commit.
3. **Rekonsiliasi lahan kolam (butuh keputusan user)** — Ap rencana 5.256,25 m²
   vs lahan FASOS 814 m². Siapkan dulu analisis pendukung sebelum bertanya:
   - skenario memakai lahan 814 m²: berapa `he` minimum agar `V >= Vs` (814 × he;
     Vs kini jauh lebih besar dari era lama — hitung angka pasti dari
     `hasil_desain.json`), opsi kolam terdistribusi, opsi fraksi kebutuhan lebih
     rendah (lihat reliability per fraksi di workbook/DB);
   - bawa angka + 2–3 opsi ke user untuk diputuskan, lalu ikuti konsekuensinya
     (workbook/DB **tidak diubah** sebelum keputusan disepakati).
4. **Verifikasi lapangan (untuk user)** — survei/waterpass: Lo = 8 m, S_atap = 30%,
   S_pipa = 0,30%, he = 3 m. Siapkan checklist koordinat/lokasi pengukuran.
5. **Housekeeping** — hapus lock `~$oposal Tesis (claude) (Revisi Antigravity) 2.docx`
   (pastikan Word tertutup), pastikan `git status` bersih, README sudah diperbarui
   pada sesi ini (cek lagi bila ada perubahan peta tahap).
6. **Setelah 1–5 beres** → buka **Bab V Tahap 1: jaringan distribusi bertekanan +
   pompa** (lingkup awal: layout jaringan dari kolam ke unit, perhitungan tekanan/los,
   pemilihan pompa debit-head, masuk tabel `parameter_desain` + skrip baru di `src/`).

## 3. Dikerjakan USER (bukan tugas agent — jangan dikerjakan sendiri)

- **Daftar Pustaka** — reformat lewat Mendeley (keputusan user).
- **Muka-muka naskah** — pernyataan orisinalitas, halaman pengesahan, abstrak
  2 bahasa, daftar istilah/simbol.
- **Verifikasi lapangan fisik** (butir 4 di atas).

## 4. Quick start

```bash
git status -sb          # harus bersih & sinkron origin/main
python -m venv .venv && source .venv/bin/activate   # bila env baru
pip install -r requirements.txt
python tools/verifikasi_excel.py                    # harus LULUS (regresi baseline)
```

Sumber angka naskah/keluaran: `data/processed/` (DB + JSON + workbook terverifikasi).
Perubahan apa pun pada input → pipeline penuh + `verifikasi_excel.py` sampai LULUS.

## 5. Definisi selesai (Tahap 6)

1. PDF naskah (Bab III, Bab IV, Lampiran, Bab V) tersedia di `manuscript/` dan ter-commit.
2. Gambar CAD ter-render ulang & tersimpan (minimal di `figures/` atau arsip lokal
   sesuai keputusan).
3. Keputusan alokasi lahan kolam terdokumentasi (angka + opsi + pilihan user) di
   `HANDOFF.md` — bila berdampak ke desain, pipeline dijalankan ulang + verifikasi.
4. `git status` bersih, semua terpush; handoff Tahap 7 disiapkan (isi ringkas di
   `HANDOFF.md` bagian peta tahap).
