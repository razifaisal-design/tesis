# -*- coding: utf-8 -*-
"""Buat data/processed/Perhitungan_Hidrologi.xlsx dari data/processed/hidrologi.db.
Semua perhitungan memakai formula Excel hidup yang saling terhubung antar-sheet
(input = data mentah dari SQLite + tabel koefisien referensi).
Sheet desain: Kawasan, Evaporasi, Hidrolika_Pipa (iterasi envelope, Manning
aliran penuh), Neraca_Air (Rippl 5 fraksi), Desain_Kolam (Va/Vs/dimensi)."""
import sqlite3
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "processed" / "hidrologi.db"
OUT = ROOT / "data" / "processed" / "Perhitungan_Hidrologi.xlsx"

con = sqlite3.connect(DB)
rows = list(con.execute("SELECT tahun,bulan,tgl,tanggal,mm FROM curah_hujan_harian ORDER BY tanggal"))
years = [r[0] for r in con.execute("SELECT DISTINCT tahun FROM curah_hujan_harian ORDER BY tahun")]
kaw_rows = list(con.execute("SELECT kunci,nilai,satuan,sumber FROM kawasan ORDER BY rowid"))
par_rows = list(con.execute("SELECT kunci,nilai,satuan,keterangan FROM parameter_desain ORDER BY rowid"))
evap_rows = list(con.execute("SELECT bulan,et0_mm,keterangan FROM evaporasi ORDER BY bulan"))
pipa_rows = list(con.execute("SELECT label,d_mm FROM pipa_standar ORDER BY urut"))
bulan_rows = list(con.execute("SELECT tahun,bulan,mm,n_hari FROM curah_hujan_bulanan ORDER BY tahun,bulan"))
con.close()
NROW = len(rows)
LAST = NROW + 1  # baris terakhir data di Data_Harian

def as_num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return v

# Peta baris sheet Kawasan (data mulai baris 3) + blok turunan/tetap
KAW_ROW = {kunci: 3 + i for i, (kunci, *_rest) in enumerate(kaw_rows)}
R_KQL, R_KQ = 19, 20        # Q kebutuhan (liter/hari), Q harian (m3/hari)
R_FR0 = 26                  # baris pertama tabel fraksi di Kawasan
FR_LIST = [float(x) for x in
           next(v for k, v, *_ in kaw_rows if k == "fraksi_diuji").split(";")]
FR_DES = float(next(v for k, v, *_ in kaw_rows if k == "fraksi_desain"))
KDES = FR_LIST.index(FR_DES)

FONT = Font(name="Arial", size=10)
BOLD = Font(name="Arial", size=10, bold=True)
TITLE = Font(name="Arial", size=11, bold=True)
INPUT = Font(name="Arial", size=10, color="0000FF")
HDR_FILL = PatternFill("solid", fgColor="D9D9D9")
YELLOW = PatternFill("solid", fgColor="FFFF00")
SIDE = Side(style="thin")
BOX = Border(left=SIDE, right=SIDE, top=SIDE, bottom=SIDE)


def put(ws, ref, value, font=FONT, fmt=None, fill=None, box=False, align=None):
    c = ws[ref]
    c.value = value
    c.font = font
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    if box:
        c.border = BOX
    if align:
        c.alignment = Alignment(horizontal=align)
    return c


def header_row(ws, row, labels, start_col=1):
    for i, lab in enumerate(labels):
        c = ws.cell(row=row, column=start_col + i, value=lab)
        c.font = BOLD
        c.fill = HDR_FILL
        c.border = BOX
        c.alignment = Alignment(horizontal="center", wrap_text=True)


def widths(ws, spec):
    for col, w in spec.items():
        ws.column_dimensions[col].width = w


wb = Workbook()
ws_data = wb.active
ws_data.title = "Data_Harian"
ws_tahun = wb.create_sheet("Statistik_Tahunan")
ws_stat = wb.create_sheet("Statistik")
ws_hom = wb.create_sheet("Uji_Homogenitas")
ws_kons = wb.create_sheet("Uji_Konsistensi")
ws_freq = wb.create_sheet("Frekuensi")
ws_chi = wb.create_sheet("Chi_Kuadrat")
ws_deb = wb.create_sheet("Debit_Rencana")
ws_kaw = wb.create_sheet("Kawasan")
ws_eva = wb.create_sheet("Evaporasi")
ws_hyp = wb.create_sheet("Hidrolika_Pipa")
ws_nrc = wb.create_sheet("Neraca_Air")
ws_klm = wb.create_sheet("Desain_Kolam")
ws_koef = wb.create_sheet("Koefisien")

# ================= 1. Data_Harian (dari SQLite) =================
header_row(ws_data, 1, ["Tahun", "Bulan", "Tanggal", "Tanggal (ISO)", "Curah Hujan (mm)"])
for i, (y, b, d, iso, mm) in enumerate(rows, start=2):
    put(ws_data, f"A{i}", y, box=True)
    put(ws_data, f"B{i}", b, box=True)
    put(ws_data, f"C{i}", d, box=True)
    put(ws_data, f"D{i}", iso, box=True)
    put(ws_data, f"E{i}", mm, fmt="0.0", box=True)
put(ws_data, "G1", "Sumber: data/processed/hidrologi.db (src/build_db.py) <- Curah_Hujan_Sungai_Ambawang_BWSK_2012-2025.xlsx (BWSK). Sel kosong = data hilang.")
ws_data.freeze_panes = "A2"
widths(ws_data, {"A": 8, "B": 7, "C": 8, "D": 13, "E": 17, "G": 60})

DT = f"Data_Harian!$A$2:$A${LAST}"   # kolom tahun
DM = f"Data_Harian!$E$2:$E${LAST}"   # kolom mm

# ================= 2. Statistik_Tahunan =================
put(ws_tahun, "A1", "STATISTIK CURAH HUJAN TAHUNAN (formula dari Data_Harian)", font=TITLE)
header_row(ws_tahun, 2, ["Tahun", "Jumlah Hari", "Data Valid", "Data Hilang",
                         "Total Curah Hujan (mm)", "X Maks Harian (mm)", "Hari Hujan (mm>0)"])
for i, y in enumerate(years, start=3):
    put(ws_tahun, f"A{i}", y, box=True)
    put(ws_tahun, f"B{i}", f"=COUNTIFS({DT},$A{i})", fmt="0", box=True)
    put(ws_tahun, f"C{i}", f'=COUNTIFS({DT},$A{i},{DM},">=0")', fmt="0", box=True)
    put(ws_tahun, f"D{i}", f"=B{i}-C{i}", fmt="0", box=True)
    put(ws_tahun, f"E{i}", f"=SUMIFS({DM},{DT},$A{i})", fmt="0.0", box=True)
    put(ws_tahun, f"F{i}", f"=_xlfn.MAXIFS({DM},{DT},$A{i})", fmt="0.0", box=True)
    put(ws_tahun, f"G{i}", f'=COUNTIFS({DT},$A{i},{DM},">0")', fmt="0", box=True)
Y1, Y2 = 3, 2 + len(years)
XMAX = f"Statistik_Tahunan!$F${Y1}:$F${Y2}"
put(ws_tahun, f"A{Y2+1}", "TOTAL", font=BOLD)
put(ws_tahun, f"E{Y2+1}", f"=SUM(E{Y1}:E{Y2})", font=BOLD, fmt="0.0")
ws_tahun.freeze_panes = "A3"
widths(ws_tahun, {"A": 8, "B": 11, "C": 11, "D": 11, "E": 20, "F": 19, "G": 17})

# ================= 3. Statistik (moments & statistik log) =================
put(ws_stat, "A1", "STATISTIK DISTRIBUSI X MAKS TAHUNAN", font=TITLE)
header_row(ws_stat, 2, ["Nilai", "Satuan/Keterangan"])
put(ws_stat, "A3", "n (jumlah tahun)")
put(ws_stat, "B3", f"=COUNT({XMAX})", fmt="0")
put(ws_stat, "C3", "tahun")
put(ws_stat, "A4", "X barat (rata-rata X maks)")
put(ws_stat, "B4", f"=AVERAGE({XMAX})", fmt="0.0000")
put(ws_stat, "C4", "mm")
put(ws_stat, "A5", "S (simpangan baku, pembagi n-1)")
put(ws_stat, "B5", f"=STDEV({XMAX})", fmt="0.0000")
put(ws_stat, "C5", "mm")
put(ws_stat, "A6", "Cv = S / X barat")
put(ws_stat, "B6", "=B5/B4", fmt="0.0000")
put(ws_stat, "A7", "Cs (rumus tesis [7])")
put(ws_stat, "B7", f"=B3/((B3-1)*(B3-2))*SUMPRODUCT((({XMAX}-B4)/B5)^3)", fmt="0.0000")
put(ws_stat, "A8", "Ck (rumus tesis [8])")
put(ws_stat, "B8", f"=(1/B3)*SUMPRODUCT((({XMAX}-B4)/B5)^4)", fmt="0.0000")
put(ws_stat, "A9", "Rata-rata log10 X")
put(ws_stat, "B9", f"=SUMPRODUCT(LOG10({XMAX}))/B3", fmt="0.0000")
put(ws_stat, "A10", "S log10")
put(ws_stat, "B10", f"=SQRT(SUMPRODUCT((LOG10({XMAX})-B9)^2)/(B3-1))", fmt="0.0000")
put(ws_stat, "A11", "Cs log10 (rumus [15])")
put(ws_stat, "B11", f"=B3/((B3-1)*(B3-2))*SUMPRODUCT(((LOG10({XMAX})-B9)/B10)^3)", fmt="0.0000")
widths(ws_stat, {"A": 34, "B": 14, "C": 18})

