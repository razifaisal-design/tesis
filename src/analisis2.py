# -*- coding: utf-8 -*-
"""Analisis sesuai Proposal Tesis (versi final, rumus diambil dari OMML docx).
Sumber data: data/processed/hidrologi.db (dibangun build_db.py)."""
import math, json, sqlite3
import numpy as np

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "processed" / "hidrologi.db"

records, missing_real, per_year = [], [], {}
con = sqlite3.connect(DB)
for y, b, d, mm in con.execute("SELECT tahun,bulan,tgl,mm FROM curah_hujan_harian ORDER BY tanggal"):
    if mm is None: missing_real.append((y,b,d))
    records.append((y,b,d,mm))
con.close()
for y in sorted({r[0] for r in records}):
    yrs = [v for (yy,_,_,v) in records if yy==y and v is not None]
    per_year[y] = dict(total=round(sum(yrs),1),
                       xmax=max(yrs, default=None),
                       hari_hujan=sum(1 for v in yrs if v>0),
                       n_valid=sum(1 for (yy,_,_,_) in records if yy==y),
                       n_missing=sum(1 for (yy,_,_) in missing_real if yy==y))

ys_list = sorted(per_year)
xmax = np.array([per_year[y]['xmax'] for y in ys_list], dtype=float)
n = len(xmax)
xbar = xmax.mean()
S = xmax.std(ddof=1)                       # rumus [5]: pembagi (n-1)
Cv = S/xbar
Cs = n/((n-1)*(n-2)) * (((xmax-xbar)/S)**3).sum()     # [7]
Ck = (1/n) * (((xmax-xbar)/S)**4).sum()               # [8] versi tesis
print(f"\nXbar={xbar:.4f} S={S:.4f} Cv={Cv:.4f} Cs={Cs:.4f} Ck={Ck:.4f}  (n={n})")

# ---- 3. UJI HOMOGENITAS (pooled t, rumus [0][1]) ----
n1, n2 = 7, 7
x1, x2 = xmax[:n1], xmax[n1:]
x1b, x2b = x1.mean(), x2.mean()
S1 = math.sqrt(((x1-x1b)**2).sum()/n1)   # pembagi N (sesuai naskah)
S2 = math.sqrt(((x2-x2b)**2).sum()/n2)
sigma = math.sqrt((n1*S1**2 + n2*S2**2)/(n1+n2-2))     # [1]
t_hit = abs(x1b-x2b)/(sigma*math.sqrt(1/n1+1/n2))       # [0]
dk = n1+n2-2
print(f"\n=== UJI HOMOGENITAS (pooled t) ===")
print(f"set1 2012-2018: Xbar1={x1b:.3f} S1={S1:.4f} | set2 2019-2025: Xbar2={x2b:.3f} S2={S2:.4f}")
print(f"sigma_pooled={sigma:.4f} t_hitung={t_hit:.4f} dk={dk}")
print(f"t_kritis 2 arah 5% (kolom alpha=0,025) = 2.179 -> {'HOMOGEN' if t_hit<2.179 else 'TIDAK HOMOGEN'}")
print(f"t_kritis kolom alpha=0,05 (1 arah) = 1.782 -> {'HOMOGEN' if t_hit<1.782 else 'TIDAK HOMOGEN'}")

# ---- 4. UJI KONSISTENSI (rumus [2][3][4]) ----
Sstar = np.cumsum(xmax - xbar)
Dy = math.sqrt(((xmax-xbar)**2).sum()/n)     # [3] pembagi n
Sstar_norm = Sstar/Dy                        # [4]
Q = abs(Sstar_norm).max()
qsqrt = Q/math.sqrt(n)
q_crit95 = 1.14 + (14-10)/(20-10)*(1.22-1.14)
q_crit99 = 1.29 + (14-10)/(20-10)*(1.42-1.29)
print(f"\n=== UJI KONSISTENSI ===")
print(f"Dy={Dy:.4f} Q=maks|S**k|={Q:.4f} Q/sqrt(n)={qsqrt:.4f}")
print(f"kritik n=14: 95%={q_crit95:.4f} -> {'KONSISTEN' if qsqrt<q_crit95 else 'TIDAK KONSISTEN'} | 99%={q_crit99:.4f} -> {'KONSISTEN' if qsqrt<q_crit99 else 'TIDAK KONSISTEN'}")

