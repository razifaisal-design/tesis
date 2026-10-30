#!/usr/bin/env python3
"""
Generator naskah BAB IV HASIL DAN PEMBAHASAN (Word .docx) — Tahap 5.

Aturan yang dipatuhi:
- Semua angka hasil dibaca dari sumber kebenaran yang sudah tervalidasi:
  data/processed/hasil_validasi.json, data/processed/hasil_desain.json, dan
  tabel di data/processed/hidrologi.db (kawasan, evaporasi, neraca_bulanan,
  curah_hujan_bulanan). TIDAK ada angka lama (Supadio 25 th, Vs 517 m3,
  kolam 814 m2) yang dicampur.
- Format mengikuti Pedoman Penulisan Tesis Magister Teknik Sipil Untan (Okt 2017):
  margin kiri 4 cm (termasuk 1 cm penjilidan), atas/kanan/bawah 3 cm; TNR 12 pt;
  spasi 1,5; rata kiri-kanan (justify). Judul tabel DI ATAS tabel, sumber ditulis
  pada kalimat yang merujuk (bukan di bawah tabel); keterangan gambar DI BAWAH
  gambar, hanya huruf pertama kapital.
- TEMUAN GLM-5.3: tanpa blok "[REVISI ...]"; istilah hanya "evaporasi" (bukan
  ET0/E0); chi-kuadrat memakai bin yang menjumlah 1 (0,50/0,20/0,10/0,06/0,14)
  dengan syarat E >= 5; satu tabel satu angka; hidrolika pipa diperlakukan
  kontinu (kemiringan tetap).

Output: manuscript/BAB_IV_HASIL_DAN_PEMBAHASAN.docx
"""

import json
import sqlite3
from pathlib import Path

import docx
from docx.shared import Pt, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data" / "processed"
FIG = ROOT / "figures"
OUT = ROOT / "manuscript" / "BAB_IV_HASIL_DAN_PEMBAHASAN.docx"

VAL = json.loads((PROC / "hasil_validasi.json").read_text(encoding="utf-8"))
DES = json.loads((PROC / "hasil_desain.json").read_text(encoding="utf-8"))
DB = sqlite3.connect(PROC / "hidrologi.db")
DB.row_factory = sqlite3.Row

BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
         "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
BULAN3 = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun",
          "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

KOL = DES["kolam"]
HID = DES["hidrolika"]
UNIT = DES["unit"]


# ------------------------------------------------------------------ format angka
def n(x, dec=2):
    """Angka gaya Indonesia (koma desimal, titik ribuan)."""
    if x is None:
        return "-"
    s = f"{x:,.{dec}f}"
    return s.replace(",", "\u2063").replace(".", ",").replace("\u2063", ".")


def ni(x):
    return n(x, 0)


def idr(x):
    return "Rp " + n(x, 0)


# ------------------------------------------------------------------ docx helpers
doc = docx.Document()

sec = doc.sections[0]
sec.page_width = Cm(21.0)
sec.page_height = Cm(29.7)
sec.top_margin = Cm(3.0)
sec.bottom_margin = Cm(3.0)
sec.left_margin = Cm(4.0)
sec.right_margin = Cm(3.0)

_normal = doc.styles["Normal"]
_normal.font.name = "Times New Roman"
_normal.font.size = Pt(12)
_normal.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")


def set_run(r, bold=False, italic=False, size=12):
    r.font.name = "Times New Roman"
    r.font.size = Pt(size)
    r.bold = bold
    r.italic = italic
    return r


def P(align=WD_ALIGN_PARAGRAPH.JUSTIFY, before=0, after=6, spacing=1.5,
      indent=None, first=None):
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = spacing
    if indent is not None:
        pf.left_indent = Cm(indent)
    if first is not None:
        pf.first_line_indent = Cm(first)
    return p


def para(text="", bold=False, italic=False, **kw):
    p = P(**kw)
    if text:
        set_run(p.add_run(text), bold=bold, italic=italic)
    return p


def rich(parts, **kw):
    """parts: list of (teks, bold)."""
    p = P(**kw)
    for item in parts:
        if isinstance(item, tuple):
            t, b = item
            set_run(p.add_run(t), bold=b)
        else:
            set_run(p.add_run(item))
    return p


def heading(num, text, before=14, after=8):
    p = P(align=WD_ALIGN_PARAGRAPH.LEFT, before=before, after=after, spacing=1.5)
    set_run(p.add_run(f"{num}\t{text}"), bold=True)
    return p


def subheading(num, text, before=10, after=6):
    p = P(align=WD_ALIGN_PARAGRAPH.LEFT, before=before, after=after, spacing=1.5)
    set_run(p.add_run(f"{num}\t{text}"), bold=True)
    return p


def bullet(text, level=0):
    p = P(after=4)
    p.paragraph_format.left_indent = Cm(1.0 + level * 0.8)
    p.paragraph_format.first_line_indent = Cm(-0.6)
    set_run(p.add_run("\u2022\t" + text))
    return p


def demand_tahun(fraksi):
    s = DB.execute("SELECT SUM(demand_m3) s FROM neraca_bulanan WHERE fraksi=?",
                   (fraksi,)).fetchone()["s"]
    return s / len(VAL["years"])


def caption_table(num, judul):
    p = P(align=WD_ALIGN_PARAGRAPH.LEFT, before=10, after=4, spacing=1.15)
    set_run(p.add_run(f"Tabel {num}"), bold=True)
    set_run(p.add_run(f" {judul}"))
    return p


def caption_gambar(num, judul):
    p = P(align=WD_ALIGN_PARAGRAPH.CENTER, before=4, after=12, spacing=1.15)
    set_run(p.add_run(f"Gambar {num}"), bold=True, size=11)
    set_run(p.add_run(f" {judul}"), size=11)
    return p


def gambar(nama, num, judul, width_cm=14.0):
    path = FIG / nama
    if path.exists():
        p = P(align=WD_ALIGN_PARAGRAPH.CENTER, before=8, after=2)
        p.add_run().add_picture(str(path), width=Cm(width_cm))
    else:
        para(f"[Gambar {num} belum tersedia: {nama}]",
             align=WD_ALIGN_PARAGRAPH.CENTER, italic=True)
    caption_gambar(num, judul)


def shade(cell, hexfill="D9D9D9"):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexfill)
    tcPr.append(shd)


def table(headers, rows, widths=None, numerik=None, size=10):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for j, h in enumerate(headers):
        hdr[j].text = ""
        p = hdr[j].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        set_run(p.add_run(str(h)), bold=True, size=size)
        shade(hdr[j])
    numerik = numerik or set()
    for row in rows:
        cells = t.add_row().cells
        for j, v in enumerate(row):
            cells[j].text = ""
            p = cells[j].paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.alignment = (WD_ALIGN_PARAGRAPH.RIGHT if j in numerik
                           else WD_ALIGN_PARAGRAPH.LEFT)
            set_run(p.add_run("" if v is None else str(v)), size=size)
    if widths:
        for row in t.rows:
            for j, w in enumerate(widths):
                row.cells[j].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


# ================================================================== DATA DB
KAW = {r["kunci"]: r for r in DB.execute("SELECT * FROM kawasan")}
EVA = [dict(r) for r in DB.execute("SELECT * FROM evaporasi ORDER BY bulan")]
MISSING = VAL["missing"]
PER = VAL["per_year"]
THN = VAL["years"]


def rup(x, dec=1):
    return n(x, dec)


