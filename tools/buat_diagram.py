# -*- coding: utf-8 -*-
"""Generator diagram alur hidrologi (HTML self-contained, SVG chart) dari hasil_validasi.json."""
import json, math

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
J = json.load(open(ROOT / "data" / "processed" / "hasil_validasi.json"))
OUT = ROOT / "figures" / "diagram-alur-hidrologi.html"

def idfmt(x, d=3):
    s = f"{x:,.{d}f}"
    return s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

YEARS = J["years"]; XMAX = J["xmax"]; N = len(XMAX)
XBAR = J["xbar"]; SD = J["S"]
TS = [2, 5, 10, 25, 50, 100]

# ---------- Chart 1: bar Xmax tahunan ----------
def chart_xmax():
    W, H = 680, 300; ml, mr, mt, mb = 48, 14, 20, 46
    pw, ph = W - ml - mr, H - mt - mb
    ymax = 240.0; slot = pw / N; bw = slot * 0.62
    p = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="Xmax tahunan">']
    for gv in range(0, 241, 60):
        y = mt + ph - gv / ymax * ph
        p.append(f'<line x1="{ml}" y1="{y:.1f}" x2="{W-mr}" y2="{y:.1f}" class="grid"/>')
        p.append(f'<text x="{ml-7}" y="{y+3:.1f}" class="ax" text-anchor="end">{gv}</text>')
    for i, v in enumerate(XMAX):
        x = ml + i * slot + (slot - bw) / 2
        y = mt + ph - v / ymax * ph
        col = "#d97706" if v == max(XMAX) else "#64748b"
        p.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{mt+ph-y:.1f}" rx="3" fill="{col}"/>')
        p.append(f'<text x="{x+bw/2:.1f}" y="{y-4:.1f}" class="vlab" text-anchor="middle">{v:.0f}</text>')
        lx = ml + i * slot + slot / 2
        p.append(f'<text x="{lx:.1f}" y="{mt+ph+14}" class="ax" text-anchor="end" transform="rotate(-45 {lx:.1f} {mt+ph+14})">{YEARS[i]}</text>')
    ybar = mt + ph - XBAR / ymax * ph
    p.append(f'<line x1="{ml}" y1="{ybar:.1f}" x2="{W-mr}" y2="{ybar:.1f}" class="mean"/>')
    p.append(f'<text x="{W-mr-2}" y="{ybar-5:.1f}" class="meanlab" text-anchor="end">X&#772; = {idfmt(XBAR,1)} mm</text>')
    divx = ml + 7 * slot
    p.append(f'<line x1="{divx:.1f}" y1="{mt}" x2="{divx:.1f}" y2="{mt+ph}" class="divider"/>')
    p.append(f'<text x="{ml+3.5*slot:.1f}" y="{mt+12}" class="setlab" text-anchor="middle">Set 1 · 2012–2018</text>')
    p.append(f'<text x="{divx+3.5*slot:.1f}" y="{mt+12}" class="setlab" text-anchor="middle">Set 2 · 2019–2025</text>')
    p.append('</svg>')
    return "".join(p)