# ================= 4. Uji_Homogenitas (uji-t) =================
X1 = f"Statistik_Tahunan!$F${Y1}:$F${Y1+6}"
X2 = f"Statistik_Tahunan!$F${Y1+7}:$F${Y2}"
put(ws_hom, "A1", "UJI HOMOGENITAS DATA (Uji-t dua sampel)", font=TITLE)
header_row(ws_hom, 2, ["Nilai", "Keterangan"])
put(ws_hom, "A3", "n1 (7 tahun pertama)")
put(ws_hom, "B3", f"=COUNT({X1})", fmt="0")
put(ws_hom, "C3", f"{years[0]}-{years[6]}")
put(ws_hom, "A4", "n2 (7 tahun terakhir)")
put(ws_hom, "B4", f"=COUNT({X2})", fmt="0")
put(ws_hom, "C4", f"{years[7]}-{years[-1]}")
put(ws_hom, "A5", "X barat 1")
put(ws_hom, "B5", f"=AVERAGE({X1})", fmt="0.0000")
put(ws_hom, "A6", "X barat 2")
put(ws_hom, "B6", f"=AVERAGE({X2})", fmt="0.0000")
put(ws_hom, "A7", "S1 (pembagi n1)")
put(ws_hom, "B7", f"=SQRT(SUMPRODUCT(({X1}-B5)^2)/B3)", fmt="0.0000")
put(ws_hom, "A8", "S2 (pembagi n2)")
put(ws_hom, "B8", f"=SQRT(SUMPRODUCT(({X2}-B6)^2)/B4)", fmt="0.0000")
put(ws_hom, "A9", "sigma pooled")
put(ws_hom, "B9", "=SQRT((B3*B7^2+B4*B8^2)/(B3+B4-2))", fmt="0.0000")
put(ws_hom, "A10", "t hitung")
put(ws_hom, "B10", "=ABS(B5-B6)/(B9*SQRT(1/B3+1/B4))", fmt="0.0000")
put(ws_hom, "A11", "dk = n1+n2-2")
put(ws_hom, "B11", "=B3+B4-2", fmt="0")
put(ws_hom, "A12", "t kritis (dua arah, alpha=5%)")
put(ws_hom, "B12", "=INDEX(Koefisien!$C$5:$C$34,MATCH(MIN(B11,30),Koefisien!$A$5:$A$34,1))", fmt="0.000")
put(ws_hom, "C12", "Tabel 2.2")
put(ws_hom, "A13", "t kritis (satu arah, alpha=5%)")
put(ws_hom, "B13", "=INDEX(Koefisien!$B$5:$B$34,MATCH(MIN(B11,30),Koefisien!$A$5:$A$34,1))", fmt="0.000")
put(ws_hom, "A14", "Kesimpulan (dua arah)")
put(ws_hom, "B14", '=IF(B10<B12,"HOMOGEN","TIDAK HOMOGEN")', font=BOLD)
put(ws_hom, "A15", "Kesimpulan (satu arah)")
put(ws_hom, "B15", '=IF(B10<B13,"HOMOGEN","TIDAK HOMOGEN")', font=BOLD)
widths(ws_hom, {"A": 32, "B": 14, "C": 18})

# ================= 5. Uji_Konsistensi (cumulative deviation) =================
put(ws_kons, "A1", "UJI KONSISTENSI DATA (Cumulative Deviation)", font=TITLE)
header_row(ws_kons, 2, ["Nilai", "Keterangan"])
put(ws_kons, "A3", "n")
put(ws_kons, "B3", "=Statistik!B3", fmt="0")
put(ws_kons, "A4", "X barat")
put(ws_kons, "B4", "=Statistik!B4", fmt="0.0000")
put(ws_kons, "A5", "Dy = SQRT(SUM(dev^2)/n)")
put(ws_kons, "B5", f"=SQRT(SUMPRODUCT($C$13:$C${12+len(years)}^2)/B3)", fmt="0.0000")
put(ws_kons, "A6", "Q = maks |S**k|")
put(ws_kons, "B6", f"=MAX(MAX($E$13:$E${12+len(years)}),-MIN($E$13:$E${12+len(years)}))", fmt="0.0000")
put(ws_kons, "A7", "Q / SQRT(n)")
put(ws_kons, "B7", "=B6/SQRT(B3)", fmt="0.0000")
put(ws_kons, "A8", "Kritik 95% (interpolasi Tabel 2.3)")
put(ws_kons, "B8", "=Koefisien!$B$38+(B3-Koefisien!$A$38)/(Koefisien!$A$39-Koefisien!$A$38)*(Koefisien!$B$39-Koefisien!$B$38)", fmt="0.0000")
put(ws_kons, "A9", "Kritik 99% (interpolasi Tabel 2.3)")
put(ws_kons, "B9", "=Koefisien!$C$38+(B3-Koefisien!$A$38)/(Koefisien!$A$39-Koefisien!$A$38)*(Koefisien!$C$39-Koefisien!$C$38)", fmt="0.0000")
put(ws_kons, "A10", "Kesimpulan (95%)")
put(ws_kons, "B10", '=IF(B7<B8,"KONSISTEN","TIDAK KONSISTEN")', font=BOLD)
put(ws_kons, "A11", "Kesimpulan (99%)")
put(ws_kons, "B11", '=IF(B7<B9,"KONSISTEN","TIDAK KONSISTEN")', font=BOLD)
header_row(ws_kons, 12, ["Tahun", "X (mm)", "Deviasi (X-Xbar)", "S**k (kumulatif)", "S**k / Dy"])
for i, y in enumerate(years):
    r = 13 + i
    put(ws_kons, f"A{r}", f"=Statistik_Tahunan!A{Y1+i}", box=True)
    put(ws_kons, f"B{r}", f"=Statistik_Tahunan!F{Y1+i}", fmt="0.0", box=True)
    put(ws_kons, f"C{r}", f"=B{r}-$B$4", fmt="0.0000", box=True)
    put(ws_kons, f"D{r}", f"=C{r}" if i == 0 else f"=D{r-1}+C{r}", fmt="0.0000", box=True)
    put(ws_kons, f"E{r}", f"=D{r}/$B$5", fmt="0.0000", box=True)
widths(ws_kons, {"A": 32, "B": 14, "C": 18, "D": 18, "E": 12})

# ================= 6. Frekuensi =================
put(ws_freq, "A1", "ANALISIS FREKUENSI CURAH HUJAN MAKSIMUM HARIAN TAHUNAN", font=TITLE)
put(ws_freq, "A3", "a Gumbel = S / 1,283")
put(ws_freq, "B3", "=Statistik!$B$5/1.283", fmt="0.0000")
put(ws_freq, "A4", "Xo Gumbel = X barat - 0,577.a")
put(ws_freq, "B4", "=Statistik!$B$4-0.577*B3", fmt="0.0000")
put(ws_freq, "A5", "Cs log10 (dari sheet Statistik)")
put(ws_freq, "B5", "=Statistik!$B$11", fmt="0.0000")
header_row(ws_freq, 7, ["T (tahun)", "K Normal", "XT Normal (mm)", "Yp Gumbel", "XT Gumbel (mm)",
                        "K LP3", "XT LP3 (mm)"])
KOEF_T_KN = "Koefisien!$A$44:$A$49"
KOEF_T_YG = "Koefisien!$A$53:$A$58"
KOEF_CS = "Koefisien!$A$62:$A$98"
for i, T in enumerate([2, 5, 10, 25, 50, 100]):
    r = 8 + i
    kcol = "BCDEFG"[i]  # kolom K LP3 untuk T ini di Koefisien
    p = f"MIN(IFERROR(MATCH($B$5,{KOEF_CS},1),1),36)"
    k_lp3 = (f"=INDEX(Koefisien!{kcol}$62:{kcol}$98,{p})"
             f"+($B$5-INDEX({KOEF_CS},{p}))/(INDEX({KOEF_CS},{p}+1)-INDEX({KOEF_CS},{p}))"
             f"*(INDEX(Koefisien!{kcol}$62:{kcol}$98,{p}+1)-INDEX(Koefisien!{kcol}$62:{kcol}$98,{p}))")
    put(ws_freq, f"A{r}", T, box=True)
    put(ws_freq, f"B{r}", f"=INDEX(Koefisien!$B$44:$B$49,MATCH($A{r},{KOEF_T_KN},0))", fmt="0.000", box=True)
    put(ws_freq, f"C{r}", f"=Statistik!$B$4+B{r}*Statistik!$B$5", fmt="0.000", box=True)
    put(ws_freq, f"D{r}", f"=INDEX(Koefisien!$B$53:$B$58,MATCH($A{r},{KOEF_T_YG},0))", fmt="0.000", box=True)
    put(ws_freq, f"E{r}", f"=$B$4+D{r}*$B$3", fmt="0.000", box=True)
    put(ws_freq, f"F{r}", k_lp3, fmt="0.0000", box=True)
    put(ws_freq, f"G{r}", f"=10^(Statistik!$B$9+F{r}*Statistik!$B$10)", fmt="0.000", box=True)