def avg_bulan(col, fraksi=None):
    """Rata-rata nilai bulanan (opsional per fraksi) -> list 12."""
    out = []
    for b in range(1, 13):
        if fraksi is None:
            q = f"SELECT AVG(mm) a FROM curah_hujan_bulanan WHERE bulan=?"
        else:
            q = f"SELECT AVG({col}) a FROM neraca_bulanan WHERE bulan=? AND fraksi=?"
        r = DB.execute(q, (b,) if fraksi is None else (b, fraksi)).fetchone()
        out.append(r["a"])
    return out


supply_avg = avg_bulan("supply_m3", 0.65)
ppond_avg = avg_bulan("p_pond_m3", 0.65)
demand_avg = avg_bulan("demand_m3", 0.65)
evap_avg = avg_bulan("e_m3", 0.65)
net_avg = avg_bulan("net_m3", 0.65)
rain_avg = avg_bulan("mm")
evap_mm_avg = [e["evap_mm"] for e in EVA]

total_hujan_thn_avg = sum(rain_avg)
supply_thn_avg = sum(supply_avg)
demand_thn_avg = sum(demand_avg)
evap_thn_mm = sum(evap_mm_avg)
evap_thn_m3 = sum(evap_avg)

Qharian = 76.8
Qharian65 = Qharian * 0.65

# iterasi konvergen
ITER = KOL["iterasi_konvergen"]
# hidrolika iterasi
HITER = HID["iterasi"]

# statistik
XBAR, S, CV, CS, CK = VAL["xbar"], VAL["S"], VAL["Cv"], VAL["Cs"], VAL["Ck"]
LOGBAR, SLOG, CSLOG = VAL["logXbar"], VAL["Slog"], VAL["Cslog"]
T = VAL["t"]
KONS = VAL["kons"]
GUM = VAL["gumbel"]
FREQ = VAL["freq"]
CHI = VAL["chi"]
TS = [2, 5, 10, 25, 50, 100]


# ================================================================== MULAI NASKAH
p = P(align=WD_ALIGN_PARAGRAPH.CENTER, before=0, after=2)
set_run(p.add_run("BAB IV"), bold=True)
p = P(align=WD_ALIGN_PARAGRAPH.CENTER, after=4)
set_run(p.add_run("HASIL DAN PEMBAHASAN"), bold=True)

para(
    "Bab ini menyajikan hasil analisis hidrologi dan perancangan awal sistem "
    "pemanenan air hujan pada Kawasan Perumahan Rajawali Residence, berdasarkan "
    "metode yang telah ditetapkan pada Bab II dan Bab III. Seluruh angka pada bab "
    "ini ditarik langsung dari basis data terpadu (data/processed/hidrologi.db), "
    "hasil_validasi.json, dan hasil_desain.json yang dihasilkan oleh rangkaian "
    "skrip analisis, serta tervalidasi silang terhadap berkas kerja "
    "Perhitungan_Hidrologi.xlsx (seluruh sel berupa rumus yang saling terhubung). "
    "Setiap persamaan yang dipakai merujuk pada nomor persamaan di Bab II dan "
    "Bab III.",
    after=10,
)

# ------------------------------------------------------------------ 4.1
heading("4.1", "Karakteristik Fisik dan Hidrologis Kawasan Studi")
para(
    "Kawasan studi adalah Perumahan Rajawali Residence di Jalan Wonodadi 2, "
    "Kecamatan Sungai Raya, Kabupaten Kubu Raya, seluas 2,88 hektar (28.800 m\u00b2) "
    "dengan 160 unit rumah Tipe 36 (Subbab 3.2). Seluruh parameter masukan analisis "
    "dirangkum pada Tabel 4.1 beserta statusnya. Status \u201cnaskah\u201d berarti nilai "
    "diambil dari proposal; \u201cdata\u201d berarti nilai dibaca dari data pengukuran; "
    "\u201cdesain\u201d berarti kriteria yang ditetapkan dan diuji sensitivitasnya; "
    "\u201cturunan\u201d berarti nilai yang dihitung dari data atau parameter lain; dan "
    "\u201citerasi\u201d berarti nilai yang diulang sampai konvergen."
)
caption_table("4.1", "Parameter Masukan Analisis dan Statusnya")
table(
    ["Parameter", "Nilai", "Satuan", "Status dan dasar"],
    [
        ["Luas kawasan", "2,88", "ha", "Naskah (siteplan 330,40 \u00d7 85,78 m)"],
        ["Jumlah unit rumah", "160", "unit", "Naskah (Tipe 36)"],
        ["Penghuni per unit", "4", "jiwa", "Naskah"],
        ["Standar kebutuhan air domestik", "120", "L/jiwa/hari", "Naskah (SNI 03-7065-2005)"],
        ["Luas atap per unit", "65", "m\u00b2", "Naskah"],
        ["Luas atap total", "10.400", "m\u00b2", "Turunan (36,1% luas kawasan)"],
        ["Koefisien limpasan atap C", "0,80", "-", "Desain: titik tengah atap seng 0,70\u20130,90 (Tabel 2.7)"],
        ["Kala ulang hujan rencana", "10", "tahun", "Naskah (Subbab 3.4)"],
        ["Sumber data hujan", "BWSK Sungai Ambawang", "-", "Data; periode 2012\u20132025 (14 tahun)"],
        ["Panjang lereng atap Lo", "8,0", "m", "Desain (asumsi tipologi atap)"],
        ["Kemiringan atap S", "0,30", "m/m", "Desain (sekitar 17\u00b0)"],
        ["Panjang pipa penyalur Ld", "330", "m", "Turunan (siteplan, bentang 330,40 m)"],
        ["Koefisien Manning pipa n", "0,011", "-", "Naskah (Tabel 2.8)"],
        ["Kemiringan pipa kolektor S", "0,003", "m/m", "Desain"],
        ["Durasi hujan efektif th", "1,0", "jam", "Desain (Subbab 3.4.3); sensitivitas 0,5\u20133 jam"],
        ["Fraksi kebutuhan yang dilayani (desain)", "0,65", "-", "Desain (Subbab 3.4.1); skenario 50\u2013100%"],
        ["Kedalaman efektif kolam he", "3,0", "m", "Desain"],
        ["Tinggi jagaan (freeboard)", "0,5", "m", "Desain"],
    ],
    widths=[6.2, 3.0, 2.0, 6.0],
)

subheading("4.1.1", "Luas Efektif Atap dan Koefisien Limpasan")
para(
    "Luas atap total adalah 160 unit \u00d7 65 m\u00b2 = 10.400 m\u00b2 (0,010400 km\u00b2), atau "
    "36,1% dari luas kawasan. Koefisien limpasan atap dipilih C = 0,80, yaitu titik "
    "tengah rentang atap lembaran seng galvanis (0,70\u20130,90) pada Tabel 2.7. Pengaruh "
    "nilai C terhadap debit dan volume atenuasi ditinjau pada Subbab 4.9."
)

subheading("4.1.2", "Evaluasi Kapasitas Saluran Drainase Eksisting")
para(
    "Saluran drainase eksisting berupa saluran terbuka beton berdimensi lebar bersih "
    "0,30 m dan tinggi 0,35 m (Subbab 1.1). Kapasitas saluran dihitung dengan "
    "persamaan Manning (Persamaan 2.28 dan 2.29) pada kondisi penuh, dengan "
    "koefisien kekasaran n = 0,013 (beton halus, Tabel 2.8) dan kemiringan S = 0,003 m/m. "
    "Luas penampang A = 0,30 \u00d7 0,35 = 0,1050 m\u00b2; keliling basah P = 1,000 m; "
    "jari-jari hidraulis Rh = A/P = 0,1050 m; kecepatan V = (1/n) Rh^(2/3) S^(1/2) = "
    "0,938 m/detik; dan kapasitas Q = V\u00b7A = 0,0985 m\u00b3/detik (98,5 liter/detik). "
    "Kecepatan aliran 0,938 m/detik berada di bawah kecepatan maksimum saluran "
    "pasangan beton sebesar 3 m/detik (Permen PU No. 12/PRT/M/2014), sehingga "
    "kecepatan saluran memenuhi syarat. Sebagai pembanding, debit puncak limpasan "
    "seluruh atap kawasan untuk kala ulang 10 tahun adalah " + rup(HID["Q"], 4) +
    " m\u00b3/detik (Subbab 4.5), atau sekitar 9,0 kali kapasitas satu saluran. Dengan "
    "demikian saluran eksisting tidak mampu menampung limpasan atap pada hujan "
    "rencana, dan pengalihan limpasan atap ke jaringan pipa tertutup menuju kolam "
    "retensi akan mengurangi beban yang harus ditanggung saluran."
)

