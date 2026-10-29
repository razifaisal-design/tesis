# -*- coding: utf-8 -*-
"""Analisis hidrologi Stasiun Ambawang 2012-2025 sesuai Proposal Tesis Rajawali Residence."""
import math, json, datetime
import pandas as pd
import numpy as np

from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "requirements.txt").exists())
F = ROOT / "data" / "raw" / "Curah_Hujan_Sungai_Ambawang_BWSK_2012-2025.xlsx"
if not F.exists():
    F = ROOT / "data" / "sample" / F.name

# ---------- 1. PARSE DATA (matrix per tahun: row=tanggal, col=bulan) ----------
DAYS_IN_MONTH = [31,28,31,30,31,30,31,31,30,31,30,31]
records = []      # (tahun, bulan, tanggal, mm|None)
missing_real = [] # tanggal valid tapi kosong
per_year = {}

xl = pd.ExcelFile(F)
for ys in xl.sheet_names:
    y = int(ys)
    df = pd.read_excel(F, sheet_name=ys, header=None)
    # header TANGGAL/BULAN di row 17 (0-indexed), data mulai row 18, 12 kolom bulan
    # deteksi robust: cari baris yang berisi 'TANGGAL' di col 0
    hdr = None
    for r in range(df.shape[0]):
        v0 = df.iat[r,0]
        v1 = df.iat[r,1]
        if (isinstance(v0,str) and v0.strip().upper()=='TANGGAL'
            and isinstance(v1,str) and v1.strip().lower() in ('jan','febuar','febr')):
            hdr = r; break
    if hdr is None:
        for r in range(df.shape[0]):
            v0 = df.iat[r,0]
            v1 = df.iat[r,1]
            if isinstance(v0,str) and v0.strip().upper()=='TANGGAL' and isinstance(v1,str) and v1.strip()[:3].lower()=='jan':
                hdr = r; break
    assert hdr is not None, f"header tidak ditemukan di {ys}"
    for d in range(1,32):
        r = hdr + d
        if r >= df.shape[0]: break
        for b in range(12):
            if d > DAYS_IN_MONTH[b]:
                continue  # tanggal tidak ada (Feb 30 dst)
            val = df.iat[r, b+1]
            mm = None
            if isinstance(val,(int,float)) and not (isinstance(val,float) and math.isnan(val)):
                mm = float(val)
            else:
                missing_real.append((y,b+1,d))
            records.append((y,b+1,d,mm))
    # ringkasan per tahun dari data yang ada
    yrs = [ (b,d,v) for (yy,b,d,v) in records if yy==y and v is not None ]
    tot = sum(v for _,_,v in yrs)
    xmax = max(v for _,_,v in yrs) if yrs else None
    nh = sum(1 for _,_,v in yrs if v>0)
    nvalid = sum(1 for (yy,b,d,_) in records if yy==y)
    last_b = max((b for (yy,b,d,_) in records if yy==y), default=None)
    per_year[y] = dict(total=round(tot,1), xmax=xmax, hari_hujan=nh,
                       n_valid=nvalid, n_missing=sum(1 for (yy,b,d) in missing_real if yy==y),
                       last_bulan=last_b)

print("=== RINGKASAN PER TAHUN ===")
for y,v in per_year.items():
    print(y, v)
print("\nTanggal valid yang KOSONG (data hilang):", len(missing_real))
for t in missing_real[:40]: print("  ", t)

# ---------- 2. SERI XMAX ----------
ys_list = sorted(per_year)
xmax = np.array([per_year[y]['xmax'] for y in ys_list], dtype=float)
n = len(xmax)
print("\n=== XMAX TAHUNAN ===")
print(dict(zip(ys_list, xmax.tolist())))

xbar = xmax.mean()
S = xmax.std(ddof=1)
Cv = S/xbar
Cs = n/((n-1)*(n-2)) * (((xmax-xbar)/S)**3).sum()
Ck = n*(n+1)/((n-1)*(n-2)*(n-3)) * (((xmax-xbar)/S)**4).sum() - 3*(n-1)**2/((n-2)*(n-3))
print(f"\nXbar={xbar:.4f} S={S:.4f} Cv={Cv:.4f} Cs={Cs:.4f} Ck={Ck:.4f}")

