# Summary P&L — RKAP vs Realisasi (Dashboard)

Dashboard interaktif untuk membandingkan **Realisasi** dengan **RKAP 2026 (Full Year)**, **RKAP Proporsional (YTD Mei)**, atau **Prognosa 2026** — dibuat dari sheet `Summary PL-All`.

Semua langkah di bawah ini dilakukan **lewat browser di github.com saja**. Tidak perlu install VS Code, Git, Node.js, atau apa pun di komputer.

---

## Isi repo ini

```
├── index.html          ← halaman dashboard (tampilan, chart, tabel)
├── data/
│   └── summary_pl.json ← semua ANGKA. Ubah file ini kalau mau update data.
└── README.md            ← file ini
```

`index.html` **tidak berisi angka sama sekali** — semua angka ada di `data/summary_pl.json` dan diambil (`fetch`) saat halaman dibuka. Jadi untuk update data bulan berikutnya, kamu cukup edit file JSON itu, tidak perlu sentuh kode HTML/JS.

---

## 1. Buat repository baru

1. Buka [github.com](https://github.com) dan login.
2. Klik tombol **+** di kanan atas → **New repository**.
3. Isi nama repo, misalnya `pl-dashboard-rkap-realisasi`.
4. Pilih **Public** (supaya GitHub Pages gratis bisa dipakai), lalu klik **Create repository**.

## 2. Upload file (drag & drop, tanpa Git)

1. Di halaman repo yang baru dibuat, klik **Add file → Upload files**.
2. Download 3 file dari chat ini (`index.html`, folder `data` berisi `summary_pl.json`, dan `README.md`), lalu **drag & drop** semuanya ke halaman upload GitHub. Pastikan strukturnya tetap `data/summary_pl.json` (bukan taruh langsung di root) — GitHub otomatis membuat folder `data` kalau kamu drag foldernya, atau kamu bisa buat folder `data` dulu di repo lalu upload json ke dalamnya.
3. Scroll ke bawah, klik **Commit changes**.

## 3. Aktifkan GitHub Pages (supaya jadi link hidup)

1. Di repo, klik tab **Settings**.
2. Di sidebar kiri, klik **Pages**.
3. Di bagian **Build and deployment → Source**, pilih **Deploy from a branch**.
4. Branch: pilih **main**, folder: **/(root)**, klik **Save**.
5. Tunggu 1–2 menit, refresh halaman itu — akan muncul link seperti:
   `https://<username-kamu>.github.io/pl-dashboard-rkap-realisasi/`
6. Buka link itu — dashboard langsung jalan, bisa dibuka di HP atau laptop mana saja.

> ⚠️ **Jangan buka `index.html` dengan cara dobel-klik dari komputer.** Browser akan memblokir pengambilan data JSON-nya (CORS) kalau dibuka lewat `file://`. Harus lewat link GitHub Pages di atas (atau server web apa pun).

## 4. Update data di kemudian hari (tanpa install apa pun)

1. Buka repo di github.com, masuk ke `data/summary_pl.json`.
2. Klik ikon pensil (**Edit this file**) di kanan atas file.
3. Ubah angka yang perlu diupdate langsung di editor browser GitHub.
4. Scroll ke bawah, klik **Commit changes** (langsung ke branch `main`).
5. Tunggu ±1 menit, refresh link GitHub Pages kamu — data sudah ter-update otomatis.

### Struktur `summary_pl.json`

- `lines[]` — daftar komponen P&L. Tiap komponen punya:
  - `a` = RKAP 2026 (Full Year)
  - `b` = RKAP 2026 Proporsional YTD Mei
  - `c` = Realisasi YTD Mei
  - `d` = Prognosa 2026
  - `unit`: `"currency"` (US$ Juta) atau `"percent"` (disimpan sebagai pecahan, misalnya `0.05` = 5.0%)
  - `hib` (higher-is-better): `true` kalau angka lebih besar = lebih baik, `false` kalau sebaliknya (contoh: BOPO)
- `chips[]` — metrik tambahan (Volume Opsen, Kurs Transaksi, Kurs Neraca)
- `meta` — label periode, satuan, sumber data, dan teks caption per basis pembanding

Untuk menambah bulan berikutnya (misal Juni), cukup update nilai `c` (Realisasi) di setiap baris — tidak perlu ubah struktur file.

---

## Fitur dashboard

- Toggle basis pembanding (RKAP Full Year / RKAP Proporsional / Prognosa)
- Cross-filter: klik bar chart, baris tabel, atau kartu KPI saling menyorot
- Tabel bisa disortir & dicari, plus tombol unduh CSV
- Insight otomatis menyebut komponen paling favorable/unfavorable

## Batasan

Ini dashboard berbasis file statis (`data/summary_pl.json`), bukan koneksi live ke Excel/database. Untuk refresh otomatis tanpa edit manual, langkah lanjutannya adalah menghubungkan sumber data (mis. Google Sheets API, atau Power Query yang mem-publish ke endpoint) — bisa didiskusikan lebih lanjut kalau dibutuhkan.