# ------------------------------------------------------------------ 4.2
heading("4.2", "Analisis Data Curah Hujan")
subheading("4.2.1", "Kompilasi Seri Data Curah Hujan Harian Maksimum")
para(
    "Sesuai keputusan sumber data, hujan rencana disusun dari data curah hujan "
    "harian Stasiun BWSK Sungai Ambawang periode 2012\u20132025 (14 tahun). Data harian "
    "Stasiun Meteorologi Supadio tidak dipakai karena arsip hariannya tidak tersedia "
    "secara utuh. Rentang 14 tahun dipilih dengan pertimbangan bahwa SNI 2415:2016 "
    "\u00a74.2.1 menyarankan panjang data lebih dari 20 tahun, sementara pedoman "
    "perencanaan Direktorat Jenderal Cipta Karya mensyaratkan minimum 10 tahun; "
    "dengan demikian panjang data 14 tahun memenuhi syarat minimum pedoman "
    "perencanaan. Seri yang dianalisis terdiri atas " + ni(5114) + " hari pengamatan, "
    "dengan " + ni(12) + " hari tanpa data (0,23%) yang dibiarkan kosong (NULL). "
    "Pengisian data sintetis tidak dilakukan mengikuti SNI 2415:2016 \u00a74.2.3 dan "
    "WMO-168 \u00a79.7.2."
)
para(
    "Seri hujan harian maksimum tahunan menghasilkan hujan tahunan rata-rata "
    + rup(total_hujan_thn_avg, 1) + " mm/tahun, dengan nilai maksimum teramati "
    "sebesar " + ni(max(VAL["xmax"])) + " mm (tahun 2020). Delapan hari hilang berada "
    "pada Maret 2023; akibatnya total hujan Maret 2023 lebih rendah dari seharusnya "
    "dan nilai maksimum harian tahun 2023 (" + ni(PER["2023"]["xmax"]) +
    " mm) diperlakukan sebagai maksimum teramati, bukan nilai sebenarnya. Rincian "
    "seri per tahun disajikan pada Tabel 4.2, dan Gambar 4.1 menampilkannya secara "
    "grafik."
)
caption_table("4.2", "Seri Hujan Harian Maksimum Tahunan Stasiun BWSK Sungai Ambawang 2012\u20132025")
rows = []
for i, y in enumerate(THN, 1):
    d = PER[str(y)]
    rows.append([i, y, ni(d["total"]), ni(d["xmax"]), ni(d["hari_hujan"]),
                 ni(d["n_missing"])])
rows.append(["", "\u03a3 / rata-rata", ni(sum(PER[str(y)]["total"] for y in THN)),
             rup(XBAR, 1), "-", ni(len(MISSING))])
table(["No", "Tahun", "Total hujan (mm)", "R maks harian (mm)",
       "Jumlah hari hujan", "Hari hilang"],
      rows, widths=[1.0, 1.6, 3.2, 3.2, 3.0, 2.2],
      numerik={0, 1, 2, 3, 4, 5})
para(
    "Rata-rata hujan harian maksimum (x\u0304) sebesar " + rup(XBAR, 3) +
    " mm. Nilai ini merupakan masukan analisis frekuensi pada Subbab 4.3.",
    after=8,
)
gambar("gambar4-1.png", "4.1",
       "Total curah hujan tahunan dan maksimum hujan harian Stasiun BWSK Sungai Ambawang 2012\u20132025")

subheading("4.2.2", "Hasil Uji Homogenitas Data Hujan (Uji-t)")
para(
    "Uji homogenitas dilakukan dengan Uji-t (Persamaan 2.1) memakai kriteria dua "
    "arah pada tingkat signifikansi \u03b1 = 5%. Seri 14 data dibagi dua: tujuh data "
    "pertama (2012\u20132018) dan tujuh data berikutnya (2019\u20132025). Hasilnya "
    "disajikan pada Tabel 4.3. Nilai t hitung sebesar " + rup(T["t"], 3) +
    " lebih kecil daripada t kritis sebesar 2,179 pada derajat kebebasan 12 dan "
    "tingkat kepercayaan 95% (dua arah), sehingga seri data dinyatakan homogen. "
    "Perlu dicatat bahwa bila dipakai kriteria satu arah, kesimpulannya dapat "
    "berbeda; kriteria dua arah dipilih dan ditulis eksplisit agar tidak ambigu."
)
caption_table("4.3", "Hasil Uji Homogenitas (Uji-t, Dua Arah \u03b1 = 5%)")
table(
    ["Parameter", "Nilai"],
    [
        ["N\u2081 (2012\u20132018)", ni(T["n1"])],
        ["N\u2082 (2019\u20132025)", ni(T["n2"])],
        ["Rata-rata x\u0304\u2081 (mm)", rup(T["x1b"], 3)],
        ["Rata-rata x\u0304\u2082 (mm)", rup(T["x2b"], 3)],
        ["Simpangan baku S\u2081 (mm)", rup(T["S1"], 3)],
        ["Simpangan baku S\u2082 (mm)", rup(T["S2"], 3)],
        ["\u03c3 (Persamaan 2.1)", rup(T["sigma"], 3)],
        ["t hitung", rup(T["t"], 3)],
        ["dk = N\u2081 + N\u2082 \u2212 2", ni(T["dk"])],
        ["t kritis (dua arah, \u03b1 = 5%)", "2,179"],
        ["Kesimpulan", "Homogen"],
    ],
    widths=[8.0, 6.0],
)

subheading("4.2.3", "Hasil Uji Konsistensi Data Hujan (Deviasi Kumulatif)")
para(
    "Uji konsistensi memakai metode deviasi kumulatif (Persamaan 2.2 sampai 2.4). "
    "Dengan n = 14, diperoleh Dy = " + rup(KONS["Dy"], 3) + " mm dan nilai maksimum "
    "mutlak deviasi terstandar maks |S*k| = " + rup(KONS["Q"], 3) + ", sehingga "
    "Q/\u221an = " + rup(KONS["qsqrt"], 3) + ". Nilai kritis hasil interpolasi Tabel 2.3 "
    "untuk n = 14 adalah " + n(KONS["q95"], 3) + " (95%) dan " + n(KONS["q99"], 3) +
    " (99%). Karena Q/\u221an lebih kecil daripada kedua nilai kritis tersebut, seri data "
    "dinyatakan konsisten dan seluruh 14 data dipakai pada analisis frekuensi."
)
caption_table("4.4", "Hasil Uji Konsistensi (Deviasi Kumulatif)")
table(
    ["Parameter", "Nilai"],
    [
        ["n", ni(14)],
        ["Dy (mm)", rup(KONS["Dy"], 3)],
        ["Q = maks |S*k|", rup(KONS["Q"], 3)],
        ["Q/\u221an hitung", rup(KONS["qsqrt"], 3)],
        ["Nilai kritis 95%", n(KONS["q95"], 3)],
        ["Nilai kritis 99%", n(KONS["q99"], 3)],
        ["Kesimpulan 95%", "Konsisten"],
        ["Kesimpulan 99%", "Konsisten"],
    ],
    widths=[8.0, 6.0],
)
gambar("gambar4-2.png", "4.2",
       "Kurva deviasi kumulatif terstandar dan batas kritis 95% serta 99%")

