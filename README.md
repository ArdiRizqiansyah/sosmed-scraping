# SosmedPulse - Social Media & Trend Listening AI Platform

Platform web *Social Media & Trend Listening Intelligence* berbasis **FastAPI (Python)**, **OpenRouter AI (Nvidia Nemotron / Minimax)**, **Tailwind CSS**, dan **Chart.js**.

---

## 🚀 Fitur Utama

- **Targeted Multi-Platform Social Scraping**:
  - Mengambil perbincangan publik dari **TikTok**, **Instagram**, **X (Twitter)**, **YouTube**, **LinkedIn**, dan **Media Berita** secara real-time.
- **OpenRouter AI Intelligence**:
  - Ringkasan Eksekutif AI (*Executive Summary*) tentang persepsi publik terhadap brand.
  - Ekstraksi otomatis *Positive Drivers* (pujian/kelebihan produk) dan *Negative Drivers* (keluhan/kritik).
  - Rekomendasi bisnis strategis (*Actionable Advice*) bagi pemilik brand.
- **Aspect-Based Sentiment Analysis (ABSA)**:
  - Membedah sentimen ke dalam 4 pilar bisnis:
    1. 📦 **Kualitas & Fitur Produk**
    2. 💰 **Harga & Nilai (Value for Money)**
    3. 🚚 **Pengiriman & Kemasan**
    4. 💬 **Pelayanan Pelanggan (Customer Service)**
- **PR Crisis & Risk Alert Detector**:
  - Mendeteksi kemunculan kata kunci berisiko tinggi (*penipuan, scam, palsu, rusak parah, dll*) beserta indikator status reputasi brand (**Aman / Waspada / Peringatan Krisis**).
- **Filter Rentang Waktu**:
  - Pilihan rentang waktu pencarian: *Semua Waktu*, *30 Hari Terakhir*, *7 Hari Terakhir*, dan *24 Jam Terakhir*.
- **Visualisasi Dashboard Interaktif**:
  - Donut Chart distribusi sentimen (Positif, Netral, Negatif).
  - Bar Chart sebaran saluran media.
  - Tag Cloud kata kunci terpopuler (*Trending Keywords*).
  - Net Sentiment Score (NSS: -100 s/d +100).
- **Ekspor & Cetak Laporan**:
  - **Ekspor CSV** data percakapan.
  - **Cetak / Simpan PDF** laporan analisis eksekutif siap presentasi.
- **Riwayat Pencarian Cepat**:
  - Menyimpan riwayat pencarian produk favorit di browser secara otomatis.

---

## 🛠️ Cara Menjalankan

1. **Install Dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Jalankan Aplikasi**:
   ```bash
   python main.py
   ```

3. **Buka di Browser**:
   Buka [http://localhost:8000](http://localhost:8000) di browser Anda.

---

## 📁 Struktur Proyek

```
sosmed-scraping/
├── main.py              # Server FastAPI & API Routing
├── scraper.py           # Multi-platform social & news data scraper
├── analyzer.py          # Indonesian NLP & Aspect-Based Sentiment Engine
├── ai_service.py        # OpenRouter AI Integration
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html       # Dashboard UI (Tailwind CSS, Chart.js, Lucide Icons)
└── static/              # Static assets
```