# ---------- 3. UJI HOMOGENITAS (Uji-t, 2 set, S pembagi N sesuai tesis) ----------
n1 = n//2; n2 = n-n1
x1, x2 = xmax[:n1], xmax[n1:]
x1b, x2b = x1.mean(), x2.mean()
S1 = math.sqrt(((x1-x1b)**2).sum()/n1)   # pembagi N (sesuai tesis 2.3.2)
S2 = math.sqrt(((x2-x2b)**2).sum()/n2)
t_hit = abs(x1b-x2b)/math.sqrt(S1**2/n1 + S2**2/n2)
dk = n1+n2-2
# tabel 2.2: dk=12, alpha=0.05 -> 2.179 (dua arah)
TCRIT = {1:6.314,2:2.920,3:2.353,4:2.132,5:2.015,6:1.943,7:1.895,8:1.860,9:1.833,10:1.812,
         11:1.796,12:1.782,13:1.771,14:1.761}
t_crit = TCRIT[dk]
print(f"\n=== UJI HOMOGENITAS (Uji-t) ===\nset1 {ys_list[0]}-{ys_list[n1-1]}: Xbar1={x1b:.3f} S1={S1:.4f} n1={n1}")
print(f"set2 {ys_list[n1]}-{ys_list[-1]}: Xbar2={x2b:.3f} S2={S2:.4f} n2={n2}")
print(f"t_hitung={t_hit:.4f} dk={dk} t_kritis(a=5%)={t_crit:.3f} -> {'HOMOGEN' if t_hit<t_crit else 'TIDAK HOMOGEN'}")

# ---------- 4. UJI KONSISTENSI (Cumulative Deviation) ----------
Sstar = np.cumsum(xmax - xbar)
Q = np.abs(Sstar).max()
q_sqrt_n = Q/math.sqrt(n)
# tabel 2.3: interpolasi n=14 antara 10 (1.14) dan 20 (1.22) pada 95%
q_crit = 1.14 + (14-10)/(20-10)*(1.22-1.14)
print(f"\n=== UJI KONSISTENSI ===\nQ={Q:.4f} Q/sqrt(n)={q_sqrt_n:.4f} Q/sqrt(n)_kritik(n=14,95%)={q_crit:.4f}")
print("->", "KONSISTEN" if q_sqrt_n<q_crit else "TIDAK KONSISTEN")