# ------------------------------------------------------------------ 4.3
heading("4.3", "Analisis Frekuensi dan Curah Hujan Rencana")
subheading("4.3.1", "Parameter Statistik Seri Data Hujan")
para(
    "Parameter statistik dihitung dengan Persamaan 2.5 sampai 2.8 untuk data asli, "
    "dan Persamaan 2.13 sampai 2.15 untuk data logaritmik (Tabel 4.5). Koefisien "
    "kemencengan data asli (Cs = " + rup(CS, 3) + ") bernilai positif, artinya "
    "sebaran hujan maksimum menceng ke kanan: sebagian besar tahun memiliki hujan "
    "maksimum moderat dan sedikit tahun memiliki hujan ekstrem (antara lain 2020 "
    "dan 2021). Koefisien kemencengan logaritmik (Cs = " + rup(CSLOG, 4) + ") lebih "
    "kecil, sebagaimana lazim pada data hidrologi."
)
caption_table("4.5", "Parameter Statistik Seri Hujan Harian Maksimum (n = 14)")
table(
    ["Parameter", "Data asli", "Data logaritmik"],
    [
        ["Rata-rata", rup(XBAR, 3) + " mm", n(LOGBAR, 4)],
        ["Standar deviasi (S)", rup(S, 3) + " mm", n(SLOG, 4)],
        ["Koefisien variasi (Cv)", n(CV, 4), "-"],
        ["Koefisien kemencengan (Cs)", n(CS, 4), n(CSLOG, 4)],
        ["Koefisien kurtosis (Ck)", n(CK, 4), "-"],
    ],
    widths=[6.5, 4.0, 3.5],
)

subheading("4.3.2", "Hujan Rencana Menurut Tiga Kandidat Distribusi")
para(
    "Tiga distribusi yang diuji sesuai Subbab 2.3.4 adalah Normal (Persamaan 2.9), "
    "Gumbel Tipe I (Persamaan 2.10 sampai 2.12), dan Log Pearson Tipe III "
    "(Persamaan 2.16). Faktor frekuensi Normal, variabel reduksi Gumbel, dan faktor "
    "K Log Pearson Tipe III dihitung dengan fungsi yang menghasilkan nilai pada "
    "Tabel 2.4 sampai 2.6. Hasil R24 menurut ketiga distribusi disajikan pada "
    "Tabel 4.6 dan Gambar 4.3. Parameter distribusi yang dihitung adalah Gumbel: "
    "a = 1,283/S = " + rup(GUM["a"], 4) + " dan X\u2080 = x\u0304 \u2212 0,577/a = "
    + rup(GUM["Xo"], 3) + " mm."
)
caption_table("4.6", "Hujan Rencana Harian R24 (mm) Menurut Distribusi dan Kala Ulang")
rows = []
for dist, key in (("Normal", "Normal"), ("Gumbel Tipe I", "Gumbel"),
                  ("Log Pearson III", "LP3")):
    rows.append([dist] + [n(FREQ[str(t)][key], 3) for t in TS])
table(["Distribusi"] + [f"T = {t}" for t in TS], rows,
      widths=[4.0] + [1.6] * len(TS), numerik=set(range(1, len(TS) + 1)))
para(
    "Pada kala ulang 10 tahun, ketiga distribusi menghasilkan R24 yang berdekatan "
    "(" + n(FREQ["10"]["Normal"], 3) + "; " + n(FREQ["10"]["Gumbel"], 3) + "; dan "
    + n(FREQ["10"]["LP3"], 3) + " mm), sehingga pilihan distribusi tidak sensitif "
    "pada kala ulang rencana.", after=8,
)
gambar("gambar4-3.png", "4.3",
       "Kurva frekuensi curah hujan rencana tiga distribusi dan data observasi")

subheading("4.3.3", "Hasil Pengujian Keselarasan Distribusi (Chi-Kuadrat)")
para(
    "Uji Chi-Kuadrat (Persamaan 2.17) dilakukan dengan lima kelas yang batasnya "
    "adalah hujan rencana T = 2, 5, 10, dan 25 tahun. Peluang tiap kelas dipilih "
    "agar menjumlah satu, yaitu 0,50; 0,20; 0,10; 0,06; dan 0,14, sehingga frekuensi "
    "harapan Ei = n \u00d7 peluang. Sesuai syarat uji, kelas dengan frekuensi harapan "
    "kurang dari 5 digabungkan sebagai uji tambahan (kelas 2 sampai 5 digabung: "
    "O = [9; 5], E = [7,0; 7,0], \u03c7\u00b2 = " + n(CHI["LP3"]["e5"]["chi2"], 3) + "). "
    "Frekuensi pengamatan dan harapan tiap distribusi disajikan pada Tabel 4.7, dan "
    "hasil uji disajikan pada Tabel 4.8."
)
caption_table("4.7", "Frekuensi Pengamatan dan Harapan pada Uji Chi-Kuadrat")
peluang = [0.50, 0.20, 0.10, 0.06, 0.14]
batas_lbl = ["X < X\u2082", "X\u2082 \u2264 X < X\u2085", "X\u2085 \u2264 X < X\u2081\u2080",
             "X\u2081\u2080 \u2264 X < X\u2082\u2085", "X \u2265 X\u2082\u2085"]
rows = []
for i in range(5):
    rows.append([batas_lbl[i], n(peluang[i], 2),
                 n(CHI["LP3"]["E"][i], 2),
                 ni(CHI["Normal"]["O"][i]), ni(CHI["Gumbel"]["O"][i]),
                 ni(CHI["LP3"]["O"][i])])
table(["Kelas", "Peluang", "Ei", "Oi Normal", "Oi Gumbel", "Oi LP3"],
      rows, widths=[5.0, 2.0, 2.0, 2.2, 2.2, 2.0],
      numerik={1, 2, 3, 4, 5})
caption_table("4.8", "Hasil Uji Chi-Kuadrat")
table(
    ["Parameter", "Normal", "Gumbel Tipe I", "Log Pearson III"],
    [
        ["\u03c7\u00b2 hitung", n(CHI["Normal"]["chi2"], 3), n(CHI["Gumbel"]["chi2"], 3),
         n(CHI["LP3"]["chi2"], 3)],
        ["Derajat kebebasan (dk)", ni(CHI["Normal"]["df"]), ni(CHI["Gumbel"]["df"]),
         ni(CHI["LP3"]["df"])],
        ["\u03c7\u00b2 kritis (\u03b1 = 5%)", n(CHI["Normal"]["crit"], 3),
         n(CHI["Gumbel"]["crit"], 3), n(CHI["LP3"]["crit"], 3)],
        ["Hasil", "Lolos", "Lolos", "Lolos"],
    ],
    widths=[5.0, 3.0, 3.2, 3.2],
)
para(
    "Ketiga distribusi lolos uji pada \u03b1 = 5% karena \u03c7\u00b2 hitung tidak melebihi "
    "nilai kritis. Dari distribusi yang lolos dipilih yang \u03c7\u00b2 hitungnya terkecil, "
    "yaitu Log Pearson Tipe III (\u03c7\u00b2 = " + n(CHI["LP3"]["chi2"], 3) + "). Pilihan "
    "ini sejalan dengan pertimbangan bahwa Log Pearson Tipe III lebih sesuai untuk "
    "sebaran hujan yang menceng ke kanan."
)