# ---- 5. FREKUENSI ----
KN = {2:0.00,5:0.84,10:1.28,25:1.64,50:2.05,100:2.33}        # Tabel 2.4 (variabel reduksi normal)
YG = {2:0.366,5:1.510,10:2.250,25:3.900,50:4.600,100:5.290}  # Tabel 2.5
LP3T = [2,5,10,25,50,100]
LP3 = {3.0:[-0.396,0.420,1.180,2.278,3.152,4.051],2.5:[-0.360,0.518,1.250,2.262,3.048,3.845],
2.2:[-0.330,0.574,1.284,2.240,2.970,3.705],2.0:[-0.307,0.609,1.302,2.219,2.912,3.605],
1.8:[-0.282,0.643,1.318,2.193,2.848,3.499],1.6:[-0.254,0.675,1.329,2.163,2.780,3.388],
1.4:[-0.225,0.705,1.337,2.128,2.706,3.271],1.2:[-0.195,0.732,1.340,2.087,2.626,3.149],
1.0:[-0.164,0.758,1.340,2.043,2.542,3.022],0.9:[-0.148,0.769,1.339,2.018,2.498,2.957],
0.8:[-0.132,0.780,1.336,1.998,2.453,2.891],0.7:[-0.116,0.790,1.333,1.967,2.407,2.824],
0.6:[-0.099,0.800,1.328,1.939,2.359,2.755],0.5:[-0.083,0.808,1.323,1.910,2.311,2.686],
0.4:[-0.066,0.816,1.317,1.880,2.261,2.615],0.3:[-0.050,0.824,1.309,1.849,2.211,2.544],
0.2:[-0.033,0.830,1.301,1.818,2.159,2.472],0.1:[-0.017,0.836,1.292,1.785,2.107,2.400],
0.0:[0.000,0.842,1.282,1.751,2.054,2.326],-0.1:[0.017,0.846,1.270,1.716,2.000,2.252],
-0.2:[0.033,0.850,1.258,1.680,1.945,2.178],-0.3:[0.050,0.853,1.245,1.643,1.890,2.104],
-0.4:[0.066,0.855,1.231,1.606,1.834,2.029],-0.5:[0.083,0.856,1.216,1.567,1.777,1.955],
-0.6:[0.099,0.857,1.200,1.528,1.720,1.880],-0.7:[0.116,0.857,1.183,1.488,1.663,1.806],
-0.8:[0.132,0.856,1.166,1.448,1.606,1.733],-0.9:[0.148,0.854,1.147,1.407,1.549,1.660],
-1.0:[0.164,0.852,1.128,1.366,1.492,1.588],-1.2:[0.195,0.844,1.086,1.282,1.379,1.449],
-1.4:[0.225,0.832,1.041,1.198,1.270,1.318],-1.6:[0.254,0.817,0.994,1.116,1.166,1.197],
-1.8:[0.282,0.799,0.945,1.035,1.069,1.087],-2.0:[0.307,0.777,0.895,0.959,0.980,0.990],
-2.2:[0.330,0.752,0.844,0.888,0.900,0.905],-2.5:[0.360,0.711,0.771,0.793,0.798,0.799],
-3.0:[0.396,0.636,0.660,0.666,0.666,0.667]}
def K_lp3(Cs_val, T):
    keys = sorted(LP3.keys())
    j = LP3T.index(T)
    if Cs_val >= keys[-1]: return LP3[keys[-1]][j]
    if Cs_val <= keys[0]:  return LP3[keys[0]][j]
    for a,b in zip(keys,keys[1:]):
        if a <= Cs_val <= b:
            f = (Cs_val-a)/(b-a)
            return LP3[a][j] + f*(LP3[b][j]-LP3[a][j])
    raise ValueError

Ts = [2,5,10,25,50,100]
logX = np.log10(xmax); logXbar = logX.mean(); Slog = logX.std(ddof=1)
# Cs dari data LOG (rumus [15] tesis)
zlog = (logX-logXbar)/Slog
Cslog = n/((n-1)*(n-2)) * (zlog**3).sum()
# Gumbel sesuai prosedur tesis (dengan perbaikan typo): a = S/1.283 ; Xo = Xbar - 0.577a ; XT = Xo + Yp*a
aG = S/1.283
Xo = xbar - 0.577*aG
Xres = {}
for T in Ts:
    Xres[T] = dict(Normal=round(xbar + KN[T]*S,3),
                   Gumbel=round(Xo + YG[T]*aG,3),
                   LP3=round(10**(logXbar + K_lp3(Cslog,T)*Slog),3),
                   K_lp3=round(K_lp3(Cslog,T),4))
