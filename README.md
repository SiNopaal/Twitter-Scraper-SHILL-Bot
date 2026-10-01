# 𝕏 Shill.Money Autonomous Clock-In Campaign & Squad Raid Bot 🚀

Suite bot otomatisasi multi-akun Twitter / X khusus untuk kampanye SocialFi **Shill.Money** ([https://shill.money/clock-in](https://shill.money/clock-in)). 

Dirancang untuk memaksimalkan perolehan poin leaderboard secara organik dan terkoordinasi melalui postingan unik dengan media grafis serta cross-engagement antar akun.

---

## 🌟 Fitur Utama

### 1. 📢 Task 1: Pembuatan Postingan Promosi Unik (Fase 1)
- Setiap akun aktif membuat postingan promosi yang **100% unik tanpa duplikasi teks**.
- Memenuhi seluruh kriteria skor tertinggi:
  - **Ticker**: `$SHILL` (+10 Poin)
  - **Contract Address (EVM)**: `0x93cfF6Dc0cf59680b8d85b9F3312a24bF1a7c1D8` (+20 Poin)
  - **Tag Resmi**: `@shillmoneyrh`
  - **Lampiran Media Grafis**: Poster badge shift unik per akun (+10 Poin)
  - **Identitas Jam Kerja**: Proof-of-work clock-in paycheck statement (+15 Poin)

### 2. 🎨 Generator Gambar Unik 100% Prosedural (`generate_shill_images.py`)
- Tidak menggunakan AI API (0 token / 100% gratis).
- Menghasilkan 8 poster badge resolusi tinggi (1200 x 675 px) dengan tema visual, palet warna, layout kartu, dan nomor shift yang sepenuhnya berbeda untuk setiap akun:
  - **Cyan Terminal Grid** (`Operator 1`)
  - **Gold Paycheck Radar** (`Operator 2`)
  - **Emerald Green Matrix** (`Operator 3`)
  - **Purple Mining Pass** (`Operator 4`)
  - **Crimson Rose Statement** (`Operator 5`)
  - **Solar Amber Validator** (`Operator 6`)
  - **Oceanic Aqua Protocol** (`Operator 7`)
  - **Cyber Lime Modern** (`Operator 8`)

### 3. 🔥 Task 2: Cross-Engagement Raid Squad (Fase 2)
- Setelah semua akun selesai mempublikasikan postingan masing-masing di Task 1, seluruh akun bergantian saling berkunjung ke postingan akun lainnya untuk melakukan:
  - ❤️ **Like** (+1 Poin)
  - 🔁💬 **Quote Tweet** (+Poin Multiplier Tertinggi dengan `Contract address $SHILL: 0x93cfF6Dc0cf59680b8d85b9F3312a24bF1a7c1D8`)
  - 🔁 **Retweet / Repost** (+3 Poin)
  - 💬 **Contextual Reply / Komentar Kontekstual** (+2 Poin)

### 4. ⏱️ Looping Terjadwal Kontinu (Jeda Acak 5–10 Menit Antar Siklus)
- **Urutan Siklus**:
  1. Task 1 (Postingan Unik) selesai untuk 6 akun kreator.
  2. Task 2 (Raid squad: Like, Quote, Retweet, Reply) selesai untuk seluruh 8 akun.
  3. Masuk mode **Sleep / Istirahat secara acak selama 5–10 Menit (300–600 detik)** untuk menghindari deteksi pola bot secara berkala.
  4. Siklus berikutnya otomatis berjalan kembali dengan ID shift baru dan gambar unik.

---

## 🛠️ Panduan Instalasi & Penggunaan

### 1. Prasyarat Sistem
- Python 3.10+
- Google Chrome terinstal

### 2. Pasang Dependensi
```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Konfigurasi Akun (`accounts.json`)
Salin template konfigurasi:
```bash
cp accounts.json.example accounts.json
```
Isi token sesi `auth_token` dan `ct0` untuk masing-masing akun Twitter Anda.

### 4. Menjalankan Bot
```bash
# Menghasilkan gambar poster unik:
python generate_shill_images.py

# Menjalankan bot kampanye autonomous:
python shill_campaign_bot.py
```

---

## 🔒 Keamanan Kredensial
File sensitif seperti `accounts.json`, `cookies.json`, folder `results/`, dan file log secara ketat diabaikan oleh `.gitignore` sehingga tidak akan pernah terunggah ke repositori publik.