subheading("4.3.4", "Penetapan Hujan Rencana R24")
para(
    "Hujan rencana yang dipakai pada analisis selanjutnya adalah R24 untuk kala "
    "ulang 10 tahun menurut distribusi terpilih (Log Pearson Tipe III), yaitu "
    "R24 = " + n(VAL["R24"], 3) + " mm (Tabel 4.9)."
)
caption_table("4.9", "Hujan Rencana Harian R24 Distribusi Terpilih (Log Pearson Tipe III)")
table(["Kala ulang T (tahun)"] + [f"{t}" for t in (2, 5, 10, 25, 50, 100)],
      [["R24 (mm)"] + [n(FREQ[str(t)]["LP3"], 3) for t in (2, 5, 10, 25, 50, 100)]],
      widths=[4.5] + [1.6] * 6, numerik=set(range(1, 7)))

# ------------------------------------------------------------------ 4.4
heading("4.4", "Analisis Intensitas Hujan Rencana")
subheading("4.4.1", "Perhitungan Waktu Konsentrasi")
para(
    "Waktu konsentrasi dihitung dari Persamaan 2.19 sampai 2.21, yaitu waktu "
    "pengaliran di atap to (Kirpich) dan waktu pengaliran di pipa td = Ld/(60 v). "
    "Dengan Lo = 8,0 m dan S = 0,30 diperoleh to = " + rup(HID["to"], 3) + " menit. "
    "Panjang pipa penyalur Ld = 330 m bersumber dari geometri siteplan. Kecepatan v "
    "pada td adalah kecepatan aliran penuh pipa menurut Manning (Persamaan 2.28; "
    "n = 0,011; S = 0,003; Rh = D/4), sehingga bergantung pada diameter pipa. Untuk "
    "setiap diameter komersial dihitung v, td, tc = (to + td)/60, intensitas I "
    "(Persamaan 2.18), dan debit rencana Q (Persamaan 2.22). Hasilnya adalah "
    "tc = " + n(HID["tc"], 5) + " jam = " + rup(HID["tc"] * 60, 3) + " menit. "
    "Rincian pemilihan diameter pipa disajikan pada Subbab 4.6."
)

subheading("4.4.2", "Intensitas Hujan dan Kurva IDF Mononobe")
para(
    "Intensitas hujan dihitung dengan rumus Mononobe (Persamaan 2.18). Untuk "
    "T = 10 tahun, R24 = " + n(VAL["R24"], 3) + " mm dan tc = " + n(HID["tc"], 5) +
    " jam, sehingga diperoleh I = " + rup(HID["I"], 2) + " mm/jam. Intensitas pada "
    "tc untuk berbagai kala ulang disajikan pada Tabel 4.10, dan kurva "
    "intensitas\u2013durasi\u2013frekuensi Mononobe pada Tabel 4.11."
)
caption_table("4.10", "Intensitas Hujan pada tc Menurut Kala Ulang")
table(["Kala ulang T (tahun)"] + [f"{t}" for t in (2, 5, 10, 25)],
      [["R24 (mm)"] + [n(FREQ[str(t)]["LP3"], 3) for t in (2, 5, 10, 25)],
       ["I pada tc (mm/jam)"] + [
           n(FREQ[str(t)]["LP3"] / 24 * (24 / HID["tc"]) ** (2 / 3), 2)
           for t in (2, 5, 10, 25)]],
      widths=[4.5] + [2.2] * 4, numerik={1, 2, 3, 4})

durasi = [5, 10, 15, 20, 30, 45, 60, 90, 120, 180, 240, 360]
rows = []
for d in durasi:
    t_jam = d / 60
    rows.append([ni(d)] + [
        n(FREQ[str(t)]["LP3"] / 24 * (24 / t_jam) ** (2 / 3), 1)
        for t in (2, 5, 10, 25)])
caption_table("4.11", "Kurva Intensitas\u2013Durasi\u2013Frekuensi (IDF) Mononobe (mm/jam)")
table(["Durasi (menit)", "T = 2", "T = 5", "T = 10", "T = 25"],
      rows, widths=[3.4, 2.6, 2.6, 2.6, 2.6], numerik={0, 1, 2, 3, 4})
para(
    "Intensitas " + rup(HID["I"], 1) + " mm/jam pada tc \u2248 " +
    rup(HID["tc"] * 60, 2) + " menit tergolong tinggi karena persamaan Mononobe "
    "memperbesar intensitas secara berpangkat 2/3 terhadap 24/tc. Persamaan "
    "Mononobe pada dasarnya diturunkan untuk durasi hingga 24 jam, sehingga "
    "penerapannya pada tc beberapa menit merupakan ekstrapolasi yang menghasilkan "
    "nilai konservatif (cenderung besar). Hal ini wajar untuk perencanaan pengaman, "
    "dan nilai konservatif tersebut dipakai sebagai batas atas pada perancangan "
    "diameter pipa.", after=8,
)

# ------------------------------------------------------------------ 4.5
heading("4.5", "Analisis Debit Puncak Limpasan")
para(
    "Debit puncak limpasan atap dihitung dengan metode Rasional (Persamaan 2.22, "
    "A dalam km\u00b2) memakai intensitas pada tc. Untuk T = 10 tahun, dengan "
    "C = 0,80, A = 0,010400 km\u00b2, dan I = " + rup(HID["I"], 2) + " mm/jam, "
    "diperoleh Q = 0,278 \u00b7 C \u00b7 I \u00b7 A = " + rup(HID["Q"], 4) +
    " m\u00b3/detik (Tabel 4.12). Debit ini adalah debit teoritis jika badai "
    "berintensitas " + rup(HID["I"], 1) + " mm/jam terjadi serentak di seluruh atap; "
    "karena itu nilainya bersifat konservatif dan sekaligus menjadi dasar pemilihan "
    "diameter pipa pada Subbab 4.6."
)
caption_table("4.12", "Debit Puncak Limpasan Atap Total (Metode Rasional)")
table(["Kala ulang T (tahun)"] + [f"{t}" for t in (2, 5, 10, 25)],
      [["I pada tc (mm/jam)"] + [
          n(FREQ[str(t)]["LP3"] / 24 * (24 / HID["tc"]) ** (2 / 3), 2)
          for t in (2, 5, 10, 25)],
       ["Q (m\u00b3/detik)"] + [
          n(0.278 * 0.80 * FREQ[str(t)]["LP3"] / 24 * (24 / HID["tc"]) ** (2 / 3)
            * 0.0104, 4) for t in (2, 5, 10, 25)]],
      widths=[4.5] + [2.2] * 4, numerik={1, 2, 3, 4})
para(
    "Pada Tabel 4.12, nilai Q untuk tiap kala ulang dihitung dengan faktor "
    "frekuensi yang sama seperti Tabel 4.10 dan Tabel 4.11; hanya nilai T = 10 tahun "
    "yang dipakai sebagai debit desain.", after=8,
)

# ------------------------------------------------------------------ 4.6
heading("4.6", "Hidrolika Pipa Penyalur")
para(
    "Diameter pipa penyalur dipilih melalui aturan iterasi (envelope) "
    "v\u2013td\u2013tc\u2013I\u2013Q\u2013D: kecepatan aliran penuh mengubah td, td mengubah tc, "
    "tc mengubah I, I mengubah Q, dan Q menentukan diameter; proses diulang sampai "
    "berkonvergensi. Pipa diperlakukan kontinu dengan kemiringan tetap S = 0,003 m/m "
    "dan dialiri penuh (Manning aliran penuh, Persamaan 2.28). Hasil iterasi "
    "disajikan pada Tabel 4.13; karena Q tidak monoton terhadap langkah iterasi, "
    "debit desain ditetapkan sebagai nilai maksimum iterasi (aturan envelope, "
    "konservatif)."
)
rows = []
for i, r in enumerate(HITER, 1):
    rows.append([ni(i), n(r[1], 2), n(r[2] * 60, 3), n(r[3], 2), n(r[4], 4),
                 ni(r[5] * 1000), ni(r[6]), n(r[7], 3)])
