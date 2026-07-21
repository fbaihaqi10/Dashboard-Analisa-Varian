"""
Script untuk membangun 'data cube' ABO (Anggaran Biaya Operasional) dari file Excel mentah
(sheet 'Real (FBL+Extra)', hasil copy-paste dari FBL3N/EXTRACOMP).

Cara pakai tiap bulan:
    python build_abo_cube.py "Data_Anggaran_Biaya_Operasional__ABO__Ytd_<Bulan>_2026.xlsx" abo-cube.json

Output: 1 file JSON kompak (dictionary-encoded) berisi SEMUA transaksi Jan-Bulan berjalan,
sudah diagregasi ke level kombinasi dimensi (bukan per-baris transaksi mentah) supaya ringan
di-load browser. Kolom 'Bulan' tetap disimpan per baris sehingga dashboard bisa hitung YTD
kumulatif untuk periode apa pun (April/Mei/Juni/dst) tanpa perlu file terpisah per bulan.
"""

import sys
import json
import pandas as pd

DIMENSIONS = ['Mapping Region', 'KK Report', 'Direktorat', 'CE Komut', 'CE Subkomut',
              'VP Pengusul', 'COGS/BU', 'Include/Exclude']
DIM_KEYS = {
    'Mapping Region': 'region', 'KK Report': 'kk', 'Direktorat': 'direktorat',
    'CE Komut': 'cekomut', 'CE Subkomut': 'cesubkomut', 'VP Pengusul': 'vp',
    'COGS/BU': 'cogsbu', 'Include/Exclude': 'incexc',
}


def build_cube(excel_path, output_path):
    df = pd.read_excel(excel_path, sheet_name='Real (FBL+Extra)', header=4, usecols=range(20))
    df.columns = [c.strip() for c in df.columns]

    before_total = df['Amount usd'].sum()
    df = df.dropna(subset=['Bulan']).copy()

    for c in DIMENSIONS:
        df[c] = df[c].astype(str).str.strip()
        df[c] = df[c].replace({'0': 'Tidak Terklasifikasi', 'nan': 'Tidak Terklasifikasi'})

    df['Bulan'] = df['Bulan'].astype(int)

    agg = df.groupby(DIMENSIONS + ['Bulan'], as_index=False)['Amount usd'].sum()

    after_total = agg['Amount usd'].sum()
    diff = abs(after_total - before_total)
    print(f"Total sebelum agregasi (termasuk baris kosong): {before_total:,.2f}")
    print(f"Total setelah agregasi: {after_total:,.2f}")
    print(f"Selisih: {diff:,.2f}")
    if diff > 1000:
        print("PERINGATAN: selisih cukup besar, cek ulang data mentahnya!")

    dicts = {}
    codes = {}
    for col, key in DIM_KEYS.items():
        uniques = sorted(agg[col].unique().tolist())
        dicts[key] = uniques
        codes[col] = {v: i for i, v in enumerate(uniques)}

    rows = []
    for _, r in agg.iterrows():
        rows.append([
            int(r['Bulan']),
            codes['Mapping Region'][r['Mapping Region']],
            codes['KK Report'][r['KK Report']],
            codes['Direktorat'][r['Direktorat']],
            codes['CE Komut'][r['CE Komut']],
            codes['CE Subkomut'][r['CE Subkomut']],
            codes['VP Pengusul'][r['VP Pengusul']],
            codes['COGS/BU'][r['COGS/BU']],
            codes['Include/Exclude'][r['Include/Exclude']],
            round(float(r['Amount usd']), 2),
        ])

    output = {
        'dims': dicts,
        'colOrder': ['bulan', 'region', 'kk', 'direktorat', 'cekomut', 'cesubkomut', 'vp', 'cogsbu', 'incexc', 'amount'],
        'rows': rows,
        'meta': {
            'source': excel_path.split('/')[-1],
            'grandTotal': round(float(after_total), 2),
            'monthsAvailable': sorted(agg['Bulan'].unique().tolist()),
        },
    }

    with open(output_path, 'w') as f:
        json.dump(output, f, separators=(',', ':'))

    print(f"Selesai. Disimpan ke {output_path} ({len(rows)} baris kombinasi).")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Cara pakai: python build_abo_cube.py <file_excel.xlsx> <output.json>")
        sys.exit(1)
    build_cube(sys.argv[1], sys.argv[2])