# ---------- Chart 2: kurva frekuensi ----------
def chart_freq():
    W, H = 680, 300; ml, mr, mt, mb = 48, 16, 30, 40
    pw, ph = W - ml - mr, H - mt - mb
    logs = [math.log10(t) for t in TS]; lo, hi = min(logs), max(logs)
    ymin, ymax = 95.0, 290.0
    def X(l): return ml + (l - lo) / (hi - lo) * pw
    def Y(v): return mt + ph - (v - ymin) / (ymax - ymin) * ph
    series = [("Normal", [J["freq"][str(t)]["Normal"] for t in TS], "#0284c7", 2),
              ("Gumbel", [J["freq"][str(t)]["Gumbel"] for t in TS], "#6366f1", 2),
              ("Log Pearson III", [J["freq"][str(t)]["LP3"] for t in TS], "#16a34a", 3.2)]
    p = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="Kurva frekuensi">']
    for gv in range(100, 251, 50):
        y = Y(gv)
        p.append(f'<line x1="{ml}" y1="{y:.1f}" x2="{W-mr}" y2="{y:.1f}" class="grid"/>')
        p.append(f'<text x="{ml-7}" y="{y+3:.1f}" class="ax" text-anchor="end">{gv}</text>')
    for t, lg in zip(TS, logs):
        x = X(lg)
        p.append(f'<line x1="{x:.1f}" y1="{mt+ph}" x2="{x:.1f}" y2="{mt+ph+5}" class="tick"/>')
        p.append(f'<text x="{x:.1f}" y="{mt+ph+18}" class="ax" text-anchor="middle">{t}</text>')
    p.append(f'<text x="{ml+pw/2:.1f}" y="{H-4}" class="axlab" text-anchor="middle">Periode ulang T (tahun, skala log)</text>')
    x10 = X(math.log10(10))
    p.append(f'<line x1="{x10:.1f}" y1="{mt}" x2="{x10:.1f}" y2="{mt+ph}" class="t10"/>')
    p.append(f'<text x="{x10+5:.1f}" y="{mt+12}" class="t10lab">T = 10 th (R24)</text>')
    for name, vals, col, wdt in series:
        pts = " ".join(f"{X(math.log10(t)):.1f},{Y(v):.1f}" for t, v in zip(TS, vals))
        p.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{wdt}" stroke-linejoin="round"/>')
        for t, v in zip(TS, vals):
            p.append(f'<circle cx="{X(math.log10(t)):.1f}" cy="{Y(v):.1f}" r="2.6" fill="{col}"/>')
    lx, ly = ml + 12, mt + 8
    for name, vals, col, wdt in series:
        p.append(f'<line x1="{lx}" y1="{ly}" x2="{lx+22}" y2="{ly}" stroke="{col}" stroke-width="{wdt}"/>')
        p.append(f'<circle cx="{lx+11}" cy="{ly}" r="2.6" fill="{col}"/>')
        p.append(f'<text x="{lx+28}" y="{ly+4}" class="leg">{esc(name)}</text>')
        ly += 17
    r24 = J["R24"]
    p.append(f'<text x="{X(math.log10(10))-8:.1f}" y="{Y(r24)-8:.1f}" class="r24lab" text-anchor="end">R24 = {idfmt(r24,1)} mm</text>')
    p.append('</svg>')
    return "".join(p)

# ---------- Chart 3: chi-kuadrat O vs E ----------
def chart_chi():
    c = J["chi"][J["chosen"]]
    O, E = c["O"], c["E"]
    labs = ["x &#8804; R2", "R2&#8211;R5", "R5&#8211;R10", "R10&#8211;R25", "x &gt; R25"]
    W, H = 680, 300; ml, mr, mt, mb = 48, 14, 34, 52
    pw, ph = W - ml - mr, H - mt - mb
    ymax = 10.0; gslot = pw / 5; bw = 38
    p = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="Chi kuadrat">']
    for gv in range(0, 11, 2):
        y = mt + ph - gv / ymax * ph
        p.append(f'<line x1="{ml}" y1="{y:.1f}" x2="{W-mr}" y2="{y:.1f}" class="grid"/>')
        p.append(f'<text x="{ml-7}" y="{y+3:.1f}" class="ax" text-anchor="end">{gv}</text>')
    for i in range(5):
        cx = ml + i * gslot + gslot / 2
        for j, (v, col) in enumerate([(O[i], "#2563eb"), (E[i], "#cbd5e1")]):
            x = cx - bw - 3 + j * (bw + 6)
            y = mt + ph - v / ymax * ph
            p.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw}" height="{mt+ph-y:.1f}" rx="3" fill="{col}" stroke="#94a3b8" stroke-width="0.6"/>')
            p.append(f'<text x="{x+bw/2:.1f}" y="{y-4:.1f}" class="vlab" text-anchor="middle">{idfmt(v,1) if v else "0"}</text>')
        p.append(f'<text x="{cx:.1f}" y="{mt+ph+16}" class="ax" text-anchor="middle">{labs[i]}</text>')
    lx, ly = ml + 8, mt + 4
    for lab, col in [("O (observasi)", "#2563eb"), ("E = n·p (harapan)", "#cbd5e1")]:
        p.append(f'<rect x="{lx}" y="{ly-9}" width="14" height="10" rx="2" fill="{col}" stroke="#94a3b8" stroke-width="0.6"/>')
        p.append(f'<text x="{lx+20}" y="{ly}" class="leg">{lab}</text>')
        ly += 18
    p.append(f'<text x="{ml+8}" y="{H-16}" class="cap">Kelas dibatasi R2, R5, R10, R25 · peluang 0,50 / 0,20 / 0,10 / 0,06 / 0,04 · &#967;&#178; = {idfmt(c["chi2"],3)} &#8804; {idfmt(c["crit"],3)} (df = {c["df"]}) &#8594; LOLOS</text>')
    p.append('</svg>')
    return "".join(p)

