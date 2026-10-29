# Penman (1948) — Tabel 6: Variasi Musiman Evaporasi Relatif

**Sumber asli:** H. L. Penman (1948), *Natural Evaporation from Open Water, Bare Soil and Grass*, Proceedings of the Royal Society of London A, 193(1032), 120–145 — Tabel 6, hlm. 137.
DOI: 10.1098/rspa.1948.0037

**Satuan:** inci/hari (1 in./hari = 25,4 mm/hari)

**Simbol:**

- `E0` — evaporasi muka air terbuka (silinder 0).
- `E_B/E0` — rasio evaporasi tanah gundul (silinder 45B) terhadap muka air.
- `E_T/E0` — rasio evaporasi rumput/turf (silinder 16T) terhadap muka air.
- `E_MO` — laju evaporasi harian rata-rata tangki MO (muka air terbuka), hanya tersedia untuk 1945.

## Tabel 6

| Periode 1944 | E0 (in./hari) | E_B/E0 | E_T/E0 | Periode 1945 | E0 (in./hari) | E_B/E0 | E_T/E0 | E_MO (in./hari) |
|---|---:|---:|---:|---|---:|---:|---:|---:|
| Feb. | — | — | — | 8 Feb.–4 Mar. | 0,04 | 0,78 | 0,31 | — |
| Mar. | — | — | — | 5 Mar.–7 April | 0,06 | 1,10 | 0,86 | 0,06 |
| April | — | — | — | 8–30 April | 0,10? | 1,05? | 0,92? | 0,10 |
| 9 May–1 June | 0,18 | 0,91 | 0,83 | 4–25 May<br>28 May–9 June | 0,11 | 0,89 | 0,69 | 0,11 |
| 2–28 June | 0,19 | 0,98 | 0,88 | 10–22 June<br>23 June–2 July | 0,16 | 0,83 | 0,72 | 0,12 |
| 29 June–4 Aug. | 0,16 | 0,82 | 0,89 | 3–12 July<br>16 July–8 Aug. | 0,17 | 0,84 | 0,71 | 0,14 |
| 5 Aug.–2 Sept. | 0,19 | 0,81 | 0,78 | 12 Aug.–2 Sept. | 0,11 | 0,87 | 0,96 | 0,08 |
| 5–30 Sept. | 0,10 | 0,91 | 0,79 | 6–15 Sept.<br>16–24 Sept. | 0,09 | 0,61 | 0,61 | 0,07 |
| 1–10 Oct. | 0,05 | 0,65 | 0,48 | 25 Sept.–22 Oct. | 0,07 | 0,70 | 0,64 | 0,06 |
| 20 Oct.–6 Nov. | 0,03 | 0,54 | 0,0 | 1–28 Nov. | 0,03 | 0,7? | 0,6 | 0,02 |
| 7–13 Nov. | — | — | — | 29 Nov.–22 Dec. | 0,05 | — | −0,0 | 0,05 |
| 20–30 Nov. | — | — | — | | | | | |
| 1–22 Dec. | 0,01 | 0,8 | −0,4 | | | | | |

## Catatan pembacaan

- `—` berarti tidak ada data/tidak dihitung; `?` berarti nilai diragukan sebagaimana dicetak pada sumber; `−0,0` adalah nilai negatif mendekati nol (kondisi kondensasi).
- Baris 1945 dengan dua periode (mis. `4–25 May` dan `28 May–9 June`) digabung oleh kurung kurawal pada tabel asli; satu set nilai berlaku untuk kedua periode.
- Blok 1944 dan 1945 ditempatkan berdampingan hanya untuk menghemat ruang. Periodenya **tidak** berkorespondensi baris-per-baris.
- Notasi desimal diubah dari bentuk asli (`0·18`) menjadi koma (`0,18`) agar konsisten dengan dokumen lain di repositori; angka tidak diubah.

## Kesimpulan Penman yang relevan (hlm. 139)

- Tanah gundul yang terus jenuh: **E_B ≈ 0,9 × E0** sepanjang tahun.
- Rumput dengan pasokan air cukup: **E_T/E0 = 0,6** (musim dingin, Nov–Feb), **0,7** (musim semi/gugur, Mar–Apr dan Sep–Okt), **0,8** (musim panas, Mei–Agu), dan **0,75** untuk setahun penuh.
- Konsekuensinya: **E0 ≈ 1,25–1,33 × E_T**. Evaporasi muka air lebih besar daripada evapotranspirasi rumput, sehingga ET0 tidak boleh dipakai langsung sebagai evaporasi kolam.

## Relevansi untuk tesis ini

- Kode desain sekarang memakai `Ei = ET0 × 1,0 × Ap`; koefisien 1,0 tersebut tidak didukung tabel ini untuk permukaan air.
- Hitung ulang dari data iklim BPS Kubu Raya 2024 memberi ET0 rumput **116,9 mm/bulan** dan E0 muka air (Penman) **149,4 mm/bulan**, dengan rasio **1,28** — konsisten dengan kisaran Penman (1/0,75 ≈ 1,33).
- Rasio Penman berasal dari Rothamsted, Inggris selatan (1944–1945). Untuk Pontianak nilainya harus dihitung ulang dari data lokal, tetapi arah hubungan (ET0 < E0) tetap berlaku.
- Rujukan pendukung: FAO-56 Bab 2 (ET0 untuk rumput vs Penman untuk muka air) dan WMO-No. 8 (pengukuran evaporasi/panci).