put(ws_freq, "A15", "Catatan: K Normal (Tabel 2.4), Yp Gumbel (Tabel 2.5), K LP3 (Tabel 2.6) di sheet Koefisien. XT Normal = Xbar + K.S ; XT Gumbel = Xo + Yp.a ; XT LP3 = 10^(rata2 log + K.S log).")
widths(ws_freq, {"A": 11, "B": 11, "C": 15, "D": 11, "E": 15, "F": 10, "G": 15})

# ================= 7. Chi_Kuadrat =================
put(ws_chi, "A1", "UJI CHI-KUADRAT PEMILIHAN DISTRIBUSI", font=TITLE)
put(ws_chi, "A2", "Kelas dibatasi R2, R5, R10, R25 (Tabel probabilitas di sheet Koefisien baris 102-106)")
dists = [("Normal", "C", 2, 6), ("Gumbel", "E", 2, 19), ("LP3", "G", 3, 32)]
kand_cells = {}
for name, fcol, P, r0 in dists:
    put(ws_chi, f"A{r0}", f"Distribusi {name}", font=BOLD)
    header_row(ws_chi, r0 + 1, ["Kelas", "Batas (mm)", "O", "E = n.p", "(O-E)^2/E"])
    bounds = [(f"x <= R2", 8, None), ("R2 < x <= R5", 9, 8), ("R5 < x <= R10", 10, 9),
              ("R10 < x <= R25", 11, 10), ("x > R25", None, 11)]
    for j, (lab, frow, prev) in enumerate(bounds):
        r = r0 + 2 + j
        put(ws_chi, f"A{r}", lab, box=True)
        if frow is not None:
            put(ws_chi, f"B{r}", f"=Frekuensi!${fcol}${frow}", fmt="0.000", box=True)
            if prev is None:
                put(ws_chi, f"C{r}", f'=COUNTIFS({XMAX},"<="&B{r})', fmt="0", box=True)
            else:
                put(ws_chi, f"C{r}", f'=COUNTIFS({XMAX},">"&B{prev},{XMAX},"<="&B{r})', fmt="0", box=True)
        else:
            put(ws_chi, f"B{r}", "-", box=True, align="center")
            put(ws_chi, f"C{r}", f'=COUNTIFS({XMAX},">"&B{prev})', fmt="0", box=True)
        put(ws_chi, f"D{r}", f"=Statistik!$B$3*Koefisien!$B${102+j}", fmt="0.000", box=True)
        put(ws_chi, f"E{r}", f"=(C{r}-D{r})^2/D{r}", fmt="0.0000", box=True)
    rs = r0 + 7  # baris ringkasan
    put(ws_chi, f"A{rs}", "chi-kuadrat hitung")
    put(ws_chi, f"B{rs}", f"=SUM(E{r0+2}:E{r0+6})", fmt="0.0000")
    put(ws_chi, f"A{rs+1}", "dk = 5-1-P")
    put(ws_chi, f"B{rs+1}", f"=4-{P}", fmt="0")
    put(ws_chi, f"A{rs+2}", "chi-kuadrat kritis")
    put(ws_chi, f"B{rs+2}", f"=INDEX(Koefisien!$B$110:$B$111,MATCH(B{rs+1},Koefisien!$A$110:$A$111,0))", fmt="0.000")
    put(ws_chi, f"A{rs+3}", "Kesimpulan")
    put(ws_chi, f"B{rs+3}", f'=IF(B{rs}<=B{rs+2},"LOLOS","GAGAL")', font=BOLD)
    put(ws_chi, f"A{rs+4}", "chi2 kandidat (999 bila gagal)")
    put(ws_chi, f"B{rs+4}", f'=IF(B{rs+3}="LOLOS",B{rs},999)', fmt="0.0000")
    kand_cells[name] = f"B{rs+4}"
put(ws_chi, "A45", "Prioritas pemilihan saat kandidat seri: LP3 (SNI 2415:2016) > Gumbel > Normal", font=FONT)
put(ws_chi, "A46", "chi2 kandidat terkecil")
put(ws_chi, "B46", f"=MIN({kand_cells['Normal']},{kand_cells['Gumbel']},{kand_cells['LP3']})", fmt="0.0000")
put(ws_chi, "A47", "Distribusi terpilih", font=BOLD)
put(ws_chi, "B47", f'=IF({kand_cells["LP3"]}=B46,"LP3",IF({kand_cells["Gumbel"]}=B46,"Gumbel",IF({kand_cells["Normal"]}=B46,"Normal","-")))', font=BOLD)
put(ws_chi, "A48", "chi2 terpilih")
put(ws_chi, "B48", f'=IF(B47="LP3",B39,IF(B47="Gumbel",B26,B13))', fmt="0.0000")
widths(ws_chi, {"A": 30, "B": 14, "C": 8, "D": 10, "E": 13})

# ================= 8. Debit_Rencana =================
put(ws_deb, "A1", "PERHITUNGAN DEBIT BANJIR RENCANA (Rasional + Mononobe)", font=TITLE)
put(ws_deb, "A2", "Sel biru = input asumsi site (ganti dengan data lapangan); sel hitam = formula otomatis.")
header_row(ws_deb, 3, ["Parameter", "Nilai", "Satuan", "Keterangan/Sumber"])
inputs = [
    ("Lo (panjang overland)", 200.0, "m", "Asumsi site", "0.0"),
    ("Ss (kemiringan)", 0.002, "m/m", "Asumsi site", "0.000"),
    ("Ld (panjang saluran)", 300.0, "m", "Asumsi site", "0.0"),
    ("n Manning", 0.011, "-", "Tabel 2.8 (saluran beton)", "0.000"),
    ("B (lebar saluran)", 0.30, "m", "Asumsi site", "0.00"),
    ("y (tinggi saluran)", 0.25, "m", "Asumsi site", "0.00"),
    ("C (koefisien limpasan)", f"=Kawasan!$B${KAW_ROW['C_atap']}", "-",
     "link sheet Kawasan (Tabel 2.7)", "0.00"),
    ("A (luas atap)", f"=Kawasan!$B${KAW_ROW['luas_atap_total']}", "m2",
     "link sheet Kawasan (1,04 ha)", "0"),
    ("th (waktu konsentrasi tandon)", 1.0, "jam", "Asumsi desain", "0.0"),
]
for i, (lab, val, sat, ket, fmt) in enumerate(inputs):
    r = 4 + i
    is_f = isinstance(val, str) and val.startswith("=")
    put(ws_deb, f"A{r}", lab, box=True)
    put(ws_deb, f"B{r}", val, font=FONT if is_f else INPUT, fmt=fmt,
        fill=None if is_f else YELLOW, box=True)
    put(ws_deb, f"C{r}", sat, box=True)
    put(ws_deb, f"D{r}", ket, box=True)
put(ws_deb, "A14", "HASIL PERHITUNGAN", font=BOLD)
header_row(ws_deb, 15, ["Besaran", "Nilai", "Satuan", "Rumus"])
res = [
    ("R24 curah hujan (T=10 th, dist. terpilih)",
     '=IF(Chi_Kuadrat!$B$47="LP3",Frekuensi!$G$10,IF(Chi_Kuadrat!$B$47="Gumbel",Frekuensi!$E$10,Frekuensi!$C$10))',
     "mm", "XT distribusi terpilih (sheet Frekuensi, T=10)", "0.000"),
    ("to (waktu konsentrasi overland)", "=0.0195*B4^0.77/B5^0.385", "menit", "Kirpich", "0.00"),
    ("V (kecepatan saluran)", "=(1/B7)*((B8*B9)/(B8+2*B9))^(2/3)*SQRT(B5)", "m/s", "Manning", "0.000"),
    ("td (waktu alir saluran)", "=B6/(60*B18)", "menit", "td = Ld / (60.V)", "0.00"),
    ("tc (waktu konsentrasi)", "=(B17+B19)/60", "jam", "tc = (to + td)/60", "0.0000"),
    ("I (intensitas hujan Mononobe)", "=(B16/24)*(24/B20)^(2/3)", "mm/jam", "rumus tesis [19]", "0.00"),
    ("Q (debit rasional)", "=0.278*B10*B21*(B11/1000000)", "m3/dtk", "Rasional: Q = 0,278.C.I.A", "0.0000"),
    ("Va (volume tandon, th=1 jam)", "=B22*B12*3600", "m3", "Va = Q.th", "0.0"),
]
for i, (lab, f, sat, ket, fmt) in enumerate(res):
    r = 16 + i
    put(ws_deb, f"A{r}", lab, box=True)
    put(ws_deb, f"B{r}", f, fmt=fmt, box=True)
    put(ws_deb, f"C{r}", sat, box=True)
    put(ws_deb, f"D{r}", ket, box=True)
