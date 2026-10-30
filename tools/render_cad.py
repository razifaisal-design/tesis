"""Render ulang sket_lengkap.dxf -> figures/ (Tahap 6).

DXF adalah sumber yang sudah disinkronkan (DN900 + anotasi kolam 15.751,7 m3);
render lama di arsip (folder di-ignore Git) belum diperbarui.

Dua keluaran (di-zoom ke area siteplan, latar putih):
- sket_lengkap_dxf.png/.pdf        : vektor saja
- sket_lengkap_dxf_satelit.png/.pdf: vektor + raster citra satelit
"""
from pathlib import Path

import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.bbox import extents
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DXF = ROOT / "data/raw/arsip-tesis-lengkap/03_Desain_CAD_dan_Peta/sket_lengkap.dxf"
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)


def bbox_siteplan(msp):
    """Extent entitas kecuali polilin batas besar & IMAGE ( footprint satelit )."""
    entitas = [e for e in msp if e.dxftype() in ("TEXT", "MTEXT", "DIMENSION")]
    bx = extents(entitas)
    return bx.extmin, bx.extmax


def render(dengan_raster: bool, nama: str) -> None:
    doc = ezdxf.readfile(DXF)
    msp = doc.modelspace()
    (xmin, ymin, _), (xmax, ymax, _) = bbox_siteplan(msp)
    gambar = [e for e in msp if e.dxftype() == "IMAGE"]
    vektor = [e for e in msp if e.dxftype() != "IMAGE"]

    pad = max(xmax - xmin, ymax - ymin) * 0.08
    fig = plt.figure(figsize=(16, 10), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    cfg = Configuration(background_policy=BackgroundPolicy.WHITE)
    fe = Frontend(RenderContext(doc), MatplotlibBackend(ax), config=cfg)
    if dengan_raster:
        fe.draw_entities(gambar)  # raster di bawah, vektor di atas
    fe.draw_entities(vektor)
    ax.set_xlim(xmin - pad, xmax + pad)
    ax.set_ylim(ymin - pad, ymax + pad)
    fig.savefig(OUT / f"{nama}.png", facecolor="white")
    fig.savefig(OUT / f"{nama}.pdf", facecolor="white")
    plt.close(fig)
    print(nama, "->", (OUT / f"{nama}.png").stat().st_size, "bytes")


render(dengan_raster=False, nama="sket_lengkap_dxf")
render(dengan_raster=True, nama="sket_lengkap_dxf_satelit")
