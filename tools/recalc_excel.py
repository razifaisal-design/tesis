# -*- coding: utf-8 -*-
"""Recalc workbook Excel via LibreOffice headless -> cached values (formula tetap utuh).

Pakai:  python tools/recalc_excel.py [path/file.xlsx]
Default: data/processed/Perhitungan_Hidrologi.xlsx
Cari soffice di PATH lalu beberapa lokasi umum (macOS lokal & SSD eksternal).
Jika LibreOffice tidak ada, workbook tetap sah: Excel/Calc menghitung ulang
semua formula saat file dibuka."""
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
XLSX = (Path(sys.argv[1]) if len(sys.argv) > 1
        else ROOT / "data" / "processed" / "Perhitungan_Hidrologi.xlsx")

SOFFICE_CANDIDATES = [
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    "/Volumes/Lexar/APPS/LibreOffice.app/Contents/MacOS/soffice",
]


def find_soffice():
    p = shutil.which("soffice") or shutil.which("libreoffice")  # Linux pakai nama 'libreoffice'
    if p:
        return p
    for c in SOFFICE_CANDIDATES:
        if Path(c).exists():
            return c
    return None


def main():
    if not XLSX.exists():
        sys.exit(f"[gagal] file tidak ada: {XLSX} (jalankan tools/buat_excel.py dulu)")
    soffice = find_soffice()
    if not soffice:
        print("[lewati] soffice/LibreOffice tidak ditemukan - workbook tetap valid, "
              "Excel akan recalc saat dibuka")
        return
    with tempfile.TemporaryDirectory() as td:
        prof, out = Path(td) / "prof", Path(td) / "out"
        out.mkdir()
        r = subprocess.run(
            [soffice, "--headless", "--norestore",
             f"-env:UserInstallation=file://{prof}",
             "--convert-to", "xlsx", "--outdir", str(out), str(XLSX)],
            capture_output=True, text=True, timeout=600)
        hasil = out / XLSX.name
        if not hasil.exists():
            sys.exit(f"[gagal] konversi tidak menghasilkan file:\n{r.stdout}\n{r.stderr}")
        shutil.copy(hasil, XLSX)
    print(f"[ok] recalc {XLSX} (cached values dibakar, formula tetap utuh)")


if __name__ == "__main__":
    main()