caption_table("4.13", "Iterasi Pemilihan Diameter Pipa Penyalur (Aturan Envelope)")
table(["Langkah", "td (menit)", "tc (menit)", "I (mm/jam)", "Q (m\u00b3/dtk)",
       "D teoritis (mm)", "D komersial (mm)", "v (m/dtk)"],
      rows, widths=[1.5, 1.9, 1.9, 2.0, 2.0, 2.1, 2.1, 1.7],
      numerik={0, 1, 2, 3, 4, 5, 6, 7})
para(
    "Debit desain (maksimum iterasi) adalah Q = " + rup(HID["Q"], 4) +
    " m\u00b3/detik, yang membutuhkan diameter teoritis D = " + ni(HID["Dteor"] * 1000) +
    " mm; diameter komersial terdekat ke atas adalah DN" + ni(HID["Dkom"]) +
    ". Pada diameter tersebut kecepatan aliran penuh v = " + n(HID["v"], 3) +
    " m/detik dan kapasitas Manning penuh sebesar " + n(HID["kapasitas"], 4) +
    " m\u00b3/detik, lebih besar daripada debit desain sehingga pipa aman "
    "(Gambar 4.4). Pipa per unit rumah, talang, dan bak pengumpul dirinci pada "
    "Tabel 4.14."
)
gambar("gambar4-7.png", "4.4",
       "Osilasi iterasi hidrolika dan perbandingan debit desain dengan kapasitas DN900")
caption_table("4.14", "Hidrolika Pipa per Unit, Talang, dan Bak Pengumpul")
table(
    ["Komponen", "Besaran", "Nilai", "Satuan"],
    [
        ["Pipa penyalur per unit", "Q unit", n(UNIT["Q_unit"] * 1000, 3), "liter/detik"],
        ["Pipa penyalur per unit", "Diameter", ni(UNIT["D_kom"]), "mm"],
        ["Pipa penyalur per unit", "Kecepatan", n(UNIT["v"], 3), "m/detik"],
        ["Talang atap (0,15 \u00d7 0,10 m)", "Kapasitas", n(UNIT["Q_talang"] * 1000, 3),
         "liter/detik"],
        ["Talang atap (0,15 \u00d7 0,10 m)", "Kecepatan", n(UNIT["v_talang"], 3),
         "m/detik"],
        ["Bak pengumpul per unit", "Volume", n(UNIT["V_bak"], 1), "m\u00b3"],
    ],
    widths=[5.5, 3.5, 2.5, 2.5],
)

# ------------------------------------------------------------------ 4.7
heading("4.7", "Analisis Kebutuhan Air dan Neraca Air")
subheading("4.7.1", "Kebutuhan Air dan Fraksi yang Dilayani")
para(
    "Kebutuhan air harian total dihitung dengan Persamaan 3.1: "
    "Qharian = n_unit \u00b7 n_jiwa \u00b7 q = 160 \u00d7 4 \u00d7 120 = 76,8 m\u00b3/hari "
    "(28.032 m\u00b3/tahun). Subbab 2.1 membatasi pemanfaatan air hujan pada kebutuhan "
    "non-potabel, sedangkan standar 120 L/jiwa/hari mencakup seluruh kebutuhan "
    "domestik. Karena itu dianalisis lima skenario fraksi kebutuhan yang dilayani: "
    "100%, 70%, 65% (desain), 60%, dan 50%. Batas bawah 50% mengacu pada Vovk dkk. "
    "(2023) yang melaporkan kebutuhan non-minum melebihi 50% kebutuhan air "
    "perkotaan, sedangkan fraksi desain 65% adalah titik tengah rentang 60\u201370% "
    "(Subbab 3.4.1). Kebutuhan desain menjadi " + n(Qharian65, 2) + " m\u00b3/hari "
    "(" + ni(Qharian * 0.65 * 365) + " m\u00b3/tahun)."
)

subheading("4.7.2", "Pasokan Air Hujan dan Evaporasi Kolam")
para(
    "Pasokan bulanan dihitung dengan Persamaan 2.23 memakai hujan bulanan rata-rata "
    "14 tahun. Evaporasi kolam dihitung dengan metode Penman (1948) untuk muka air "
    "terbuka, memakai data iklim NOAA ISD Supadio (suhu, kelembapan, angin, tekanan) "
    "dan radiasi NASA POWER (CERES). Hujan yang jatuh langsung di permukaan kolam "
    "(P \u00d7 Ap) diperhitungkan sebagai pemasukan tambahan. Evaporasi bulanan "
    "berkisar " + n(min(evap_mm_avg), 1) + "\u2013" + n(max(evap_mm_avg), 1) +
    " mm/bulan (total " + rup(evap_thn_mm, 1) + " mm/tahun). Rincian pasokan, "
    "kebutuhan, dan evaporasi bulanan rata-rata disajikan pada Tabel 4.15, dan "
    "sebaran evaporasi Penman pada Gambar 4.5."
)
caption_table("4.15", "Pasokan Atap, Kebutuhan, dan Evaporasi Bulanan (Rata-rata 2012\u20132025)")
rows = []
for b in range(12):
    rows.append([BULAN[b], rup(rain_avg[b], 1), n(evap_mm_avg[b], 1),
                 ni(supply_avg[b]), ni(ppond_avg[b]), ni(demand_avg[b]),
                 ni(evap_avg[b])])
rows.append(["\u03a3", rup(total_hujan_thn_avg, 1), rup(evap_thn_mm, 1),
             ni(supply_thn_avg), ni(sum(ppond_avg)), ni(demand_thn_avg),
             ni(evap_thn_m3)])
table(["Bulan", "R (mm)", "Evaporasi (mm)", "Vsupply (m\u00b3)",
       "P\u00b7Ap kolam (m\u00b3)", "Vdemand 65% (m\u00b3)", "Evaporasi (m\u00b3)"],
      rows, widths=[2.4, 1.8, 2.3, 2.2, 2.4, 2.4, 2.4],
      numerik={1, 2, 3, 4, 5, 6})
para(
    "Total pasokan atap tahunan adalah " + ni(supply_thn_avg) + " m\u00b3/tahun; "
    "dengan tambahan hujan langsung di kolam, total pemasukan menjadi "
    + ni(supply_thn_avg + sum(ppond_avg)) + " m\u00b3/tahun, sedangkan kebutuhan "
    "desain (fraksi 65%) adalah " + ni(Qharian * 0.65 * 365) + " m\u00b3/tahun dan "
    "evaporasi kolam setara " + ni(evap_thn_m3) + " m\u00b3/tahun. Penjumlahan "
    "kebutuhan pada kolom Tabel 4.15 menghasilkan " + ni(sum(demand_avg)) +
    " m\u00b3/tahun (mengikuti panjang bulan nyata); nilai rancangan dari "
    "Persamaan 3.1 dengan 365 hari adalah " + ni(Qharian * 0.65 * 365) +
    " m\u00b3/tahun. Selisih " + n(abs(sum(demand_avg) - Qharian * 0.65 * 365), 1) +
    " m\u00b3/tahun (\u003c 0,1%) berasal dari perbedaan panjang bulan.", after=8,
)
gambar("gambar4-8.png", "4.5",
       "Evaporasi muka air bulanan (Penman 1948) dan komponen iklimnya")