# ---------- 5. ANALISIS FREKUENSI ----------
# Tabel 2.4 Normal (Kp): T:2,5,10,25,50,100
KN = {2:0.84,5:1.64,10:2.33,25:3.09,50:3.90,100:4.60}
# Tabel 2.5 Gumbel (Yp)
YG = {2:0.366,5:1.510,10:2.250,25:3.900,50:4.600,100:5.290}
# Tabel 2.6 K LP3 (Cs, T)
LP3T = [2,5,10,25,50,100]
LP3 = {  # Cs: [K2,K5,K10,K25,K50,K100]
3.0:[-0.396,0.420,1.180,2.278,3.152,4.051], 2.5:[-0.360,0.518,1.250,2.262,3.048,3.845],
2.2:[-0.330,0.574,1.284,2.240,2.970,3.705], 2.0:[-0.307,0.609,1.302,2.219,2.912,3.605],
1.8:[-0.282,0.643,1.318,2.193,2.848,3.499], 1.6:[-0.254,0.675,1.329,2.163,2.780,3.388],
1.4:[-0.225,0.705,1.337,2.128,2.706,3.271], 1.2:[-0.195,0.732,1.340,2.087,2.626,3.149],
1.0:[-0.164,0.758,1.340,2.043,2.542,3.022], 0.9:[-0.148,0.769,1.339,2.018,2.498,2.957],
0.8:[-0.132,0.780,1.336,1.998,2.453,2.891], 0.7:[-0.116,0.790,1.333,1.967,2.407,2.824],
0.6:[-0.099,0.800,1.328,1.939,2.359,2.755], 0.5:[-0.083,0.808,1.323,1.910,2.311,2.686],
0.4:[-0.066,0.816,1.317,1.880,2.261,2.615], 0.3:[-0.050,0.824,1.309,1.849,2.211,2.544],
0.2:[-0.033,0.830,1.301,1.818,2.159,2.472], 0.1:[-0.017,0.836,1.292,1.785,2.107,2.400],
0.0:[0.000,0.842,1.282,1.751,2.054,2.326], -0.1:[0.017,0.846,1.270,1.716,2.000,2.252],
-0.2:[0.033,0.850,1.258,1.680,1.945,2.178], -0.3:[0.050,0.853,1.245,1.643,1.890,2.104],
-0.4:[0.066,0.855,1.231,1.606,1.834,2.029], -0.5:[0.083,0.856,1.216,1.567,1.777,1.955],
-0.6:[0.099,0.857,1.200,1.528,1.720,1.880], -0.7:[0.116,0.857,1.183,1.488,1.663,1.806],
-0.8:[0.132,0.856,1.166,1.448,1.606,1.733], -0.9:[0.148,0.854,1.147,1.407,1.549,1.660],
-1.0:[0.164,0.852,1.128,1.366,1.492,1.588], -1.2:[0.195,0.844,1.086,1.282,1.379,1.449],
-1.4:[0.225,0.832,1.041,1.198,1.270,1.318], -1.6:[0.254,0.817,0.994,1.116,1.166,1.197],
-1.8:[0.282,0.799,0.945,1.035,1.069,1.087], -2.0:[0.307,0.777,0.895,0.959,0.980,0.990],
-2.2:[0.330,0.752,0.844,0.888,0.900,0.905], -2.5:[0.360,0.711,0.771,0.793,0.798,0.799],
-3.0:[0.396,0.636,0.660,0.666,0.666,0.667]}
def K_lp3(Cs_val, T):
    keys = sorted(LP3.keys())
    if Cs_val >= keys[0]: return LP3[keys[0]][LP3T.index(T)]
    if Cs_val <= keys[-1]: return LP3[keys[-1]][LP3T.index(T)]
    for a,b in zip(keys,keys[1:]):
        if b <= Cs_val <= a:  # keys descending in value? keys sorted asc: -3..3
            lo, hi = min(a,b), max(a,b)
            f = (Cs_val-lo)/(hi-lo)
            return LP3[lo][LP3T.index(T)] + f*(LP3[hi][LP3T.index(T)]-LP3[lo][LP3T.index(T)])
    raise ValueError

Ts = [2,5,10,25,50,100]
logX = np.log10(xmax)
logXbar = logX.mean()
Slog = logX.std(ddof=1)
Xres = {}
for T in Ts:
    XN = xbar + KN[T]*S
    XG = xbar + (S*math.sqrt(6)/math.pi)*YG[T]
    K = K_lp3(Cs, T)
    XL = 10**(logXbar + K*Slog)
    Xres[T] = dict(Normal=round(XN,3), Gumbel=round(XG,3), LP3=round(XL,3), K=round(K,4))
print("\n=== HASIL FREKUENSI (mm) ===")
for T in Ts:
    print(f"T={T:>3} th  Normal={Xres[T]['Normal']:8.3f}  Gumbel={Xres[T]['Gumbel']:8.3f}  LP3={Xres[T]['LP3']:8.3f} (K={Xres[T]['K']})")