print(f"\nCs_log={Cslog:.4f} | Gumbel: a={aG:.4f} Xo={Xo:.4f}")
print("=== HASIL FREKUENSI (mm) ===")
for T in Ts:
    r = Xres[T]
    print(f"T={T:>3}  Normal={r['Normal']:9.3f}  Gumbel={r['Gumbel']:9.3f}  LP3={r['LP3']:9.3f} (K={r['K_lp3']})")

# ---- 6. CHI-KUADRAT ----
p = [0.50,0.20,0.10,0.06,0.04]
E = [n*pi for pi in p]
CHIC = {1:3.841, 2:5.991}
chi = {}
for dist, P in [("Normal",2),("Gumbel",2),("LP3",3)]:
    b = [Xres[2][dist], Xres[5][dist], Xres[10][dist], Xres[25][dist]]
    O = [0]*5
    for x in xmax:
        if x <= b[0]: O[0]+=1
        elif x <= b[1]: O[1]+=1
        elif x <= b[2]: O[2]+=1
        elif x <= b[3]: O[3]+=1
        else: O[4]+=1
    df = 5-1-P
    ch2 = sum((o-e)**2/e for o,e in zip(O,E))
    chi[dist] = dict(batas=[round(v,3) for v in b], O=O, E=[round(e,3) for e in E],
                     chi2=round(ch2,4), df=df, crit=CHIC[df], lolos=ch2<=CHIC[df])
    print(f"\n{dist}: batas={chi[dist]['batas']} O={O} chi2={ch2:.4f} df={df} kritik={CHIC[df]} -> {'LOLOS' if chi[dist]['lolos'] else 'GAGAL'}")
# urut prioritas saat chi2 seri: LP3 (standar SNI 2415:2016, df lebih ketat) > Gumbel > Normal
prio = ["LP3","Gumbel","Normal"]
lolos = {d:v for d,v in chi.items() if v['lolos']}
candi = lolos if lolos else chi
minv = min(candi[d]['chi2'] for d in candi)
chosen = next(d for d in prio if d in candi and abs(candi[d]['chi2']-minv) < 1e-9)
print(f">> DIPILIH: {chosen} (chi2={chi[chosen]['chi2']})")

# ---- 7. R24, tc, MONONOBE (rumus [19]-[22]), RASIONAL [23] ----
R24 = Xres[10][chosen]
Lo, Ss = 200.0, 0.002
Ld, nM, B, y = 300.0, 0.011, 0.30, 0.25
to = 0.0195*Lo**0.77/Ss**0.385
Vch = (1/nM)*((B*y)/(B+2*y))**(2/3)*math.sqrt(Ss)
td = Ld/(60*Vch)
tc = (to+td)/60
I = (R24/24)*((24/tc)**(2/3))     # rumus [19] sesuai tesis
Crun, Aha = 0.80, 10400/1e6
Q = 0.278*Crun*I*Aha
print(f"\n=== HASIL AKHIR ===")
print(f"R24 (T=10, {chosen}) = {R24:.3f} mm")
print(f"to={to:.2f} mnt  V={Vch:.3f} m/s  td={td:.2f} mnt  tc={tc:.4f} jam")
print(f"I Mononobe = ({R24:.1f}/24)*(24/{tc:.4f})^(2/3) = {I:.2f} mm/jam")
print(f"Q Rasional = 0.278*{Crun}*{I:.2f}*{Aha} = {Q:.4f} m3/dtk")
print(f"Va (th=1 jam) = {Q*3600:.1f} m3")

out = dict(years=ys_list, per_year=per_year, missing=missing_real,
           xmax=xmax.tolist(), xbar=float(xbar), S=float(S), Cv=float(Cv), Cs=float(Cs), Ck=float(Ck),
           t=dict(n1=n1,n2=n2,x1b=float(x1b),S1=float(S1),x2b=float(x2b),S2=float(S2),
                  sigma=float(sigma),t=float(t_hit),dk=dk),
           kons=dict(Sstar=Sstar.tolist(), Dy=float(Dy), Sstar_norm=Sstar_norm.tolist(),
                     Q=float(Q), qsqrt=float(qsqrt), q95=q_crit95, q99=q_crit99),
           gumbel=dict(a=float(aG), Xo=float(Xo)),
           logXbar=float(logXbar), Slog=float(Slog), Cslog=float(Cslog),
           freq=Xres, chi=chi, chosen=chosen,
           R24=float(R24), to=float(to), Vch=float(Vch), td=float(td), tc=float(tc),
           I=float(I), C=float(Crun), A_km2=Aha, Q=float(Q))
json.dump(out, open(ROOT / "data" / "processed" / "hasil_validasi.json", "w"), indent=1)
print("\n[ok] data/processed/hasil_validasi.json tersimpan")
