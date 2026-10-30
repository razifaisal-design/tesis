#!/usr/bin/env python3
"""Kirim berkas naskah tesis ke Telegram via Bot API (sendDocument).

Kredensial TIDAK disimpan di skrip ini. Isi lewat environment variable:

    export TELEGRAM_BOT_TOKEN="123456:ABC..."     # dari @BotFather
    export TELEGRAM_CHAT_ID="123456789"           # id chat/group tujuan
    python3 tools/kirim_telegram.py               # kirim berkas bawaan
    python3 tools/kirim_telegram.py a.docx b.docx # atau berkas pilihan

Opsi lain:
    python3 tools/kirim_telegram.py --zip          # kirim satu file .zip
    python3 tools/kirim_telegram.py --list         # lihat berkas yang akan dikirim

Catatan: bot harus sudah pernah di-/start di chat tujuan, dan untuk grup bot
harus menjadi anggota.
"""

import argparse
import os
import sys
import zipfile
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
MAN = ROOT / "manuscript"

DEFAULT_FILES = [
    "BAB_III_REVISI.docx",
    "BAB_IV_HASIL_DAN_PEMBAHASAN.docx",
    "LAMPIRAN_BAB_IV.docx",
    "BAB_V_KESIMPULAN.docx",
]
ZIP_NAME = MAN / "Naskah_Tesis_Bab-III-IV-V_Lampiran.zip"


def buat_zip():
    with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as z:
        for name in DEFAULT_FILES:
            p = MAN / name
            if p.exists():
                z.write(p, arcname=name)
    return ZIP_NAME


def kirim(token, chat_id, path):
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    with open(path, "rb") as fh:
        r = requests.post(url, data={"chat_id": chat_id},
                          files={"document": (path.name, fh)}, timeout=120)
    ok = r.status_code == 200 and r.json().get("ok")
    print(("  OK   " if ok else "  GAGAL ") + path.name +
          ("" if ok else f"  -> {r.status_code} {r.text[:200]}"))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*", help="berkas yang dikirim (default: 4 naskah)")
    ap.add_argument("--zip", action="store_true", help="kirim satu berkas .zip")
    ap.add_argument("--list", action="store_true", help="tampilkan berkas target")
    ap.add_argument("--token", default=os.environ.get("TELEGRAM_BOT_TOKEN"))
    ap.add_argument("--chat", default=os.environ.get("TELEGRAM_CHAT_ID"))
    a = ap.parse_args()

    if a.zip:
        targets = [buat_zip()]
    elif a.files:
        targets = [Path(f) for f in a.files]
    else:
        targets = [MAN / f for f in DEFAULT_FILES]

    targets = [t for t in targets if t.exists()]
    if not targets:
        sys.exit("Tidak ada berkas yang ditemukan.")

    if a.list:
        for t in targets:
            print(f"{t}  ({t.stat().st_size:,} bytes)")
        return

    if not a.token or not a.chat:
        sys.exit("Set TELEGRAM_BOT_TOKEN dan TELEGRAM_CHAT_ID dulu "
                 "(atau pakai --token/--chat).")
    print(f"Mengirim {len(targets)} berkas ke chat {a.chat} ...")
    hasil = [kirim(a.token, a.chat, t) for t in targets]
    print(f"Selesai: {sum(hasil)}/{len(hasil)} terkirim.")


if __name__ == "__main__":
    main()