# ---------- 6. UJI CHI-KUADRAT (5 kelas dibatasi R2,R5,R10,R25) ----------
# peluang kelas: (-inf,R2]=0.50, (R2,R5]=0.20, (R5,R10]=0.10, (R10,R25]=0.06, (R25,inf)=0.04
p = [0.50,0.20,0.10,0.06,0.04]
E = [n*pi for pi in p]
CHIC = {1:3.841, 2:5.991}
chi = {}
for dist, P in [("Normal",2),("Gumbel",2),("LP3",3)]:
    b = [Xres[2][dist], Xres[5][dist], Xres[10][dist], Xres[25][dist]]
    O = [0,0,0,0,0]
    for x in xmax:
        if x <= b[0]: O[0]+=1
        elif x <= b[1]: O[1]+=1
        elif x <= b[2]: O[2]+=1
        elif x <= b[3]: O[3]+=1
        else: O[4]+=1
    df = 5-1-P
    ch2 = sum((o-e)**2/e for o,e in zip(O,E))
    ok = ch2 <= CHIC[df]
    chi[dist] = dict(batas=[round(v,3) for v in b], O=O, E=[round(e,3) for e in E],
                     chi2=round(ch2,4), df=df, crit=CHIC[df], lolos=ok)
    print(f"\n{dist}: batas={chi[dist]['batas']}")
    print(f"  O={O} E={chi[dist]['E']} chi2={ch2:.4f} df={df} kritik={CHIC[df]} -> {'LOLOS' if ok else 'GAGAL'}")
# pilih: chi2 terkecil yang lolos
lolos = {d:v for d,v in chi.items() if v['lolos']}
if lolos:
    chosen = min(lolos, key=lambda d: lolos[d]['chi2'])
else:
    chosen = min(chi, key=lambda d: chi[d]['chi2'])
print(f"\n>> Distribusi terpilih: {chosen} (chi2={chi[chosen]['chi2']})")

# ---------- 7. R24, tc, MONONOBE, RASIONAL ----------
R24 = Xres[10][chosen]
# Asumsi site (ganti dgn data lapangan):
Lo, Ss = 30.0, 0.005        # panjang overland (m), kemiringan (m/m)
Lc, nM, B, y, Hp = 100.0, 0.011, 0.30, 0.30, 0.35  # saluran beton
to = 0.0195*Lo**0.77/Ss**0.385   # menit (Kirpich)
A_ch, Pw = B*y, B+2*y
Vch = (1/nM)*(A_ch/Pw)**(2/3)*math.sqrt(Ss)
td = Lc/Vch/60
tc = (to+td)/60  # jam
I = R24/(tc*math.sqrt(tc))  # Mononobe mm/jam
Crun, Aha = 0.80, 10400/1000000  # C seng 0.70-0.90 ambil 0.80; A atap = 1.04 ha = 0.0104 km2
Q = 0.278*Crun*I*Aha
print(f"\n=== HASIL AKHIR ===")
print(f"R24 (T=10 th, {chosen}) = {R24:.3f} mm")
print(f"to(Kirpich)={to:.2f} mnt  Vsal={Vch:.3f} m/s  td={td:.2f} mnt  tc={tc:.4f} jam")
print(f"I Mononobe = {I:.2f} mm/jam")
print(f"Q Rasional = 0.278 x {Crun} x {I:.2f} x {Aha} = {Q:.4f} m3/dtk")
print(f"Va atenuasi (th=1 jam) = Q x th = {Q*3600:.1f} m3")

# ---------- 8. SIMPAN SEMUA UNTUK EXCEL ----------
out = dict(years=ys_list, per_year=per_year, missing=missing_real,
           xmax=xmax.tolist(), xbar=xbar, S=S, Cv=Cv, Cs=Cs, Ck=Ck,
           t=dict(n1=n1,n2=n2,x1b=x1b,S1=S1,x2b=x2b,S2=S2,t=t_hit,dk=dk,tcrit=t_crit),
           kons=dict(Sstar=Sstar.tolist(), Q=Q, qsqrt=q_sqrt_n, qcrit=q_crit),
           freq=Xres, chi=chi, chosen=chosen,
           R24=R24, to=to, Vch=Vch, td=td, tc=tc, I=I, C=Crun, A_km2=Aha, Q=Q)
json.dump(out, open(ROOT / "data" / "processed" / "hasil_legacy.json", "w"), indent=1, default=str)
print("\n[ok] data/processed/hasil_legacy.json tersimpan")
