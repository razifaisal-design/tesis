#!/usr/bin/env python3
"""Generator naskah BAB III METODOLOGI (revisi) — docx.

Menerapkan revisi wajib pada REVISI.md (9 butir): sumber hujan BWSK 2012-2025,
variabel iklim NOAA ISD Supadio + NASA POWER, evaporasi Penman muka air + hujan
langsung kolam (tanpa istilah ET0/E0), data hilang 12 hari NULL, uji homogenitas
2 arah alpha=5%, chi-kuadrat bin menjumlah 1 (0,50/0,20/0,10/0,06/0,14) + E>=5,
justifikasi T=10, dan hidrolika pipa kontinu (atap->kolam gravitasi, kolam->warga
pompa).

Output: manuscript/BAB_III_REVISI.docx
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from naskah_util import (ROOT, setup_doc, para, heading, subheading, bullet,
                         caption_table, table, P, set_run, n, ni, rup,
                         VAL, DES, KOL, HID)

OUT = ROOT / "manuscript" / "BAB_III_REVISI.docx"
doc = setup_doc()

# ================================================================== JUDUL
p = P(doc, align=0, before=0, after=2)
set_run(p.add_run("BAB III"), bold=True)
p.paragraph_format.alignment = 1
p = P(doc, align=1, after=4)
set_run(p.add_run("METODOLOGI"), bold=True)

# ------------------------------------------------------------------ 3.1
heading(doc, "3.1", "Jenis Penelitian")
para(doc,
     "Studi ini dikategorikan sebagai studi dengan pendekatan metode kuantitatif. "
     "Data curah hujan historis diolah secara statistik untuk menentukan intensitas "
     "curah hujan rencana dan selanjutnya digunakan dalam perhitungan debit limpasan "
     "permukaan. Pemodelan hidrolika memanfaatkan prinsip-prinsip kuantitatif untuk "
     "mendesain dimensi optimal sistem drainase dan kolam retensi berdasarkan volume "
     "tampungan yang dibutuhkan. Analisis dilakukan pada satu basis data terpadu "
     "(SQLite) yang menjadi sumber kebenaran seluruh angka, sehingga setiap keluaran "
     "dapat ditelusuri, dihitung ulang, dan divalidasi silang terhadap berkas kerja "
     "spreadsheet. Dengan demikian, data numerik dan analisis statistik menjadi "
     "fondasi dalam menghasilkan spesifikasi teknis perancangan.")

# ------------------------------------------------------------------ 3.2
heading(doc, "3.2", "Lokasi Perencanaan")
para(doc,
     "Perencanaan ini berfokus pada kawasan perumahan Rajawali Residence yang berada "
     "di Jalan Wonodadi 2, Kecamatan Sungai Raya, Kabupaten Kubu Raya, sebagaimana "
     "ditunjukkan pada Gambar 3.1. Kawasan perumahan ini terdiri atas 160 unit "
     "residensial dengan tipologi bangunan tunggal Tipe 36, dengan luas kawasan "
     "2,88 hektar (28.800 m\u00b2) dan luas atap rata-rata 65 m\u00b2 per unit "
     "(total 10.400 m\u00b2 atau 36,1% luas kawasan). Perancangan sistem dilakukan "
     "berdasarkan data dan analisis tersebut.")
para(doc, "Gambar 3.1 Lokasi Perencanaan", align=1, italic=True)
para(doc, "Gambar 3.2 Siteplan", align=1, italic=True)

# ------------------------------------------------------------------ 3.3
heading(doc, "3.3", "Data dan Alat yang Dibutuhkan")
subheading(doc, "3.3.1", "Data Primer")
para(doc, "Data primer yang wajib dikumpulkan dalam studi perencanaan ini meliputi:")
bullet(doc, "Dimensi saluran drainase eksisting (lebar dan tinggi saluran), "
            "diperoleh melalui pengukuran langsung di lapangan menggunakan meteran.")
bullet(doc, "Elevasi/beda tinggi antara titik talang atap dan titik rencana kolam "
            "retensi, diperoleh melalui pengukuran langsung menggunakan waterpass.")
bullet(doc, "Dokumentasi kondisi eksisting kawasan, diperoleh melalui pemotretan "
            "langsung di lapangan.")

subheading(doc, "3.3.2", "Data Sekunder")
para(doc, "Data sekunder yang wajib dikumpulkan dalam studi perencanaan ini meliputi:")
bullet(doc,
       "Data curah hujan harian dari Stasiun BWSK Sungai Ambawang periode 2012\u20132025 "
       "(14 tahun). Data ini dipakai untuk menyusun hujan harian maksimum tahunan, "
       "uji homogenitas, uji konsistensi, analisis frekuensi, dan neraca air bulanan. "
       "Panjang data 14 tahun dipilih dengan pertimbangan bahwa SNI 2415:2016 "
       "\u00a74.2.1 menyarankan panjang data lebih dari 20 tahun, sedangkan pedoman "
       "perencanaan Direktorat Jenderal Cipta Karya mensyaratkan minimum 10 tahun; "
       "dengan demikian 14 tahun memenuhi syarat minimum pedoman perencanaan. Data "
       "harian Stasiun Meteorologi Supadio tidak dipakai untuk hujan rencana karena "
       "arsip hariannya tidak tersedia secara utuh di repositori penelitian.")
bullet(doc,
       "Data iklim untuk perhitungan evaporasi kolam (suhu udara, kelembapan relatif, "
       "kecepatan angin, dan tekanan udara) dari arsip Integrated Surface Database "
       "(ISD) NOAA Stasiun Supadio (WMO 96581) periode 2012\u20132025, serta radiasi "
       "matahari (Rs) dari NASA POWER (produk CERES). NASA POWER merupakan produk "
       "satelit/reanalisis, bukan pengamatan stasiun; penggunaannya dinyatakan secara "
       "eksplisit dan polanya diverifikasi konsisten terhadap pola musiman iklim "
       "setempat. Data iklim ini dipakai untuk menghitung evaporasi muka air dengan "
       "metode Penman (1948).")
bullet(doc,
       "Siteplan dan gambar teknis kawasan perumahan, diperoleh dari pengembang "
       "Rajawali Residence.")
bullet(doc,
       "Standar dan pedoman teknis, meliputi SNI 03-7065-2005, SNI 2415:2016, "
       "koefisien kekasaran Manning, dan pedoman perencanaan drainase/kolam retensi.")
para(doc,
     "Pengendalian mutu data hujan dilakukan dengan aturan tertulis. Nilai yang "
     "bertanda meragukan atau tidak konsisten dengan akumulasi sub-harian ditolak. "
     "Hari tanpa data dibiarkan kosong (NULL) dan tidak diisi dengan nilai sintetis, "
     "sejalan dengan SNI 2415:2016 \u00a74.2.3 (data kosong tidak perlu dilakukan "
     "pengisian data) dan WMO-168 \u00a79.7.2 (hindari pengisian data sintetis). Pada "
     "seri 2012\u20132025 terdapat 12 hari tanpa data (0,23%).")

subheading(doc, "3.3.3", "Alat yang Dibutuhkan")
para(doc, "Alat-alat yang digunakan dalam penelitian ini meliputi:")
bullet(doc, "Perangkat keras (hardware): komputer/laptop untuk pengolahan data dan "
            "penyusunan laporan, serta peralatan survei (meteran, alat tulis, kamera).")
bullet(doc, "Perangkat lunak (software): pengolah data spreadsheet (Microsoft Excel) "
            "untuk berkas kerja berformula hidup; bahasa pemrograman Python beserta "
            "pustaka analisis data (pandas, numpy, matplotlib) dan basis data SQLite "
            "sebagai sumber kebenaran; serta perangkat lunak desain teknik "
            "Computer-Aided Design (CAD/AutoCAD) untuk gambar perancangan.")

# ------------------------------------------------------------------ 3.4
heading(doc, "3.4", "Analisis Data")
para(doc,
     "Tahapan analisis dalam perancangan ini dilakukan untuk membuat desain sistem "
     "perpipaan beserta fasilitas pendukung, dengan mempertimbangkan berbagai aspek "
     "tambahan seperti faktor keselamatan.")
bullet(doc,
       "Analisis hidrologi bertujuan menentukan besaran debit limpasan yang masuk ke "
       "sistem yang direncanakan. Proses dimulai dengan evaluasi data curah hujan, "
       "meliputi uji homogenitas (Uji-t dua arah pada \u03b1 = 5%), uji konsistensi "
       "(deviasi kumulatif), analisis frekuensi, dan penentuan intensitas curah hujan "
       "rencana kala ulang 10 tahun. Uji kecocokan Chi-Kuadrat dilakukan dengan lima "
       "kelas yang dibatasi hujan rencana kala ulang 2, 5, 10, dan 25 tahun, dengan "
       "peluang kelas yang menjumlah satu (0,50; 0,20; 0,10; 0,06; dan 0,14) dan "
       "syarat frekuensi harapan E \u2265 5 dipenuhi melalui penggabungan kelas. "
       "Debit inflow dihitung dengan Metode Rasional dan intensitas hujan diperoleh "
       "melalui konversi curah hujan harian maksimum menggunakan metode Mononobe. "
       "Debit inflow selanjutnya menjadi dasar perencanaan dimensi pipa dan kapasitas "
       "tampungan kolam retensi.")
bullet(doc,
       "Analisis hidrolika mencakup penentuan dimensi pipa (koefisien Manning, "
       "kemiringan, geometri penampang basah), kapasitas aliran maksimum, tinggi "
       "jagaan (freeboard), dan perencanaan kolam tampungan. Untuk keperluan "
       "perancangan awal, pipa diperlakukan sebagai pipa kontinu yang dialiri penuh "
       "dengan kemiringan tetap; kehilangan energi di ujung pipa dan gesekan lokal "
       "ditinjau pada tahap teknis lanjutan. Bangunan pelimpah (overflow) direncanakan "
       "untuk mengendalikan muka air maksimum pada kolam agar sistem tetap aman pada "
       "kondisi hujan ekstrem.")
bullet(doc,
       "Analisis ekonomi teknik meliputi penyusunan Rencana Anggaran Biaya (RAB) "
       "sebagai biaya investasi awal, estimasi biaya operasional dan pemeliharaan, "
       "serta analisis potensi pendapatan dari retribusi air hujan, untuk menentukan "
       "titik keseimbangan (Break Even Point) sebagai dasar penilaian kelayakan "
       "investasi dari sudut pandang pengembang.")
bullet(doc,
       "Hasil visual dari perancangan berupa gambar-gambar teknis yang merinci "
       "struktur utama dan bangunan pelengkap pada sistem drainase dan kolam retensi.")

subheading(doc, "3.4.1", "Analisis Kebutuhan Air dan Neraca Air")
para(doc,
     "Tahap ini menjawab kebutuhan penyimpanan air baku kawasan. Kebutuhan air harian "
     "total dihitung dari jumlah unit rumah, rata-rata jumlah penghuni per unit, dan "
     "standar kebutuhan air domestik (Persamaan 3.1):")
para(doc, "Qharian = n_unit \u00b7 n_jiwa \u00b7 q\u2003(3.1)", align=1, italic=True)
para(doc,
     "dengan Qharian = kebutuhan air harian total kawasan (liter/hari), n_unit = "
     "jumlah unit rumah, n_jiwa = rata-rata jumlah penghuni per unit, dan q = standar "
     "kebutuhan air domestik (liter/jiwa/hari).")
para(doc,
     "Selanjutnya disusun neraca air bulanan dengan membandingkan volume pasokan air "
     "hujan (Vsupply) terhadap volume kebutuhan (Vdemand) untuk setiap bulan, "
     "menggunakan Persamaan 2.23 sampai 2.25 pada Bab II. Volume pasokan berasal dari "
     "limpasan atap (C \u00b7 A \u00b7 R) ditambah hujan yang jatuh langsung di permukaan "
     "kolam (P \u00b7 Ap). Dari neraca kumulatif tersebut, volume kebutuhan penyimpanan "
     "(Vs) ditentukan sebagai selisih antara tampungan kumulatif tertinggi dan "
     "terendah (Persamaan 2.26), yang secara grafis diperoleh melalui metode kurva "
     "massa (diagram Rippl). Keandalan sistem dievaluasi sebagai persentase bulan yang "
     "kebutuhannya terpenuhi sepenuhnya (Persamaan 2.27).")
para(doc,
     "Karena air hujan dibatasi untuk kebutuhan non-potabel (Subbab 2.1), neraca air "
     "dihitung untuk beberapa fraksi kebutuhan yang dilayani (100%, 70%, 65%, 60%, dan "
     "50%) dengan fraksi desain 65%, yaitu titik tengah rentang 60\u201370% kebutuhan "
     "non-potabel; batas bawah 50% mengacu pada Vovk dkk. (2023).")
para(doc,
     "Evaporasi permukaan kolam dihitung dengan metode Penman (1948) untuk muka air "
     "terbuka, bukan dengan pendekatan evapotranspirasi acuan rumput. Sehubungan "
     "dengan itu, istilah yang dipakai pada naskah ini adalah \u201cevaporasi\u201d dan "
     "bukan \u201cET0\u201d atau \u201cE0\u201d. Karena luas permukaan kolam (Ap) "
     "memengaruhi besarnya evaporasi dan hujan langsung yang masuk, sedangkan volume "
     "kolam (Vs) menentukan Ap, maka Ap dan Vs saling bergantung; keduanya diselesaikan "
     "secara iteratif sampai mencapai titik tetap.")

subheading(doc, "3.4.2", "Perhitungan Debit Limpasan Rencana (Q)")
para(doc,
     "Debit limpasan dihitung dengan Metode Rasional sesuai Persamaan 2.22:")
para(doc, "QT = 0,278 \u00b7 C \u00b7 I \u00b7 A\u2003(3.2)", align=1, italic=True)
para(doc,
     "dengan QT = debit rencana (m\u00b3/detik), C = koefisien pengaliran sesuai "
     "material atap, I = intensitas hujan (mm/jam) dari Persamaan 2.18, dan A = luas "
     "total atap (km\u00b2).")
para(doc,
     "Kala ulang hujan rencana ditetapkan T = 10 tahun. Penetapan ini bersifat "
     "konservatif dan dipertanggungjawabkan melalui beberapa dasar: (a) pedoman "
     "perencanaan drainase Direktorat Jenderal Cipta Karya menetapkan kala ulang "
     "sekitar 2 tahun untuk daerah tangkapan berukuran kecil (kurang dari 10 ha), "
     "sehingga T = 10 tahun berada di sisi aman; (b) Tata Cara Perencanaan Kolam "
     "Retensi mengarahkan pemilihan kala ulang berdasarkan tingkat risiko yang "
     "diterima; (c) praktik penelitian kolam retensi kawasan permukiman (antara lain "
     "studi Bangkinang dan Roy dkk., 2019) memakai kala ulang pada kisaran ini; dan "
     "(d) rumus risiko r = 1 \u2212 (1 \u2212 1/T)^n menunjukkan bahwa untuk T = 10 tahun "
     "dengan umur layan n = 20 tahun, peluang terjadinya paling sedikit satu kejadian "
     "hujan yang menyamai atau melampaui hujan rencana adalah sekitar 87,8%.")

subheading(doc, "3.4.3", "Penentuan Volume Kolam Retensi (Kriteria Ganda)")
para(doc,
     "Sesuai fungsi ganda kolam sebagai reservoir air baku dan sarana atenuasi "
     "limpasan, volume kolam ditentukan berdasarkan dua kriteria. Kriteria pertama "
     "adalah volume kebutuhan penyimpanan (Vs) dari analisis neraca air (Subbab 3.4.1). "
     "Kriteria kedua adalah volume atenuasi limpasan (Va) yang dihitung dari akumulasi "
     "debit puncak selama durasi hujan efektif (Persamaan 2.30 dan 2.31 pada Bab II). "
     "Volume desain kolam ditetapkan sebagai nilai terbesar di antara keduanya "
     "(Persamaan 2.32 pada Bab II), sehingga kolam mampu memenuhi kedua fungsi "
     "sekaligus. Durasi hujan efektif th pada Persamaan 2.31 ditetapkan sebagai "
     "kriteria desain sebesar 1 jam dan diuji sensitivitasnya pada 0,5 sampai 3 jam. "
     "Dimensi geometri kolam, tinggi jagaan, dan bangunan pelimpah (overflow) kemudian "
     "ditentukan berdasarkan volume desain tersebut, dengan mempertimbangkan bahwa "
     "kolam dirancang kedap (lined) mengingat kondisi tanah gambut di kawasan studi.")

subheading(doc, "3.4.4", "Perhitungan dan Verifikasi Dimensi Pipa")
para(doc,
     "Diameter teoritis pipa dihitung menggunakan Persamaan Manning untuk kondisi "
     "aliran penuh (full flow) agar memiliki faktor aman.")
para(doc, "D = (4 \u00b7 Q \u00b7 n / (\u03c0 \u00b7 S^0,5))^(3/8)\u2003(3.3)",
     align=1, italic=True)
para(doc,
     "Diameter teoritis (D) dibulatkan ke atas ke ukuran pipa standar yang tersedia "
     "di pasaran. Setelah diameter komersial (Dkomersial) dipilih, kecepatan aliran "
     "aktual di dalam pipa diverifikasi untuk memastikan kinerja yang baik:")
para(doc, "V = Qrencana / Apipa\u2003(3.4)", align=1, italic=True)
para(doc,
     "dengan V = kecepatan aliran (m/detik), Qrencana = debit rencana pada pipa "
     "(m\u00b3/detik), dan Apipa = luas penampang pipa (m\u00b2).")
para(doc,
     "Pada tahap perancangan ini, pipa diperlakukan sebagai pipa kontinu dengan "
     "kemiringan tetap; skema aliran adalah gravitasi untuk jalur atap menuju kolam, "
     "sedangkan jalur kolam menuju rumah warga dilayani dengan pompa. Perancangan "
     "jaringan pipa distribusi bertekanan dan pemilihan pompa dilakukan pada tahap "
     "perancangan teknis lanjutan, sedangkan Bab IV memuat analisis hidrologi, neraca "
     "air, dan penentuan dimensi kolam serta pipa penyalur.")

subheading(doc, "3.4.5", "Perhitungan Break Even Point (BEP)")
para(doc,
     "Perhitungan Break Even Point (BEP) digunakan untuk mengetahui jangka waktu yang "
     "diperlukan agar investasi awal dapat kembali melalui keuntungan bersih yang "
     "dihasilkan sistem. Analisis BEP dilakukan dengan pendekatan waktu pengembalian "
     "modal (Payback Period), yaitu membandingkan total investasi awal terhadap "
     "keuntungan bersih per tahun. Keuntungan bersih diperoleh dari selisih antara "
     "total pendapatan retribusi air hujan dan total biaya operasional tahunan. Hasil "
     "perhitungan BEP selanjutnya disajikan dalam bentuk tabel kumulatif dan "
     "divisualisasikan dalam grafik hubungan antara biaya dan pendapatan terhadap "
     "waktu, sehingga dapat ditentukan titik pertemuan antara total biaya dan total "
     "pendapatan sebagai titik BEP (Persamaan 3.5).")
para(doc, "BEP = Investasi awal / Keuntungan bersih per tahun\u2003(3.5)",
     align=1, italic=True)

# ------------------------------------------------------------------ 3.5
heading(doc, "3.5", "Bagan Alir Perancangan")
para(doc,
     "Tahapan penelitian ini digambarkan pada bagan alir perancangan (Gambar 3.3), "
     "mulai dari pengumpulan data primer dan sekunder, pengendalian mutu data, "
     "analisis hidrologi (uji homogenitas dan konsistensi, analisis frekuensi, "
     "penetapan hujan rencana), perhitungan intensitas dan debit rencana, analisis "
     "neraca air dan penentuan volume kolam, verifikasi dimensi pipa, hingga "
     "perancangan teknis dan analisis kelayakan ekonomi.")
para(doc, "Gambar 3.3 Bagan Alir Perancangan", align=1, italic=True)

doc.save(OUT)
print("Tersimpan:", OUT.relative_to(ROOT), f"({OUT.stat().st_size:,} bytes)")