put(ws_deb, "A25", "Catatan: R24 diambil dari XT T=10 tahun distribusi terpilih (hasil uji chi-kuadrat). Parameter site bersifat asumsi dan harus diganti dengan data lapangan.")
widths(ws_deb, {"A": 42, "B": 13, "C": 9, "D": 45})

# ================= 9. Kawasan (parameter + kebutuhan air) =================
put(ws_kaw, "A1", "PARAMETER KAWASAN & KEBUTUHAN AIR (sumber: tabel kawasan di data/processed/hidrologi.db)", font=TITLE)
header_row(ws_kaw, 2, ["Kunci", "Nilai", "Satuan", "Sumber"])
for kunci, nilai, satuan, sumber in kaw_rows:
    r = KAW_ROW[kunci]
    v = as_num(nilai)
    is_num = isinstance(v, float)
    put(ws_kaw, f"A{r}", kunci, box=True)
    put(ws_kaw, f"B{r}", v, font=INPUT if is_num else FONT, fmt="0.####" if is_num else None, box=True)
    put(ws_kaw, f"C{r}", satuan, box=True)
    put(ws_kaw, f"D{r}", sumber, box=True)
put(ws_kaw, "A17", "PERHITUNGAN TURUNAN (formula hidup)", font=BOLD)
header_row(ws_kaw, 18, ["Besaran", "Nilai", "Satuan", "Rumus"])
put(ws_kaw, "A19", "Q kebutuhan total [36]", box=True)
put(ws_kaw, "B19", f"=B{KAW_ROW['jumlah_unit']}*B{KAW_ROW['jiwa_per_unit']}*B{KAW_ROW['q_kebutuhan_air']}",
    fmt="0", box=True)
put(ws_kaw, "C19", "liter/hari", box=True)
put(ws_kaw, "D19", "jumlah_unit x jiwa x q", box=True)
put(ws_kaw, "A20", "Q harian", box=True)
put(ws_kaw, "B20", f"=B{R_KQL}/1000", fmt="0.000", box=True)
put(ws_kaw, "C20", "m3/hari", box=True)
put(ws_kaw, "D20", "Q kebutuhan / 1000", box=True)
put(ws_kaw, "A21", "Luas atap total", box=True)
put(ws_kaw, "B21", f"=B{KAW_ROW['luas_atap_total']}/1000000", fmt="0.000000", box=True)
put(ws_kaw, "C21", "km2", box=True)
put(ws_kaw, "A22", "Rasio luas atap / luas kawasan", box=True)
put(ws_kaw, "B22", f"=B{KAW_ROW['luas_atap_total']}/B{KAW_ROW['luas_kawasan']}", fmt="0.0%", box=True)
put(ws_kaw, "A24", "KEBUTUHAN AIR PER FRAKSI (Tesis 3.4.1)", font=BOLD)
header_row(ws_kaw, 25, ["Fraksi f", "Q x f (m3/hari)", "Kebutuhan (liter/hari)"])
for k, f in enumerate(FR_LIST):
    r = R_FR0 + k
    des = (f == FR_DES)
    put(ws_kaw, f"A{r}", f, font=INPUT, fmt="0.00", fill=YELLOW if des else None, box=True)
    put(ws_kaw, f"B{r}", f"=$B${R_KQ}*A{r}", fmt="0.000", box=True)
    put(ws_kaw, f"C{r}", f"=A{r}*$B${R_KQL}", fmt="0", box=True)
    if des:
        put(ws_kaw, f"D{r}", "<- fraksi desain", font=BOLD)
widths(ws_kaw, {"A": 26, "B": 34, "C": 15, "D": 60})

# ================= 10. Evaporasi =================
put(ws_eva, "A1", "EVAPORASI (ET0) BULANAN - ASUMSI, ganti dengan data BMKG/ERA5 (Tesis 3.3.2)", font=TITLE)
header_row(ws_eva, 2, ["Bulan", "ET0 (mm/bulan)", "Keterangan"])
for i, (b, et0, ket) in enumerate(evap_rows):
    r = 3 + i
    put(ws_eva, f"A{r}", b, fmt="0", box=True)
    put(ws_eva, f"B{r}", et0, font=INPUT, fmt="0.0", fill=YELLOW, box=True)
    put(ws_eva, f"C{r}", ket, box=True)
put(ws_eva, "A15", "TOTAL SETAHUN", font=BOLD)
put(ws_eva, "B15", "=SUM(B3:B14)", font=BOLD, fmt="0.0")
put(ws_eva, "A16", "RATA-RATA", font=BOLD)
put(ws_eva, "B16", "=AVERAGE(B3:B14)", font=BOLD, fmt="0.0")
put(ws_eva, "C16", "dipakai sheet Neraca_Air (INDEX/MATCH kolom bulan)")
widths(ws_eva, {"A": 8, "B": 17, "C": 80})

# ================= 11. Hidrolika_Pipa (iterasi envelope) =================
par = {k: (as_num(v), s, ket) for k, v, s, ket in par_rows}
put(ws_hyp, "A1", "HIDROLIKA PIPA INDUK & PER UNIT - ITERASI ENVELOPE (MANNING ALIRAN PENUH)", font=TITLE)
put(ws_hyp, "A2", "Aturan envelope: iterasi v<->td<->tc<->I<->Q<->D (12x, seed v=1 m/dtk) ber-osilasi karena umpan balik positif + pembulatan diameter diskrit; Q desain = maksimum iterasi (konservatif), D teoritis dihitung dari Q tsb lalu dibulatkan ke atas ke pipa komersial. Pipa diperlakukan sebagai saluran bulat PENUH terisi (Manning aliran penuh [29][30][38][39]), bukan aliran terbuka.")
header_row(ws_hyp, 4, ["Parameter", "Nilai", "Satuan", "Sumber/Keterangan"])

def hyp_par(label, key, r, fmt):
    v, s, ket = par[key]
    put(ws_hyp, f"A{r}", label, box=True)
    put(ws_hyp, f"B{r}", v, font=INPUT, fmt=fmt, fill=YELLOW, box=True)
    put(ws_hyp, f"C{r}", s, box=True)
    put(ws_hyp, f"D{r}", ket, box=True)

hyp_par("Lo (panjang aliran atap)", "Lo", 5, "0.0")
hyp_par("S_atap (kemiringan atap)", "S_atap", 6, "0.000")
hyp_par("Ld (panjang pipa penyalur)", "Ld", 7, "0.0")
hyp_par("S_pipa (kemiringan pipa)", "S_pipa", 8, "0.000")
hyp_par("n Manning pipa", "n_pipa", 9, "0.000")
put(ws_hyp, "A10", "to (Kirpich pada atap) [21]", box=True)
put(ws_hyp, "B10", "=0.0195*(B5/SQRT(B6))^0.77", fmt="0.0000", box=True)
put(ws_hyp, "C10", "menit", box=True)
put(ws_hyp, "D10", "to = 0,0195.(Lo/SQRT(S))^0,77", box=True)
put(ws_hyp, "A11", "A atap total", box=True)
put(ws_hyp, "B11", f"=Kawasan!$B${KAW_ROW['luas_atap_total']}", fmt="0", box=True)
put(ws_hyp, "C11", "m2", box=True)
put(ws_hyp, "D11", "link sheet Kawasan", box=True)
put(ws_hyp, "A12", "C (koefisien limpasan)", box=True)
put(ws_hyp, "B12", f"=Kawasan!$B${KAW_ROW['C_atap']}", fmt="0.00", box=True)
put(ws_hyp, "D12", "link sheet Kawasan (Tabel 2.7)", box=True)
put(ws_hyp, "A13", "A (luas atap)", box=True)
put(ws_hyp, "B13", "=B11/1000000", fmt="0.000000", box=True)
put(ws_hyp, "C13", "km2", box=True)
put(ws_hyp, "A14", "R24 curah hujan rencana (T=10 th)", box=True)
put(ws_hyp, "B14", '=IF(Chi_Kuadrat!$B$47="LP3",Frekuensi!$G$10,IF(Chi_Kuadrat!$B$47="Gumbel",Frekuensi!$E$10,Frekuensi!$C$10))',
    fmt="0.000", box=True)
put(ws_hyp, "C14", "mm", box=True)
put(ws_hyp, "D14", "XT distribusi terpilih (sheet Frekuensi/Chi_Kuadrat)", box=True)