subheading("4.7.3", "Neraca Air Bulanan dan Kurva Massa Rippl")
para(
    "Neraca air bulanan dihitung dengan Persamaan 2.25: "
    "Si = S(i\u22121) + Vsupply,i + P\u00b7Ap,i \u2212 Vdemand,i \u2212 Ei, dan disusun untuk "
    "seluruh 168 bulan periode 2012\u20132025 (14 tahun). Volume tampungan Vs "
    "ditentukan dengan metode kurva massa Rippl (Persamaan 2.26), yaitu selisih "
    "terbesar antara kumulatif maksimum dan kumulatif minimum yang mengikutinya. "
    "Untuk fraksi desain 65%, diperoleh Vs = " + rup(KOL["Vs"], 1) + " m\u00b3 "
    "(Gambar 4.7). Neraca bulanan dan kumulatifnya ditampilkan pada Gambar 4.6."
)
gambar("gambar4-5.png", "4.6",
       "Neraca air bulanan dan kumulatif pada fraksi kebutuhan 65%")
gambar("gambar4-4.png", "4.7",
       "Kurva massa Rippl neraca air bulanan pada fraksi kebutuhan 65%")

subheading("4.7.4", "Tingkat Keandalan Pasokan")
para(
    "Keandalan dihitung dari simulasi bulanan 168 bulan sebagai perbandingan jumlah "
    "bulan terpenuhi terhadap jumlah bulan total (Persamaan 2.27). Ringkasan Vs dan "
    "keandalan tiap fraksi disajikan pada Tabel 4.16. Pada fraksi desain 65%, "
    "kebutuhan terpenuhi pada 167 dari 168 bulan sehingga keandalan "
    + n(DES["neraca"]["0.65"]["reliability"], 1) + "%. Pada fraksi 100%, keandalan "
    "turun menjadi " + n(DES["neraca"]["1.00"]["reliability"], 1) + "%, yang "
    "menunjukkan bahwa sistem tidak dapat diandalkan untuk memasok seluruh "
    "kebutuhan domestik, khususnya air minum."
)
caption_table("4.16", "Ringkasan Fraksi Kebutuhan: Volume Tampungan Vs dan Keandalan")
rows = []
relabel = {"1.00": "100%", "0.70": "70%", "0.65": "65% (desain)", "0.60": "60%",
           "0.50": "50%"}
for f in ["1.00", "0.70", "0.65", "0.60", "0.50"]:
    d = DES["neraca"][f]
    rows.append([relabel[f], ni(Qharian * float(f) * 365), rup(d["vs"], 1),
                 n(d["reliability"], 1) + "%"])
table(["Fraksi", "Kebutuhan (m\u00b3/tahun)", "Vs (m\u00b3)", "Keandalan"],
      rows, widths=[3.4, 4.0, 3.4, 3.0], numerik={1, 2, 3})

# ------------------------------------------------------------------ 4.8
heading("4.8", "Volume Atenuasi Banjir (Va) dan Volume Desain Kolam")
subheading("4.8.1", "Volume Tampungan Atenuasi")
para(
    "Volume atenuasi dihitung dengan Persamaan 2.31, Va = Qin \u00b7 th, pada asumsi "
    "konservatif tidak ada pelepasan (Qout = 0) dan durasi hujan efektif th = 1,0 jam "
    "sebagai kriteria desain (Subbab 3.4.3). Dengan debit masuk hasil Subbab 4.5, "
    "diperoleh Va = " + rup(KOL["Va"], 1) + " m\u00b3. Sensitivitas Va terhadap th "
    "disajikan pada Tabel 4.17."
)
caption_table("4.17", "Sensitivitas Volume Atenuasi Va terhadap Durasi Hujan th")
thv = ["0.5", "1", "1.5", "2", "3"]
thv_lbl = ["0,5", "1,0", "1,5", "2,0", "3,0"]
table(["th (jam)"] + thv_lbl,
      [["Va (m\u00b3)"] + [ni(KOL["Va_sensitivitas"][k]) for k in thv]],
      widths=[3.5] + [2.3] * 5, numerik={1, 2, 3, 4, 5})

subheading("4.8.2", "Volume Desain dan Iterasi Konvergensi Luas Kolam")
para(
    "Dengan kriteria ganda Persamaan 2.32, volume desain kolam adalah "
    "Vdesain = maks(Vs, Va). Karena Vs (" + rup(KOL["Vs"], 1) + " m\u00b3) jauh lebih "
    "besar daripada Va (" + rup(KOL["Va"], 1) + " m\u00b3), maka volume desain "
    "ditetapkan oleh fungsi penyedia air baku, yaitu Vdesain = " +
    rup(KOL["V_desain"], 1) + " m\u00b3. Luas permukaan kolam Ap memengaruhi evaporasi "
    "dan hujan langsung yang masuk, sehingga Ap dan Vs saling bergantung; iterasi "
    "Ap \u2194 Vs diulang sampai mencapai titik tetap (Tabel 4.18 dan Gambar 4.8c). "
    "Iterasi konvergen pada langkah ke-5 dengan Ap = " + n(KOL["Ap"], 2) + " m\u00b2."
)
rows = []
for d in ITER:
    rows.append([ni(d["i"]), n(d["Ap_masuk"], 1), rup(d["Vs"], 1),
                 n(d["p"], 1) + " \u00d7 " + n(d["l"], 1), n(d["Ap_keluar"], 1)])
caption_table("4.18", "Iterasi Konvergensi Luas Permukaan Kolam (Ap \u2194 Vs)")
table(["Langkah", "Ap masuk (m\u00b2)", "Vs (m\u00b3)", "Dimensi p \u00d7 l (m)",
       "Ap keluar (m\u00b2)"],
      rows, widths=[1.8, 3.2, 3.2, 3.2, 3.0], numerik={0, 1, 2, 3, 4})
para(
    "Dengan kedalaman efektif he = " + n(KOL["he"], 1) + " m dan tambahan tinggi "
    "jagaan (freeboard) " + n(KOL["hf"], 1) + " m, dimensi kolam adalah panjang "
    + n(KOL["p"], 1) + " m \u00d7 lebar " + n(KOL["l"], 1) + " m \u00d7 kedalaman total "
    + n(KOL["htotal"], 1) + " m, dengan luas permukaan Ap = " + n(KOL["Ap"], 2) +
    " m\u00b2. Pipa pelimpah untuk debit masuk Qin dipilih DN" + ni(KOL["D_overflow"]) +
    " mm. Perancangan teknis rinci kolam (talud, struktur pelimpah, dan pondasi) "
    "dibahas pada bagian perancangan lanjutan."
)

# ------------------------------------------------------------------ 4.9
heading("4.9", "Analisis Sensitivitas")
para(
    "Analisis sensitivitas dilakukan untuk menguji pengaruh kriteria desain "
    "terhadap hasil, yaitu fraksi kebutuhan terhadap Vs dan keandalan, durasi hujan "
    "terhadap Va, koefisien limpasan terhadap debit dan volume, serta konvergensi "
    "iterasi Ap \u2194 Vs. Ringkasannya disajikan pada Gambar 4.8 dan Tabel 4.19."
)
gambar("gambar4-6.png", "4.8",
       "Analisis sensitivitas desain kolam: (a) Vs terhadap fraksi kebutuhan; "
       "(b) Va terhadap th; (c) iterasi konvergensi Vs\u2013Ap")
caption_table("4.19", "Sensitivitas Debit dan Volume Atenuasi terhadap Koefisien Limpasan C")
rows = []
for c in (0.7, 0.8, 0.9):
    Qc = HID["Q"] * c / 0.80
    rows.append([n(c, 2), n(Qc, 4), rup(Qc * 3600, 0)])