# ---------- Chart 4: deviasi kumulatif ternormalisasi ----------
def chart_kons():
    vals = J["kons"]["Sstar_norm"]
    Dy = J["kons"]["Dy"]
    Q = max(abs(v) for v in vals)
    qsqrt = Q / math.sqrt(N)
    W, H = 680, 280; ml, mr, mt, mb = 48, 14, 20, 40
    pw, ph = W - ml - mr, H - mt - mb
    ymin, ymax = -4.6, 1.0
    def X(i): return ml + (i + 0.5) / N * pw
    def Y(v): return mt + ph - (v - ymin) / (ymax - ymin) * ph
    p = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="Deviasi kumulatif">']
    for gv in [-4, -3, -2, -1, 0]:
        y = Y(gv)
        p.append(f'<line x1="{ml}" y1="{y:.1f}" x2="{W-mr}" y2="{y:.1f}" class="grid"/>')
        p.append(f'<text x="{ml-7}" y="{y+3:.1f}" class="ax" text-anchor="end">{gv}</text>')
    p.append(f'<line x1="{ml}" y1="{Y(0):.1f}" x2="{W-mr}" y2="{Y(0):.1f}" class="zero"/>')
    pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(vals))
    p.append(f'<polyline points="{pts}" fill="none" stroke="#0d9488" stroke-width="2" stroke-linejoin="round"/>')
    imin = min(range(N), key=lambda i: vals[i])
    for i, v in enumerate(vals):
        col = "#dc2626" if i == imin else "#0d9488"
        p.append(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="{4.5 if i==imin else 2.4}" fill="{col}"/>')
        p.append(f'<text x="{X(i):.1f}" y="{mt+ph+15}" class="ax" text-anchor="middle">{str(YEARS[i])[2:]}</text>')
    p.append(f'<circle cx="{X(imin):.1f}" cy="{Y(vals[imin]):.1f}" r="7" fill="none" stroke="#dc2626" stroke-width="1.4"/>')
    p.append(f'<text x="{X(imin):.1f}" y="{Y(vals[imin])-12:.1f}" class="qlab" text-anchor="middle">Q = {idfmt(Q,3)} (tahun {YEARS[imin]})</text>')
    p.append(f'<text x="{ml+6}" y="{mt+14}" class="cap">Q/&#8730;n = {idfmt(qsqrt,3)} &lt; kritik 95% = {idfmt(J["kons"]["q95"],3)} &#8594; KONSISTEN</text>')
    p.append('</svg>')
    return "".join(p)

# ---------- mini tables ----------
freq_rows = ""
for t in TS:
    r = J["freq"][str(t)]
    hl = ' class="hl"' if t == 10 else ""
    freq_rows += (f'<tr{hl}><td>T = {t} th</td><td>{idfmt(r["Normal"])}</td>'
                  f'<td>{idfmt(r["Gumbel"])}</td><td><b>{idfmt(r["LP3"])}</b></td></tr>')

chi_rows = ""
for name, P in [("Normal", 2), ("Gumbel", 2), ("LP3", 3)]:
    c = J["chi"][name]
    chi_rows += (f'<tr><td>{name}</td><td>{idfmt(c["chi2"],3)}</td><td>{c["df"]}</td>'
                 f'<td>{idfmt(c["crit"],3)}</td><td>{"LOLOS" if c["lolos"] else "GAGAL"}</td></tr>')

t = J["t"]; k = J["kons"]; g = J["gumbel"]
R24 = J["R24"]; I = J["I"]; Qr = J["Q"]; Va = Qr * 3600

CSS = """
:root{--bg:#f4f6fa;--card:#fff;--border:#e3e8f0;--ink:#1e293b;--muted:#64748b;--slate:#64748b;
--indigo:#6366f1;--sky:#0284c7;--blue:#2563eb;--amber:#d97706;--teal:#0d9488;--green:#16a34a;--red:#dc2626}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink);line-height:1.5;padding:32px 16px 48px}
.wrap{max-width:980px;margin:0 auto}
header{text-align:center;margin-bottom:16px}
header h1{font-size:26px;letter-spacing:-.02em}
header p{color:var(--muted);margin-top:6px;font-size:14px}
.flowstrip{display:flex;flex-wrap:wrap;justify-content:center;gap:6px;margin:18px 0 26px}
.fchip{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11.5px;background:var(--card);border:1px solid var(--border);border-radius:999px;padding:5px 11px;cursor:pointer;transition:border-color .15s,background .15s}
.fchip:hover{border-color:var(--blue);background:#eff6ff}
.farr{color:var(--muted);align-self:center;font-size:12px}
.stage{background:var(--card);border:1px solid var(--border);border-left:5px solid var(--acc,var(--slate));border-radius:14px;padding:16px 20px;box-shadow:0 1px 3px rgba(15,23,42,.06)}
.stage-head{display:flex;align-items:flex-start;gap:12px}
.num{flex:0 0 auto;width:30px;height:30px;border-radius:50%;background:var(--acc,var(--slate));color:#fff;display:grid;place-items:center;font-weight:800;font-size:14px;margin-top:2px}
.stage-head h2{font-size:16.5px;letter-spacing:-.01em;font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
.stage-head .sub{color:var(--muted);font-size:13px;margin-top:1px}
.badge{margin-left:auto;flex:0 0 auto;font-size:12px;font-weight:700;border-radius:999px;padding:5px 12px;white-space:nowrap}
.b-ok{background:#dcfce7;color:#14532d;border:1px solid #86efac}
.b-info{background:#eff6ff;color:#1e3a8a;border:1px solid #bfdbfe}
.b-warn{background:#fffbeb;color:#78350f;border:1px solid #fde68a}
.body-row{display:flex;gap:18px;margin-top:12px;align-items:stretch}
.chips-zone{flex:1;min-width:0}
.chips-label{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:8px 0 6px}
.chips-label:first-child{margin-top:0}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{background:#f8fafc;border:1px solid var(--border);border-radius:8px;padding:5px 11px;font-size:13px}
.chip.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px}
.chip b{font-weight:700}
.chip .f{color:var(--muted)}
.arrow{width:2px;height:30px;background:#c9d3e0;margin:0 auto;position:relative;flex:0 0 auto}
.arrow::after{content:"";position:absolute;bottom:-2px;left:50%;transform:translateX(-50%);border:7px solid transparent;border-top-color:#c9d3e0}
table.mini{border-collapse:collapse;font-size:12px;margin-top:4px}
table.mini th,table.mini td{border:1px solid var(--border);padding:3px 10px;text-align:right;font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
table.mini th{background:#f1f5f9;font-weight:700;text-align:center}
table.mini td:first-child,table.mini th:first-child{text-align:left}
table.mini tr.hl td{background:#f0fdf4;font-weight:600}
.charts{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:26px}
.chart-card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:14px 16px;box-shadow:0 1px 3px rgba(15,23,42,.06)}
.chart-card h3{font-size:14px;margin-bottom:2px}
.chart-card .cap{color:var(--muted);font-size:12px;margin-bottom:8px}
svg.chart{width:100%;height:auto;display:block}
.grid line{stroke:#e2e8f0;stroke-width:1}
.grid{stroke:#e2e8f0;stroke-width:1}
.tick{stroke:#94a3b8;stroke-width:1}
.mean{stroke:var(--blue);stroke-width:1.4;stroke-dasharray:6 4}
.meanlab{font-size:10.5px;fill:var(--blue);font-weight:700}
.divider{stroke:#cbd5e1;stroke-width:1.2;stroke-dasharray:3 4}
.setlab{font-size:10px;fill:var(--muted);font-weight:700}
.ax{font-size:10px;fill:#64748b}
.axlab{font-size:10.5px;fill:#64748b}
.vlab{font-size:9px;fill:#334155}
.leg{font-size:11px;fill:var(--ink)}
.t10{stroke:var(--amber);stroke-width:1.2;stroke-dasharray:5 4}
.t10lab{font-size:10px;fill:var(--amber);font-weight:700}
.r24lab{font-size:11px;fill:var(--green);font-weight:700}
.zero{stroke:#334155;stroke-width:1.2}
.qlab{font-size:11px;fill:var(--red);font-weight:700}
.cap2{font-size:10.5px;fill:var(--muted)}
.cap{font-size:10.5px;fill:var(--muted)}
.summary{margin-top:26px;background:var(--card);border:1px solid var(--border);border-radius:14px;padding:16px 20px;box-shadow:0 1px 3px rgba(15,23,42,.06)}
.summary h3{font-size:15px;margin-bottom:10px}
.sum-row{display:flex;gap:12px;flex-wrap:wrap}
.sum{flex:1;min-width:200px;border-radius:10px;padding:12px 14px;font-size:13px}
.sum b{font-size:14px}
.sum-r{background:#eff6ff;color:#1e3a8a}.sum-i{background:#fffbeb;color:#78350f}.sum-q{background:#f0fdf4;color:#14532d}
.note{margin-top:14px;background:#fff7ed;border:1px solid #fed7aa;border-radius:10px;padding:12px 14px;font-size:12.5px;color:#7c2d12}
.note b{font-weight:700}
@media (max-width:760px){.charts{grid-template-columns:1fr}.badge{display:none}}
@media print{body{background:#fff}.stage,.chart-card,.summary{box-shadow:none}}
"""

HTML = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Diagram Alur Perhitungan Hidrologi — Ambawang 2012–2025</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header>
<h1>Diagram Alur Perhitungan Hidrologi</h1>
<p>Stasiun Ambawang (BWSK) 2012–2025 · n = {N} tahun · X&#772; = {idfmt(XBAR,1)} mm · S = {idfmt(SD,1)} mm · Cv = {idfmt(J['Cv'],3)} · Cs = {idfmt(J['Cs'],3)}</p>
</header>

<div class="flowstrip">
<span class="fchip" onclick="jump('s1')">1 Data_Harian</span><span class="farr">&#8594;</span>
<span class="fchip" onclick="jump('s2')">2 Statistik_Tahunan</span><span class="farr">&#8594;</span>
<span class="fchip" onclick="jump('s3')">3 Statistik</span><span class="farr">&#8594;</span>
<span class="fchip" onclick="jump('s4')">4 Uji_Homogenitas</span><span class="farr">&#8594;</span>
<span class="fchip" onclick="jump('s5')">5 Uji_Konsistensi</span><span class="farr">&#8594;</span>
<span class="fchip" onclick="jump('s6')">6 Frekuensi</span><span class="farr">&#8594;</span>
<span class="fchip" onclick="jump('s7')">7 Chi_Kuadrat</span><span class="farr">&#8594;</span>
<span class="fchip" onclick="jump('s8')">8 Debit_Rencana</span>
</div>

<div class="flow">

<section class="stage" id="s1" style="--acc:var(--slate)">
<div class="stage-head"><span class="num">1</span>
<div><h2>Data_Harian</h2><p class="sub">Curah hujan harian mentah (mm) — Stasiun Sungai Ambawang, BWSK</p></div>
<span class="badge b-info">INPUT</span></div>
<div class="body-row"><div class="chips-zone">
<div class="chips-label">Pekerjaan</div>
<div class="chips">
<span class="chip">Parse xlsx BWSK per sheet-tahun</span>
<span class="chip">Grid tanggal valid 14 tahun</span>
<span class="chip">Sel kosong &#8594; NULL (data hilang)</span>
<span class="chip">Simpan ke SQLite <b>hidrologi.db</b></span>
</div>
<div class="chips-label">Keluaran</div>
<div class="chips"><span class="chip mono">5.113 baris harian · 14 tahun · 12 hari hilang</span></div>
</div></div>
</section>
<div class="arrow"></div>

<section class="stage" id="s2" style="--acc:var(--sky)">
<div class="stage-head"><span class="num">2</span>
<div><h2>Statistik_Tahunan</h2><p class="sub">Agregasi per tahun &#8594; ambil nilai maksimum harian (metode annual maxima)</p></div>
<span class="badge b-info">SERI Xmax</span></div>
<div class="body-row"><div class="chips-zone">
<div class="chips-label">Rumus / kerja (Excel: COUNTIFS · SUMIFS · MAXIFS)</div>
<div class="chips">
<span class="chip">Total hujan tahunan = &#931; mm</span>
<span class="chip">X maks harian = MAXIFS(mm, tahun)</span>
<span class="chip">Hari hujan = COUNTIF(mm &gt; 0)</span>
</div>
<div class="chips-label">Seri Xmax tahunan (mm) — lihat Grafik 1</div>
<div class="chips"><span class="chip mono">{esc(" · ".join(f"{v:.0f}" for v in XMAX))}</span></div>
</div></div>
</section>
<div class="arrow"></div>

<section class="stage" id="s3" style="--acc:var(--indigo)">
<div class="stage-head"><span class="num">3</span>
<div><h2>Statistik</h2><p class="sub">Parameter momen dari seri Xmax (n = {N})</p></div>
<span class="badge b-info">PARAMETER</span></div>
<div class="body-row"><div class="chips-zone">
<div class="chips-label">Momen (rumus tesis [5]–[8])</div>
<div class="chips">
<span class="chip mono">X&#772; = &#931;Xi/n = <b>{idfmt(XBAR)}</b></span>
<span class="chip mono">S = &#8730;(&#931;(Xi&#8722;X&#772;)&#178;/(n&#8722;1)) = <b>{idfmt(SD)}</b></span>
<span class="chip mono">Cv = S/X&#772; = <b>{idfmt(J['Cv'])}</b></span>
<span class="chip mono">Cs = n/((n&#8722;1)(n&#8722;2))·&#931;z&#179; = <b>{idfmt(J['Cs'])}</b></span>
<span class="chip mono">Ck = (1/n)·&#931;z&#8308; = <b>{idfmt(J['Ck'])}</b></span>
</div>
<div class="chips-label">Statistik log&#8321;&#8320; (untuk Log Pearson III, rumus [13]–[15])</div>
<div class="chips">
<span class="chip mono">log X&#772; = <b>{idfmt(J['logXbar'],4)}</b></span>
<span class="chip mono">S log = <b>{idfmt(J['Slog'],4)}</b></span>
<span class="chip mono">Cs log = <b>{idfmt(J['Cslog'],3)}</b></span>
</div>
</div></div>
</section>
<div class="arrow"></div>

<section class="stage" id="s4" style="--acc:var(--sky)">
<div class="stage-head"><span class="num">4</span>
<div><h2>Uji_Homogenitas</h2><p class="sub">Uji-t dua sampel <i>pooled</i> (rumus [0],[1]) — setengah awal vs setengah akhir</p></div>
<span class="badge b-ok">HOMOGEN</span></div>
<div class="body-row"><div class="chips-zone">
<div class="chips-label">Perhitungan</div>
<div class="chips">
<span class="chip mono">Set 1 (2012–2018): X&#772;&#8321; = {idfmt(t['x1b'],2)}, S&#8321; = {idfmt(t['S1'],2)} (pembagi n&#8321;={t['n1']})</span>
<span class="chip mono">Set 2 (2019–2025): X&#772;&#8322; = {idfmt(t['x2b'],2)}, S&#8322; = {idfmt(t['S2'],2)} (pembagi n&#8322;={t['n2']})</span>
<span class="chip mono">&#963; = &#8730;((n&#8321;S&#8321;&#178;+n&#8322;S&#8322;&#178;)/(n&#8321;+n&#8322;&#8722;2)) = <b>{idfmt(t['sigma'])}</b></span>
<span class="chip mono">t = |X&#772;&#8321;&#8722;X&#772;&#8322;| / (&#963;&#183;&#8730;(1/n&#8321;+1/n&#8322;)) = <b>{idfmt(t['t'],3)}</b></span>
</div>
<div class="chips-label">Keputusan (dk = {t['dk']}, &#945; = 5%)</div>
<div class="chips">
<span class="chip mono">dua arah: {idfmt(t['t'],3)} &lt; 2,179 &#8594; <b>HOMOGEN</b></span>
<span class="chip mono">satu arah: 2,179&#8594;1,782 · {idfmt(t['t'],3)} &gt; 1,782 (batas)</span>
</div>
</div></div>
</section>
<div class="arrow"></div>

<section class="stage" id="s5" style="--acc:var(--teal)">
<div class="stage-head"><span class="num">5</span>
<div><h2>Uji_Konsistensi</h2><p class="sub">Cumulative Deviation (rumus [2]–[4]) — Sri Harto (1993)</p></div>
<span class="badge b-ok">KONSISTEN</span></div>
<div class="body-row"><div class="chips-zone">
<div class="chips-label">Perhitungan</div>
<div class="chips">
<span class="chip mono">S*&#7522; = &#931;(Xi &#8722; X&#772;) kumulatif, k = 1..{N}</span>
<span class="chip mono">Dy = &#8730;(&#931;(Xi&#8722;X&#772;)&#178;/n) = <b>{idfmt(k['Dy'])}</b></span>
<span class="chip mono">Q = maks |S*&#7522;/Dy| = <b>{idfmt(max(abs(v) for v in k['Sstar_norm']))}</b> (tahun 2019)</span>
<span class="chip mono">Q/&#8730;n = <b>{idfmt(k['qsqrt'],3)}</b></span>
</div>
<div class="chips-label">Keputusan (Tabel 2.3, interpolasi n = {N})</div>
<div class="chips">
<span class="chip mono">95%: {idfmt(k['qsqrt'],3)} &lt; {idfmt(k['q95'],3)} &#8594; <b>KONSISTEN</b></span>
<span class="chip mono">99%: kritik {idfmt(k['q99'],3)}</span>
</div>
</div></div>
</section>
<div class="arrow"></div>

<section class="stage" id="s6" style="--acc:var(--blue)">
<div class="stage-head"><span class="num">6</span>
<div><h2>Frekuensi</h2><p class="sub">Fitting tiga distribusi kandidat &#8594; XT(T) dalam mm</p></div>
<span class="badge b-info">3 KANDIDAT</span></div>
<div class="body-row"><div class="chips-zone">
<div class="chips-label">Rumus</div>
<div class="chips">
<span class="chip mono"><b>Normal:</b> XT = X&#772; + Kp·S <span class="f">(Kp: Tabel 2.4)</span></span>
<span class="chip mono"><b>Gumbel:</b> a = S/1,283 = {idfmt(g['a'],2)}; Xo = X&#772;&#8722;0,577a = {idfmt(g['Xo'],2)}; XT = Xo + Yp·a <span class="f">(Yp: Tabel 2.5)</span></span>
<span class="chip mono"><b>LP3:</b> XT = 10^(log X&#772; + K·S log) <span class="f">(K: Tabel 2.6, interpolasi Cs log = {idfmt(J['Cslog'],3)})</span></span>
</div>
<div class="chips-label">Hasil XT (mm)</div>
<table class="mini">
<tr><th>Periode ulang</th><th>Normal</th><th>Gumbel</th><th>Log Pearson III</th></tr>
{freq_rows}
</table>
</div></div>
</section>
<div class="arrow"></div>

<section class="stage" id="s7" style="--acc:var(--amber)">
<div class="stage-head"><span class="num">7</span>
<div><h2>Chi_Kuadrat</h2><p class="sub">Uji kecocokan (rumus [2.17]) — &#967;&#178; = &#931;(Oi&#8722;Ei)&#178;/Ei, dk = G&#8722;1&#8722;P</p></div>
<span class="badge b-ok">LP3 TERPILIH</span></div>
<div class="body-row"><div class="chips-zone">
<div class="chips-label">Kelas &amp; frekuensi (batas R2, R5, R10, R25 · peluang 0,50/0,20/0,10/0,06/0,04)</div>
<div class="chips">
<span class="chip mono">E = n·p = [7,0 · 2,8 · 1,4 · 0,84 · 0,56]</span>
<span class="chip mono">O = [9 · 2 · 2 · 0 · 1]</span>
<span class="chip mono">&#967;&#178; hitung = <b>{idfmt(J['chi'][J['chosen']]['chi2'],3)}</b> (ketiga distribusi)</span>
</div>
<div class="chips-label">Hasil uji (&#945; = 5%)</div>
<table class="mini">
<tr><th>Distribusi</th><th>&#967;&#178; hitung</th><th>df</th><th>&#967;&#178; kritik</th><th>Kesimpulan</th></tr>
{chi_rows}
</table>
<div class="chips"><span class="chip mono">Semua lolos &#8594; seri &#8594; prioritas <b>LP3 &gt; Gumbel &gt; Normal</b> (SNI 2415:2016)</span></div>
</div></div>
</section>
<div class="arrow"></div>

<section class="stage" id="s8" style="--acc:var(--green)">
<div class="stage-head"><span class="num">8</span>
<div><h2>Debit_Rencana</h2><p class="sub">R24 (T=10, LP3) &#8594; tc &#8594; intensitas Mononobe &#8594; debit Rasional</p></div>
<span class="badge b-ok">Q = {idfmt(Qr,3)} m&#179;/dtk</span></div>
<div class="body-row"><div class="chips-zone">
<div class="chips-label">Rantai perhitungan</div>
<div class="chips">
<span class="chip mono">R24 = XT(T=10, LP3) = <b>{idfmt(R24)} mm</b></span>
<span class="chip mono">to = 0,0195·Lo^0,77/Ss^0,385 (Kirpich) = {idfmt(J['to'],2)} mnt</span>
<span class="chip mono">V = (1/n)·Rh&#8310;&#8314;·&#8730;S (Manning) = {idfmt(J['Vch'],3)} m/s</span>
<span class="chip mono">td = Ld/(60·V) = {idfmt(J['td'],2)} mnt</span>
<span class="chip mono">tc = (to+td)/60 = <b>{idfmt(J['tc'],4)} jam</b></span>
<span class="chip mono">I = (R24/24)·(24/tc)^&#8531; (Mononobe) = <b>{idfmt(I,1)} mm/jam</b></span>
<span class="chip mono">Q = 0,278·C·I·A = 0,278·{idfmt(J['C'],2)}·{idfmt(I,1)}·{idfmt(J['A_km2'],4)} = <b>{idfmt(Qr,3)} m&#179;/dtk</b></span>
<span class="chip mono">Va = Q·th = {idfmt(Qr,3)} × 3600 &#8776; <b>{idfmt(Va,0)} m&#179;</b> (th = 1 jam)</span>
</div>
</div></div>
</section>

</div>

<h2 style="font-size:17px;margin:34px 0 4px">Grafik pendukung</h2>
<p style="color:var(--muted);font-size:13px;margin-bottom:12px">Visualisasi data dan hasil fitting dari angka-angka pada alur di atas.</p>
<div class="charts">
<div class="chart-card"><h3>Grafik 1 — X maksimum harian tahunan</h3><p class="cap">Seri annual maxima (mm) dengan garis rata-rata X&#772; = {idfmt(XBAR,1)} mm dan batas dua set uji homogenitas.</p>{chart_xmax()}</div>
<div class="chart-card"><h3>Grafik 2 — Kurva frekuensi kandidat</h3><p class="cap">XT vs periode ulang T (skala log). LP3 (hijau tebal) terpilih; titik T=10 &#8594; R24 = {idfmt(R24,1)} mm.</p>{chart_freq()}</div>
<div class="chart-card"><h3>Grafik 3 — Chi-kuadrat: O vs E ({J['chosen']})</h3><p class="cap">Frekuensi observasi vs harapan per kelas (distribusi terpilih).</p>{chart_chi()}</div>
<div class="chart-card"><h3>Grafik 4 — Deviasi kumulatif ternormalisasi</h3><p class="cap">S*&#7522;/Dy per tahun; puncak negatif di 2019 (hujan 220 mm) menentukan Q.</p>{chart_kons()}</div>
</div>

<div class="summary">
<h3>Rangkaian keputusan akhir</h3>
<div class="sum-row">
<div class="sum sum-r"><b>R24 = {idfmt(R24,1)} mm</b><br>hujan rencana T = 10 th dari Log Pearson III (&#967;&#178; lolos, prioritas SNI 2415:2016)</div>
<div class="sum sum-i"><b>I = {idfmt(I,1)} mm/jam</b><br>intensitas Mononobe pada tc = {idfmt(J['tc'],4)} jam (to {idfmt(J['to'],1)} mnt + td {idfmt(J['td'],1)} mnt)</div>
<div class="sum sum-q"><b>Q = {idfmt(Qr,3)} m&#179;/dtk</b><br>debit rencana Rasional (C = {idfmt(J['C'],2)}, A = {idfmt(J['A_km2']*100,2)} ha) · Va &#8776; {idfmt(Va,0)} m&#179;</div>
</div>
</div>

<div class="note">
<b>Catatan:</b> seluruh angka dibaca dari <span class="chip mono" style="display:inline">data/processed/hasil_validasi.json</span> (analisis2.py &#8594; hidrologi.db &#8594; xlsx BWSK). Parameter site pada tahap 8 (Lo, Ss, Ld, B, y, n Manning, C, A) masih asumsi placeholder — ganti dengan data lapangan. Nilai Q uji konsistensi pada Grafik 4 dihitung ulang dari deret S*&#7522;/Dy (field <i>kons.Q</i> di JSON tertimpa variabel debit — lihat chat).
</div>

</div>
<script>
function jump(id){{var el=document.getElementById(id);if(el)el.scrollIntoView({{behavior:'smooth',block:'center'}});}}
</script>
</body>
</html>
"""

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"[ok] {OUT} ({len(HTML)} byte)")