P0 = 33
PD = f"$B${P0}:$B${P0 + len(pipa_rows) - 1}"   # kolom D (mm) tabel pipa
PA = f"$C${P0}:$C${P0 + len(pipa_rows) - 1}"   # kolom A (m2) tabel pipa
NPIPE = len(pipa_rows)

def f_dkom(expr_mm):
    return f'=INDEX({PD},MIN(COUNTIF({PD},"<"&{expr_mm})+1,{NPIPE}))'

put(ws_hyp, "A16", "ITERASI v<->td<->tc<->I<->Q<->D - pipa induk (envelope)", font=BOLD)
header_row(ws_hyp, 17, ["i", "v masuk (m/dtk)", "td (menit)", "tc (jam)", "I (mm/jam)", "Q (m3/dtk)",
                        "D teor (m)", "D kom (mm)", "A pipa (m2)", "v keluar (m/dtk)"])
for i in range(12):
    r = 18 + i
    put(ws_hyp, f"A{r}", i + 1, fmt="0", box=True)
    put(ws_hyp, f"B{r}", 1.0 if i == 0 else f"=J{r-1}", font=INPUT if i == 0 else FONT,
        fmt="0.0000", fill=YELLOW if i == 0 else None, box=True)
    put(ws_hyp, f"C{r}", f"=$B$7/(60*B{r})", fmt="0.000", box=True)
    put(ws_hyp, f"D{r}", f"=($B$10+C{r})/60", fmt="0.00000", box=True)
    put(ws_hyp, f"E{r}", f"=($B$14/24)*(24/D{r})^(2/3)", fmt="0.00", box=True)
    put(ws_hyp, f"F{r}", f"=0.278*$B$12*E{r}*$B$13", fmt="0.0000", box=True)
    put(ws_hyp, f"G{r}", f"=(F{r}*$B$9/(0.312*SQRT($B$8)))^(3/8)", fmt="0.0000", box=True)
    put(ws_hyp, f"H{r}", f_dkom(f"G{r}*1000"), fmt="0", box=True)
    put(ws_hyp, f"I{r}", f"=INDEX({PA},MATCH(H{r},{PD},0))", fmt="0.000000", box=True)
    put(ws_hyp, f"J{r}", f"=F{r}/I{r}", fmt="0.0000", box=True)
put(ws_hyp, "A31", "TABEL PIPA STANDAR (tabel pipa_standar di hidrologi.db)", font=BOLD)
header_row(ws_hyp, 32, ["Label", "D (mm)", "A (m2)"])
for i, (label, d_mm) in enumerate(pipa_rows):
    r = P0 + i
    put(ws_hyp, f"A{r}", label, box=True)
    put(ws_hyp, f"B{r}", d_mm, font=INPUT, fmt="0", box=True)
    put(ws_hyp, f"C{r}", f"=PI()*(B{r}/1000)^2/4", fmt="0.000000", box=True)

put(ws_hyp, "A49", "HASIL ENVELOPE - PIPA INDUK (desain konservatif)", font=BOLD)
header_row(ws_hyp, 50, ["Besaran", "Nilai", "Satuan", "Rumus/Keterangan"])
env = [
    ("Q desain (maks iterasi) [23]", "=MAX(F18:F29)", "m3/dtk",
     "envelope: Q = maksimum dari 12 iterasi", "0.0000"),
    ("I desain (Mononobe) [19]", "=INDEX($E$18:$E$29,MATCH(B51,$F$18:$F$29,0))", "mm/jam",
     "I pada baris Q maks", "0.00"),
    ("td [22]", "=INDEX($C$18:$C$29,MATCH(B51,$F$18:$F$29,0))", "menit", "td = Ld / (60.v)", "0.000"),
    ("tc [20]", "=INDEX($D$18:$D$29,MATCH(B51,$F$18:$F$29,0))", "jam", "tc = (to + td) / 60", "0.00000"),
    ("D teoritis [38]", "=(B51*$B$9/(0.312*SQRT($B$8)))^(3/8)", "m", "dari Q desain", "0.0000"),
    ("D komersial", f_dkom("B55*1000"), "mm", "dibulatkan ke atas ke ukuran pipa standar", "0"),
    ("A pipa", f"=INDEX({PA},MATCH(B56,{PD},0))", "m2", "pada tabel pipa standar", "0.000000"),
    ("v pipa [39]", "=B51/B57", "m/dtk", "v = Q / A", "0.0000"),
    ("Kapasitas pipa (Manning penuh)", "=(1/$B$9)*B57*(B56/1000/4)^(2/3)*SQRT($B$8)", "m3/dtk",
     "Q = (1/n).A.(D/4)^(2/3).S^(1/2)", "0.0000"),
    ("Cek kapasitas", '=IF(B59>=B51,"AMAN","TIDAK AMAN")', "-", "kapasitas >= Q desain", None),
    ("D pipa pelimpah (overflow)", "=B56", "mm", "untuk Q desain (sama dgn induk)", "0"),
]
for i, (lab, fml, sat, ket, fmt) in enumerate(env):
    r = 51 + i
    put(ws_hyp, f"A{r}", lab, box=True)
    put(ws_hyp, f"B{r}", fml, fmt=fmt, font=BOLD if lab.startswith("Q desain") else FONT, box=True)
    put(ws_hyp, f"C{r}", sat, box=True)
    put(ws_hyp, f"D{r}", ket, box=True)

put(ws_hyp, "A63", "PIPA PENYALUR PER UNIT, TALANG & BAK PENAMPUNG", font=BOLD)
header_row(ws_hyp, 64, ["Besaran", "Nilai", "Satuan", "Rumus/Keterangan"])
unit = [
    ("Luas atap per unit", f"=Kawasan!$B${KAW_ROW['luas_atap_per_unit']}", "m2",
     "link sheet Kawasan", "0.0"),
    ("Q per unit", "=0.278*$B$12*$B$52*(B65/1000000)", "m3/dtk", "Rasional pada atap 1 unit", "0.00000"),
    ("D teoritis unit [38]", "=(B66*$B$9/(0.312*SQRT($B$8)))^(3/8)", "m", "Manning penuh", "0.0000"),
    ("D komersial unit", f_dkom("B67*1000"), "mm", "pipa penyalur per unit (downspout)", "0"),
    ("A pipa unit", f"=INDEX({PA},MATCH(B68,{PD},0))", "m2", "tabel pipa standar", "0.000000"),
    ("v unit [39]", "=B66/B69", "m/dtk", "v = Q / A", "0.0000"),
    ("b talang", 0.15, "m", "Asumsi desain (cerminan analisis_desain.py)", "0.00"),
    ("h talang", 0.10, "m", "Asumsi desain", "0.00"),
    ("S talang", 0.005, "m/m", "Asumsi desain", "0.000"),
    ("n talang", 0.012, "-", "Tabel 2.8 - asumsi talang (aliran terbuka)", "0.000"),
    ("A talang", "=B71*B72", "m2", "A = b . h", "0.0000"),
    ("P basah talang", "=B71+2*B72", "m", "P = b + 2h", "0.0000"),
    ("R hidraulik talang", "=B75/B76", "m", "R = A / P", "0.0000"),
    ("Q kapasitas talang [29][30]", "=(1/B74)*B75*B77^(2/3)*SQRT(B73)", "m3/dtk",
     "Manning ALIRAN TERBUKA (talang terbuka)", "0.00000"),
    ("v talang", "=B78/B75", "m/dtk", "v = Q / A", "0.0000"),
    ("V bak penampung unit",
     f"=CEILING(Kawasan!$B${KAW_ROW['jiwa_per_unit']}*Kawasan!$B${KAW_ROW['q_kebutuhan_air']}*Kawasan!$B${KAW_ROW['fraksi_desain']}*1.5/1000,0.1)",
     "m3", "1,5x kebutuhan harian unit (asumsi terdokumentasi)", "0.0"),
]
for i, (lab, val, sat, ket, fmt) in enumerate(unit):
    r = 65 + i
    is_f = isinstance(val, str) and val.startswith("=")
    put(ws_hyp, f"A{r}", lab, box=True)
    put(ws_hyp, f"B{r}", val, font=FONT if is_f else INPUT, fmt=fmt,
        fill=None if is_f else YELLOW, box=True)
    put(ws_hyp, f"C{r}", sat, box=True)
    put(ws_hyp, f"D{r}", ket, box=True)
widths(ws_hyp, {"A": 34, "B": 15, "C": 14, "D": 20, "E": 12, "F": 12, "G": 12, "H": 12, "I": 12, "J": 13})