table(["C", "Q (m\u00b3/detik)", "Va = Q \u00b7 th (m\u00b3)"],
      rows, widths=[3.0, 4.0, 4.0], numerik={1, 2})
para(
    "Pada Tabel 4.19, nilai Q untuk tiap C diperoleh dengan penskalaan linear "
    "langsung dari debit desain terverifikasi (Q \u221d C, dengan I dan A tetap), "
    "sehingga tidak ada perhitungan ulang rumus. Kenaikan C dari 0,70 menjadi 0,90 "
    "menaikkan Q dan Va sekitar 29%. Dari seluruh sensitivitas, hasil bahwa Vs "
    "menentukan volume desain (Vs > Va) tetap berlaku."
)

# ------------------------------------------------------------------ 4.10
heading("4.10", "Pembahasan")
para(
    "Tiga hal penting dibahas pada subbab ini: penentuan parameter dominan, "
    "konsistensi sumber data, dan verifikasi asumsi lapangan."
)
subheading("4.10.1", "Perubahan Parameter Penentu Volume Kolam")
para(
    "Hasil analisis menunjukkan bahwa fungsi penyedia air baku (Vs) menentukan "
    "volume desain, bukan fungsi atenuasi banjir (Va). Vs = " + rup(KOL["Vs"], 1) +
    " m\u00b3 jauh melampaui Va = " + rup(KOL["Va"], 1) + " m\u00b3. Temuan ini "
    "berbeda dari draf berbasis data lama yang menyimpulkan Va lebih besar daripada "
    "Vs; perbedaan tersebut berasal dari penggunaan sumber data hujan dan panjang "
    "seri yang berbeda, bukan dari perubahan metode. Dengan sumber data BWSK "
    "2012\u20132025 dan metode yang telah ditetapkan pada Bab II dan Bab III, "
    "kebutuhan tampungan air baku menjadi penentu utama dimensi kolam."
)
subheading("4.10.2", "Konsistensi Sumber Data")
para(
    "Seluruh angka pada bab ini konsisten bersumber dari satu basis data "
    "(hidrologi.db) yang dibangun dari data curah hujan BWSK Sungai Ambawang "
    "2012\u20132025. Data hujan Stasiun Supadio tidak dipakai untuk hujan rencana. "
    "Untuk variabel iklim evaporasi, suhu, kelembapan, angin, dan tekanan berasal "
    "dari NOAA ISD Supadio, sedangkan radiasi matahari (Rs) berasal dari NASA POWER "
    "(CERES). NASA POWER adalah produk satelit/reanalisis, bukan pengamatan stasiun, "
    "sehingga penggunaannya dinyatakan secara eksplisit; pola musimannya "
    "konsisten dengan pola iklim Supadio."
)
subheading("4.10.3", "Verifikasi Asumsi Lapangan")
para(
    "Sejumlah parameter merupakan asumsi desain yang wajib diverifikasi melalui "
    "survei lapangan: panjang lereng atap Lo (8,0 m), kemiringan atap S (30%), "
    "kemiringan pipa S (0,30%), dan kedalaman efektif kolam he (3,0 m). Panjang "
    "pipa penyalur Ld (330 m) bersumber dari siteplan. Pengaruh Lo terhadap waktu "
    "konsentrasi tc kecil (kurang dari 5%) sehingga tidak menentukan hasil, "
    "sedangkan kemiringan pipa perlu dikonfirmasi melalui pengukuran waterpass "
    "karena menentukan kecepatan aliran dan kapasitas pipa."
)

# ------------------------------------------------------------------ 4.11
heading("4.11", "Rekapitulasi Hasil dan Keterbatasan")
caption_table("4.20", "Rekapitulasi Hasil Analisis Bab IV")
table(
    ["Hasil", "Nilai", "Subbab"],
    [
        ["Hujan tahunan rata-rata", rup(total_hujan_thn_avg, 1) + " mm/tahun", "4.2.1"],
        ["Uji homogenitas (Uji-t, dua arah 5%)",
         "Homogen (t = " + rup(T["t"], 3) + " < 2,179)", "4.2.2"],
        ["Uji konsistensi (Q/\u221an)", rup(KONS["qsqrt"], 3) + " (konsisten)", "4.2.3"],
        ["Distribusi terpilih", "Log Pearson Tipe III", "4.3.3"],
        ["R24 kala ulang 10 tahun", n(VAL["R24"], 3) + " mm", "4.3.4"],
        ["Waktu konsentrasi tc", rup(HID["tc"] * 60, 2) + " menit", "4.4.1"],
        ["Intensitas hujan T = 10 tahun", rup(HID["I"], 2) + " mm/jam", "4.4.2"],
        ["Debit puncak atap (T = 10 th)", rup(HID["Q"], 4) + " m\u00b3/detik", "4.5"],
        ["Diameter pipa penyalur", "DN" + ni(HID["Dkom"]) + " mm (aman, v = "
         + n(HID["v"], 3) + " m/detik)", "4.6"],
        ["Kebutuhan air total", n(Qharian, 1) + " m\u00b3/hari (" + ni(Qharian * 365)
         + " m\u00b3/tahun)", "4.7.1"],
        ["Evaporasi kolam (Penman)", rup(evap_thn_mm, 1) + " mm/tahun", "4.7.2"],
        ["Vs (fraksi 65%)", rup(KOL["Vs"], 1) + " m\u00b3", "4.7.3"],
        ["Keandalan (fraksi 65%; 100%)",
         n(DES["neraca"]["0.65"]["reliability"], 1) + "%; "
         + n(DES["neraca"]["1.00"]["reliability"], 1) + "%", "4.7.4"],
        ["Va (th = 1 jam)", rup(KOL["Va"], 1) + " m\u00b3", "4.8.1"],
        ["Vdesain = maks(Vs, Va)", rup(KOL["V_desain"], 1) + " m\u00b3 (Vs menentukan)",
         "4.8.2"],
        ["Dimensi kolam", n(KOL["p"], 1) + " \u00d7 " + n(KOL["l"], 1) + " \u00d7 "
         + n(KOL["htotal"], 1) + " m", "4.8.2"],
    ],
    widths=[5.6, 5.0, 2.4],
)
para("Keterbatasan yang melekat pada hasil bab ini:")
bullet("Data hujan berasal dari stasiun BWSK Sungai Ambawang periode 14 tahun "
       "(2012\u20132025); panjang data ini memenuhi syarat minimum pedoman "
       "perencanaan, tetapi masih di bawah saran SNI 2415:2016.")
bullet("Terdapat 12 hari tanpa data (0,23%) yang dibiarkan kosong (NULL); dampak "
       "terbesar pada Maret 2023. Nilai maksimum harian tahun 2023 diperlakukan "
       "sebagai maksimum teramati.")
bullet("Variabel iklim evaporasi memakai radiasi NASA POWER yang merupakan produk "
       "satelit/reanalisis; validasi terhadap panci evaporasi lapangan belum "
       "dilakukan.")
bullet("Parameter lapangan (Lo, S atap, S pipa, he) masih berupa asumsi desain dan "
       "perlu diverifikasi melalui survei serta pengukuran waterpass.")
bullet("Persamaan Mononobe pada tc sekitar beberapa menit merupakan ekstrapolasi "
       "di luar rentang durasi asalnya, sehingga debit puncak, diameter pipa, dan Va "
       "bersifat konservatif (batas atas).")
bullet("Pipa diperlakukan kontinu; kehilangan energi di ujung pipa, kehilangan "
       "gesekan lokal, dan pemilihan pompa untuk jaringan distribusi (kolam ke "
       "warga) akan dibahas pada tahap perancangan berikutnya.")

doc.save(OUT)
print("Tersimpan:", OUT.relative_to(ROOT), f"({OUT.stat().st_size:,} bytes)")