# ================= 12. Neraca_Air (Rippl, 5 fraksi) =================
put(ws_nrc, "A1", "NERACA AIR BULANAN - 5 FRAKSI KEBUTUHAN (Rippl [27], 2012-2025)", font=TITLE)
put(ws_nrc, "A2", "E = ET0 x luas kolam kriteria atenuasi Va (aturan pass-1 terdokumentasi, lihat Desain_Kolam); kolom M-N = simulasi tampungan terbatas V_desain [26][28]; blok fraksi desain punya kolom O-X utk pass-2/pass-3 (umpan balik evaporasi).")
HDR_N = ["Tahun", "Bulan", "R (mm)", "n hari", "ET0 (mm)", "Supply (m3) [24]", "Demand (m3) [25]",
         "Evaporasi E (m3)", "Net (m3)", "K kumulatif (m3)", "Sp (m3)", "Defisit (m3)",
         "S (m3) [26]", "Terpenuhi"]
HDR2 = ["E pass-2", "Net pass-2", "K pass-2", "Sp pass-2", "Defisit pass-2",
        "E pass-3", "Net pass-3", "K pass-3", "Sp pass-3", "Defisit pass-3"]
KLM_AP0 = "Desain_Kolam!$B$16"
KLM_VDES = "Desain_Kolam!$B$21"
KLM_APD = "Desain_Kolam!$B$24"
KLM_AP2 = "Desain_Kolam!$B$34"
NB = len(bulan_rows)
VS, REL, NPN, TNET = {}, {}, {}, {}
VS2 = VS3 = None
row = 4
for k, f in enumerate(FR_LIST):
    r0 = row
    put(ws_nrc, f"A{r0}", f"Fraksi f = {f:.2f}" + ("   (FRAKSI DESAIN)" if k == KDES else ""),
        font=BOLD, fill=YELLOW if k == KDES else None)
    header_row(ws_nrc, r0 + 1, HDR_N)
    if k == KDES:
        header_row(ws_nrc, r0 + 1, HDR2, start_col=15)
    rd = r0 + 2
    fr_cell = f"Kawasan!$B${R_FR0 + k}"
    for i, (y, b, mm, nd) in enumerate(bulan_rows):
        rr = rd + i
        put(ws_nrc, f"A{rr}", y, fmt="0", box=True)
        put(ws_nrc, f"B{rr}", b, fmt="0", box=True)
        put(ws_nrc, f"C{rr}", mm, fmt="0.0", box=True)
        put(ws_nrc, f"D{rr}", nd, fmt="0", box=True)
        put(ws_nrc, f"E{rr}", f"=INDEX(Evaporasi!$B$3:$B$14,MATCH(B{rr},Evaporasi!$A$3:$A$14,0))",
            fmt="0.0", box=True)
        put(ws_nrc, f"F{rr}",
            f"=Kawasan!$B${KAW_ROW['C_atap']}*Kawasan!$B${KAW_ROW['luas_atap_total']}*C{rr}/1000",
            fmt="0.00", box=True)
        put(ws_nrc, f"G{rr}", f"={fr_cell}*D{rr}", fmt="0.00", box=True)
        put(ws_nrc, f"H{rr}", f"=E{rr}*{KLM_AP0}/1000", fmt="0.00", box=True)
        put(ws_nrc, f"I{rr}", f"=F{rr}-G{rr}-H{rr}", fmt="0.00", box=True)
        put(ws_nrc, f"J{rr}", f"=I{rr}" if i == 0 else f"=J{rr-1}+I{rr}", fmt="0.00", box=True)
        put(ws_nrc, f"K{rr}", f"=MAX(0,J{rr})" if i == 0 else f"=MAX(K{rr-1},J{rr})", fmt="0.00", box=True)
        put(ws_nrc, f"L{rr}", f"=K{rr}-J{rr}", fmt="0.00", box=True)
        put(ws_nrc, f"M{rr}",
            f"=MIN({KLM_VDES},MAX(0,F{rr}-H{rr}-G{rr}))" if i == 0
            else f"=MIN({KLM_VDES},MAX(0,M{rr-1}+F{rr}-H{rr}-G{rr}))", fmt="0.00", box=True)
        put(ws_nrc, f"N{rr}",
            f"=IF(F{rr}-H{rr}>=G{rr},1,0)" if i == 0
            else f"=IF(M{rr-1}+F{rr}-H{rr}>=G{rr},1,0)", fmt="0", box=True)
        if k == KDES:
            put(ws_nrc, f"O{rr}", f"=E{rr}*{KLM_APD}/1000", fmt="0.00", box=True)
            put(ws_nrc, f"P{rr}", f"=F{rr}-G{rr}-O{rr}", fmt="0.00", box=True)
            put(ws_nrc, f"Q{rr}", f"=P{rr}" if i == 0 else f"=Q{rr-1}+P{rr}", fmt="0.00", box=True)
            put(ws_nrc, f"R{rr}", f"=MAX(0,Q{rr})" if i == 0 else f"=MAX(R{rr-1},Q{rr})", fmt="0.00", box=True)
            put(ws_nrc, f"S{rr}", f"=R{rr}-Q{rr}", fmt="0.00", box=True)
            put(ws_nrc, f"T{rr}", f"=E{rr}*{KLM_AP2}/1000", fmt="0.00", box=True)
            put(ws_nrc, f"U{rr}", f"=F{rr}-G{rr}-T{rr}", fmt="0.00", box=True)
            put(ws_nrc, f"V{rr}", f"=U{rr}" if i == 0 else f"=V{rr-1}+U{rr}", fmt="0.00", box=True)
            put(ws_nrc, f"W{rr}", f"=MAX(0,V{rr})" if i == 0 else f"=MAX(W{rr-1},V{rr})", fmt="0.00", box=True)
            put(ws_nrc, f"X{rr}", f"=W{rr}-V{rr}", fmt="0.00", box=True)
    re_ = rd + NB - 1
    s = re_ + 1

    def summ(label, formula, srow, fmt="0.00"):
        ws_nrc.merge_cells(f"A{srow}:D{srow}")
        put(ws_nrc, f"A{srow}", label, font=BOLD, box=True)
        put(ws_nrc, f"E{srow}", formula, font=BOLD, fmt=fmt, box=True)

    summ(f"Vs fraksi {f:.2f} (m3) [27]", f"=MAX(L{rd}:L{re_})", s)
    summ("Reliability (%) [28]", f"=100*SUM(N{rd}:N{re_})/COUNT(N{rd}:N{re_})", s + 1, "0.0")
    summ(f"Bulan terpenuhi (dari {NB})", f"=SUM(N{rd}:N{re_})", s + 2, "0")
    summ("Total net kumulatif (m3)", f"=J{re_}", s + 3)
    VS[k] = f"Neraca_Air!$E${s}"
    REL[k] = f"Neraca_Air!$E${s+1}"
    NPN[k] = f"Neraca_Air!$E${s+2}"
    TNET[k] = f"Neraca_Air!$E${s+3}"
    nxt = s + 4
    if k == KDES:
        summ("Vs pass-2 (m3)", f"=MAX(S{rd}:S{re_})", s + 4)
        summ("Vs pass-3 (m3)", f"=MAX(X{rd}:X{re_})", s + 5)
        VS2 = f"Neraca_Air!$E${s+4}"
        VS3 = f"Neraca_Air!$E${s+5}"
        nxt = s + 6
    row = nxt + 1
ws_nrc.freeze_panes = "A3"
widths(ws_nrc, {"A": 9, "B": 7, "C": 9, "D": 8, "E": 11, "F": 14, "G": 14, "H": 14, "I": 12,
                "J": 15, "K": 11, "L": 12, "M": 12, "N": 11, "O": 11, "P": 12, "Q": 12,
                "R": 11, "S": 13, "T": 11, "U": 12, "V": 12, "W": 11, "X": 13})

# ================= 13. Desain_Kolam =================
put(ws_klm, "A1", "DESAIN KOLAM RETENSI - DIMENSI, FREEBOARD & SENSITIVITAS", font=TITLE)
put(ws_klm, "A2", "Urutan: Va [32] -> neraca pass-1 (E pada Ap Va) -> Vs [27] -> V desain [33] -> dimensi [34] -> pass-2/pass-3 (umpan balik evaporasi). Dimensi dibulatkan ke atas kelipatan 0,5 m.")
header_row(ws_klm, 4, ["Parameter", "Nilai", "Satuan", "Sumber/Keterangan"])
put(ws_klm, "A5", "he (kedalaman efektif kolam)", box=True)
put(ws_klm, "B5", par["he_kolam"][0], font=INPUT, fmt="0.00", fill=YELLOW, box=True)
put(ws_klm, "C5", par["he_kolam"][1], box=True)
put(ws_klm, "D5", par["he_kolam"][2], box=True)
put(ws_klm, "A6", "hf (freeboard)", box=True)
put(ws_klm, "B6", f"=Kawasan!$B${KAW_ROW['freeboard']}", fmt="0.00", box=True)
put(ws_klm, "C6", "m", box=True)
put(ws_klm, "D6", "link sheet Kawasan (Tesis 2.7)", box=True)
put(ws_klm, "A7", "th (durasi hujan efektif)", box=True)
put(ws_klm, "B7", f"=Kawasan!$B${KAW_ROW['th_durasi_efektif']}", fmt="0.0", box=True)
put(ws_klm, "C7", "jam", box=True)
put(ws_klm, "D7", "link sheet Kawasan (Tesis 3.4.3)", box=True)
put(ws_klm, "A8", "Q desain", box=True)
put(ws_klm, "B8", "=Hidrolika_Pipa!$B$51", fmt="0.0000", box=True)
put(ws_klm, "C8", "m3/dtk", box=True)
put(ws_klm, "D8", "link Hidrolika_Pipa (envelope)", box=True)
put(ws_klm, "A9", "Ap_kolam (parameter DB)", box=True)
put(ws_klm, "B9", par["Ap_kolam"][0], font=INPUT, fmt="0.00", fill=YELLOW, box=True)
put(ws_klm, "C9", "m2", box=True)
put(ws_klm, "D9", "parameter_desain - dipakai utk cek konsistensi", box=True)

put(ws_klm, "A11", "KRITERIA ATENUASI Va [32]", font=BOLD)
header_row(ws_klm, 12, ["Besaran", "Nilai", "Satuan", "Rumus/Keterangan"])
put(ws_klm, "A13", "Va (volume atenuasi)", box=True)
put(ws_klm, "B13", "=B8*B7*3600", fmt="0.00", box=True)
put(ws_klm, "C13", "m3", box=True)
put(ws_klm, "D13", "Va = Q . th . 3600 [32]", box=True)
put(ws_klm, "A14", "l (lebar kolam Va)", box=True)
put(ws_klm, "B14", "=CEILING(SQRT(B13/B5),0.5)", fmt="0.0", box=True)
put(ws_klm, "C14", "m", box=True)
put(ws_klm, "D14", "dibulatkan ke atas 0,5 m", box=True)
put(ws_klm, "A15", "p (panjang kolam Va)", box=True)
put(ws_klm, "B15", "=CEILING(B13/(B5*B14),0.5)", fmt="0.0", box=True)
put(ws_klm, "C15", "m", box=True)
put(ws_klm, "A16", "Ap kriteria atenuasi", box=True)
put(ws_klm, "B16", "=B14*B15", fmt="0.00", box=True)
put(ws_klm, "C16", "m2", box=True)
put(ws_klm, "D16", "basis E neraca pass-1 (Neraca_Air kolom H)", box=True)

put(ws_klm, "A18", "NERACA PASS-1 & DIMENSI KOLAM (fraksi desain)", font=BOLD)
header_row(ws_klm, 19, ["Besaran", "Nilai", "Satuan", "Rumus/Keterangan"])
put(ws_klm, "A20", "Vs pass-1 [27]", box=True)
put(ws_klm, "B20", f"={VS[KDES]}", fmt="0.00", box=True)
put(ws_klm, "C20", "m3", box=True)
put(ws_klm, "D20", "MAX defisit, sheet Neraca_Air", box=True)
put(ws_klm, "A21", "V desain [33]", font=BOLD, box=True)
put(ws_klm, "B21", "=MAX(B20,B13)", font=BOLD, fmt="0.00", box=True)
put(ws_klm, "C21", "m3", box=True)
put(ws_klm, "D21", "maks(Vs, Va)", box=True)
put(ws_klm, "A22", "l (lebar kolam)", box=True)
put(ws_klm, "B22", "=CEILING(SQRT(B21/B5),0.5)", fmt="0.0", box=True)
put(ws_klm, "C22", "m", box=True)
put(ws_klm, "A23", "p (panjang kolam)", box=True)
put(ws_klm, "B23", "=CEILING(B21/(B5*B22),0.5)", fmt="0.0", box=True)
put(ws_klm, "C23", "m", box=True)
put(ws_klm, "A24", "Ap hasil desain", box=True)
put(ws_klm, "B24", "=B22*B23", fmt="0.00", box=True)
put(ws_klm, "C24", "m2", box=True)
put(ws_klm, "D24", "basis E pass-2 (Neraca_Air kolom O)", box=True)
put(ws_klm, "A25", "V kolam [34]", box=True)
put(ws_klm, "B25", "=B23*B22*B5", fmt="0.00", box=True)
put(ws_klm, "C25", "m3", box=True)
put(ws_klm, "D25", "V = p . l . he", box=True)
put(ws_klm, "A26", "h total [35]", box=True)
put(ws_klm, "B26", "=B5+B6", fmt="0.00", box=True)
put(ws_klm, "C26", "m", box=True)
put(ws_klm, "D26", "he + hf", box=True)

put(ws_klm, "A28", "UMPAN BALIK EVAPORASI (pass-2 & pass-3)", font=BOLD)
header_row(ws_klm, 29, ["Besaran", "Nilai", "Satuan", "Rumus/Keterangan"])
put(ws_klm, "A30", "Vs pass-2", box=True)
put(ws_klm, "B30", f"={VS2}", fmt="0.00", box=True)
put(ws_klm, "C30", "m3", box=True)
put(ws_klm, "D30", "E pada Ap hasil desain (Neraca_Air O-S)", box=True)
put(ws_klm, "A31", "V2 = maks(Vs pass-2, Va)", box=True)
put(ws_klm, "B31", "=MAX(B30,B13)", fmt="0.00", box=True)
put(ws_klm, "C31", "m3", box=True)
put(ws_klm, "A32", "l2", box=True)
put(ws_klm, "B32", "=CEILING(SQRT(B31/B5),0.5)", fmt="0.0", box=True)
put(ws_klm, "C32", "m", box=True)
put(ws_klm, "A33", "p2", box=True)
put(ws_klm, "B33", "=CEILING(B31/(B5*B32),0.5)", fmt="0.0", box=True)
put(ws_klm, "C33", "m", box=True)
put(ws_klm, "A34", "Ap2", box=True)
put(ws_klm, "B34", "=B32*B33", fmt="0.00", box=True)
put(ws_klm, "C34", "m2", box=True)
put(ws_klm, "D34", "basis E pass-3 (Neraca_Air kolom T)", box=True)
put(ws_klm, "A35", "Vs pass-3", box=True)
put(ws_klm, "B35", f"={VS3}", fmt="0.00", box=True)
put(ws_klm, "C35", "m3", box=True)
put(ws_klm, "D35", "E pada Ap2 - divergen bila luas kolam besar (catatan Tesis)", box=True)

put(ws_klm, "A37", "CEK KONSISTENSI parameter_desain.Ap_kolam", font=BOLD)
header_row(ws_klm, 38, ["Cek", "Nilai", "Satuan", "Keterangan"])
put(ws_klm, "A39", "Ap kriteria (basis E neraca)", box=True)
put(ws_klm, "B39", "=B16", fmt="0.00", box=True)
put(ws_klm, "C39", "m2", box=True)
put(ws_klm, "A40", "Ap hasil desain", box=True)
put(ws_klm, "B40", "=B24", fmt="0.00", box=True)
put(ws_klm, "C40", "m2", box=True)
put(ws_klm, "A41", "Selisih hasil desain - Ap DB", box=True)
put(ws_klm, "B41", "=B40-B9", fmt="0.00", box=True)
put(ws_klm, "C41", "m2", box=True)
put(ws_klm, "A42", "Status konsistensi", box=True)
put(ws_klm, "B42", '=IF(ABS(B41)<=0.05*B9,"KONSISTEN (<=5%)","UPDATE parameter_desain.Ap_kolam")',
    font=BOLD, box=True)

put(ws_klm, "A44", "SENSITIVITAS Va terhadap th (Tesis 3.4.3)", font=BOLD)
header_row(ws_klm, 45, ["th (jam)", "Va (m3)"])
for i, th in enumerate([0.5, 1.0, 1.5, 2.0, 3.0]):
    r = 46 + i
    put(ws_klm, f"A{r}", th, font=INPUT, fmt="0.0", fill=YELLOW, box=True)
    put(ws_klm, f"B{r}", f"=$B$8*A{r}*3600", fmt="0.00", box=True)

put(ws_klm, "A52", "RINGKASAN NERACA PER FRAKSI [27][28]", font=BOLD)
header_row(ws_klm, 53, ["Fraksi", "Vs (m3)", "Reliability (%)", "Terpenuhi (bln)", "Total net (m3)"])
for k, f in enumerate(FR_LIST):
    r = 54 + k
    put(ws_klm, f"A{r}", f"=Kawasan!$A${R_FR0 + k}", fmt="0.00", box=True)
    put(ws_klm, f"B{r}", f"={VS[k]}", fmt="0.00", box=True)
    put(ws_klm, f"C{r}", f"={REL[k]}", fmt="0.0",
        fill=YELLOW if k == KDES else None, box=True)
    put(ws_klm, f"D{r}", f"={NPN[k]}", fmt="0", box=True)
    put(ws_klm, f"E{r}", f"={TNET[k]}", fmt="0.00", box=True)
put(ws_klm, "A60", "Catatan: fraksi desain 0,65 (highlight kuning). Pass-2/pass-3 memperlihatkan umpan balik evaporasi: neraca tahunan berubah negatif bila luas kolam melebihi ~4.800 m2 -> Vs terus tumbuh (defisit kritis 32 bulan Sep-2017 s/d Apr-2020).")
widths(ws_klm, {"A": 34, "B": 15, "C": 16, "D": 58, "E": 15})

# ================= 14. Koefisien =================
put(ws_koef, "A1", "TABEL KOEFISIEN DAN NILAI KRITIS (referensi)", font=TITLE)
put(ws_koef, "A3", "Tabel 2.2 Nilai kritis distribusi t (uji-t) - Sumber: Proposal Tesis Tabel 2.2", font=BOLD)
header_row(ws_koef, 4, ["dk", "t (satu arah, 5%)", "t (dua arah, 5%)"])
t1 = [6.314, 2.920, 2.353, 2.132, 2.015, 1.943, 1.895, 1.860, 1.833, 1.812,
      1.796, 1.782, 1.771, 1.761, 1.753, 1.746, 1.740, 1.734, 1.729, 1.725,
      1.721, 1.717, 1.714, 1.711, 1.708, 1.706, 1.703, 1.701, 1.699, 1.697]
t2 = [12.706, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262, 2.228,
      2.201, 2.179, 2.160, 2.145, 2.131, 2.120, 2.110, 2.101, 2.093, 2.086,
      2.080, 2.074, 2.069, 2.064, 2.060, 2.056, 2.052, 2.048, 2.045, 2.042]
for i in range(30):
    r = 5 + i
    put(ws_koef, f"A{r}", i + 1, fmt="0", box=True)
    put(ws_koef, f"B{r}", t1[i], fmt="0.000", box=True)
    put(ws_koef, f"C{r}", t2[i], fmt="0.000", box=True)
put(ws_koef, "A36", "Tabel 2.3 Nilai kritik Q/SQRT(n) - Sumber: Proposal Tesis Tabel 2.3", font=BOLD)
header_row(ws_koef, 37, ["n", "95%", "99%"])
for i, (n, q95, q99) in enumerate([(10, 1.14, 1.29), (20, 1.22, 1.42)]):
    r = 38 + i
    put(ws_koef, f"A{r}", n, fmt="0", box=True)
    put(ws_koef, f"B{r}", q95, fmt="0.00", box=True)
    put(ws_koef, f"C{r}", q99, fmt="0.00", box=True)
put(ws_koef, "A40", "Untuk n di antaranya dipakai interpolasi linear.")
put(ws_koef, "A42", "Tabel 2.4 Variabel reduksi Normal (Kp) - Sumber: Proposal Tesis Tabel 2.4", font=BOLD)
header_row(ws_koef, 43, ["T (tahun)", "Kp"])
for i, (T, k) in enumerate([(2, 0.00), (5, 0.84), (10, 1.28), (25, 1.64), (50, 2.05), (100, 2.33)]):
    r = 44 + i
    put(ws_koef, f"A{r}", T, fmt="0", box=True)
    put(ws_koef, f"B{r}", k, fmt="0.000", box=True)
put(ws_koef, "A51", "Tabel 2.5 Variabel reduksi Gumbel Tipe I (Yp) - Sumber: Proposal Tesis Tabel 2.5", font=BOLD)
header_row(ws_koef, 52, ["T (tahun)", "Yp"])
for i, (T, y) in enumerate([(2, 0.366), (5, 1.510), (10, 2.250), (25, 3.900), (50, 4.600), (100, 5.290)]):
    r = 53 + i
    put(ws_koef, f"A{r}", T, fmt="0", box=True)
    put(ws_koef, f"B{r}", y, fmt="0.000", box=True)
put(ws_koef, "A60", "Tabel 2.6 Koefisien K Log Pearson III - Sumber: Proposal Tesis Tabel 2.6 (Cs menaik untuk interpolasi)", font=BOLD)
header_row(ws_koef, 61, ["Cs", "T=2", "T=5", "T=10", "T=25", "T=50", "T=100"])
lp3 = [
    (-3.0, [0.396, 0.636, 0.660, 0.666, 0.666, 0.667]),
    (-2.5, [0.360, 0.711, 0.771, 0.793, 0.798, 0.799]),
    (-2.2, [0.330, 0.752, 0.844, 0.888, 0.900, 0.905]),
    (-2.0, [0.307, 0.777, 0.895, 0.959, 0.980, 0.990]),
    (-1.8, [0.282, 0.799, 0.945, 1.035, 1.069, 1.087]),
    (-1.6, [0.254, 0.817, 0.994, 1.116, 1.166, 1.197]),
    (-1.4, [0.225, 0.832, 1.041, 1.198, 1.270, 1.318]),
    (-1.2, [0.195, 0.844, 1.086, 1.282, 1.379, 1.449]),
    (-1.0, [0.164, 0.852, 1.128, 1.366, 1.492, 1.588]),
    (-0.9, [0.148, 0.854, 1.147, 1.407, 1.549, 1.660]),
    (-0.8, [0.132, 0.856, 1.166, 1.448, 1.606, 1.733]),
    (-0.7, [0.116, 0.857, 1.183, 1.488, 1.663, 1.806]),
    (-0.6, [0.099, 0.857, 1.200, 1.528, 1.720, 1.880]),
    (-0.5, [0.083, 0.856, 1.216, 1.567, 1.777, 1.955]),
    (-0.4, [0.066, 0.855, 1.231, 1.606, 1.834, 2.029]),
    (-0.3, [0.050, 0.853, 1.245, 1.643, 1.890, 2.104]),
    (-0.2, [0.033, 0.850, 1.258, 1.680, 1.945, 2.178]),
    (-0.1, [0.017, 0.846, 1.270, 1.716, 2.000, 2.252]),
    (0.0, [0.000, 0.842, 1.282, 1.751, 2.054, 2.326]),
    (0.1, [-0.017, 0.836, 1.292, 1.785, 2.107, 2.400]),
    (0.2, [-0.033, 0.830, 1.301, 1.818, 2.159, 2.472]),
    (0.3, [-0.050, 0.824, 1.309, 1.849, 2.211, 2.544]),
    (0.4, [-0.066, 0.816, 1.317, 1.880, 2.261, 2.615]),
    (0.5, [-0.083, 0.808, 1.323, 1.910, 2.311, 2.686]),
    (0.6, [-0.099, 0.800, 1.328, 1.939, 2.359, 2.755]),
    (0.7, [-0.116, 0.790, 1.333, 1.967, 2.407, 2.824]),
    (0.8, [-0.132, 0.780, 1.336, 1.998, 2.453, 2.891]),
    (0.9, [-0.148, 0.769, 1.339, 2.018, 2.498, 2.957]),
    (1.0, [-0.164, 0.758, 1.340, 2.043, 2.542, 3.022]),
    (1.2, [-0.195, 0.732, 1.340, 2.087, 2.626, 3.149]),
    (1.4, [-0.225, 0.705, 1.337, 2.128, 2.706, 3.271]),
    (1.6, [-0.254, 0.675, 1.329, 2.163, 2.780, 3.388]),
    (1.8, [-0.282, 0.643, 1.318, 2.193, 2.848, 3.499]),
    (2.0, [-0.307, 0.609, 1.302, 2.219, 2.912, 3.605]),
    (2.2, [-0.330, 0.574, 1.284, 2.240, 2.970, 3.705]),
    (2.5, [-0.360, 0.518, 1.250, 2.262, 3.048, 3.845]),
    (3.0, [-0.396, 0.420, 1.180, 2.278, 3.152, 4.051]),
]
for i, (cs, ks) in enumerate(lp3):
    r = 62 + i
    put(ws_koef, f"A{r}", cs, fmt="0.0", box=True)
    for j, k in enumerate(ks):
        put(ws_koef, f"{'BCDEFG'[j]}{r}", k, fmt="0.000", box=True)
put(ws_koef, "A100", "Probabilitas kelas uji chi-kuadrat (5 kelas dibatasi R2, R5, R10, R25)", font=BOLD)
header_row(ws_koef, 101, ["Kelas", "p"])
for j, (lab, p) in enumerate([("x <= R2", 0.50), ("R2 < x <= R5", 0.20), ("R5 < x <= R10", 0.10),
                              ("R10 < x <= R25", 0.06), ("x > R25", 0.04)]):
    r = 102 + j
    put(ws_koef, f"A{r}", lab, box=True)
    put(ws_koef, f"B{r}", p, fmt="0.00", box=True)
put(ws_koef, "A108", "Nilai kritik chi-kuadrat", font=BOLD)
header_row(ws_koef, 109, ["df", "Kritik"])
for j, (df, k) in enumerate([(1, 3.841), (2, 5.991)]):
    r = 110 + j
    put(ws_koef, f"A{r}", df, fmt="0", box=True)
    put(ws_koef, f"B{r}", k, fmt="0.000", box=True)
widths(ws_koef, {"A": 14, "B": 18, "C": 18, "D": 10, "E": 10, "F": 10, "G": 10})

wb.save(OUT)
print(f"[ok] {OUT} ({NROW} baris data, {len(years)} tahun)")
