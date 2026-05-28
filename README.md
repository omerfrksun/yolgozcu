<div align="center">

# 🛣️ YolGözcü
### AI Destekli Gerçek Zamanlı Yol Hasar Tespit ve Maliyet Tahminleme Sistemi

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-seg-FF6B35?style=flat&logo=ultralytics&logoColor=white)](https://ultralytics.com)
[![Leaflet](https://img.shields.io/badge/Leaflet.js-1.9-199900?style=flat&logo=leaflet&logoColor=white)](https://leafletjs.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

> **iş'te Yapay Zeka Hackathonu** — 24 saatte geliştirildi · 3 kişilik ekip

[Demo Video](#-demo) · [Kurulum](#-kurulum) · [API Docs](#-api) · [Ekip](#-ekip)

</div>

---

## 📌 Proje Hakkında

YolGözcü, belediye hizmet araçlarının ön camına yerleştirilen akıllı telefon kameraları aracılığıyla **seyir halindeyken** yoldaki çukur ve çatlakları tespit eden, bunları haritada konumlandıran ve onarım için gereken tahmini malzeme miktarı ile maliyeti hesaplayan bilgisayarlı görü tabanlı bir yol kalite yönetim sistemidir.

### Problem
- Türkiye'de yol hasarları reaktif sistemle yönetiliyor: vatandaş şikayet ediyor → geç müdahale → yüksek maliyet
- Manuel tespit hem yavaş hem maliyetli
- Fen işleri hasar önceliğini ve bütçeyi anlık göremiyor

### Çözüm
Rutin görevlerini yapan belediye araçları aynı zamanda **gezici yol tarama sistemine** dönüşüyor.

---

## 🎥 Demo

| Ekran | Açıklama |
|:---:|:---|
| **Sürücü Ekranı** | YOLOv8-seg bbox tespiti · GPS overlay · Anlık sayaç |
| **Harita Panosu** | Leaflet.js canlı harita · Renk kodlu önceliklendirme · Mali panel |
| **Mobil Uygulama** | 4 ekranlı PWA · Ana sayfa · Kamera · Harita · Rapor |

---

## ✨ Özellikler

- 🔴 **Gerçek zamanlı tespit** — YOLOv8-seg ile saniyede 45 kareye kadar işlem
- 📍 **GPS entegrasyonu** — Her hasar koordinatıyla haritaya pinlenir
- 💰 **Maliyet tahmini** — Hacim hesabı × asfalt yoğunluğu × birim fiyat
- 🗺️ **Canlı harita** — Kırmızı/Sarı/Yeşil renk kodlu öncelik sistemi
- 📱 **Mobil arayüz** — Sürücü ve fen işleri için ayrı ekranlar
- 📊 **Mali rapor** — Malzeme, işçilik, lojistik kırılımlı bütçe özeti
- 🔄 **REST API** — GeoJSON formatında standart çıktı

---

## 🏗️ Teknik Mimari

```
Araç Kamerası
      │
      ▼
┌─────────────────┐
│  YOLOv8-seg     │  ← Segmentasyon + Bbox tespiti
│  Monoküler      │  ← Derinlik kestirimi (Olaye et al.)
│  Derinlik       │  ← Hacim = alan × derinlik
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI       │  ← REST API Backend
│   Backend       │  ← GeoJSON endpoint'leri
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Leaflet.js     │  ← OpenStreetMap üzeri harita
│  Harita Panosu  │  ← Canlı pin animasyonları
│  Mali Rapor     │  ← Bütçe kırılım paneli
└─────────────────┘
```

---

## 🤖 Yapay Zeka Modeli

| Özellik | Detay |
|---------|-------|
| Model | YOLOv8-seg (segmentasyon) |
| Hız | 45 FPS (mobil uyumlu) |
| Derinlik tahmini | Monoküler projeksiyon |
| Hata toleransı | Derinlik ±%3.4, Genişlik ±%3.8 (Olaye et al.) |
| Asfalt yoğunluğu | 2.350 kg/m³ |
| Birim fiyat | 4.500 TL/ton |

### Severity Sınıflandırması

| Renk | Seviye | Kriter |
|------|--------|--------|
| 🔴 Kırmızı | Kritik | Derinlik > 12 cm veya maliyet > 4.000 ₺ |
| 🟡 Sarı | Orta | Derinlik 5-12 cm veya maliyet 1.500-4.000 ₺ |
| 🟢 Yeşil | Hafif | Derinlik < 5 cm veya maliyet < 1.500 ₺ |

---

## 📁 Proje Yapısı

```
yolgozcu/
├── app.py                  # FastAPI backend
├── index.html              # Fen işleri harita panosu
├── driver.html             # Sürücü tespit ekranı
├── mobile.html             # Mobil uygulama arayüzü
├── simulate_camera.py      # GPS rota simülatörü (demo)
├── requirements.txt
└── README.md
```

---

## 🚀 Kurulum

### Gereksinimler

- Python 3.10+
- Modern web tarayıcı

### Backend

```bash
# Repo'yu klonla
git clone https://github.com/omerfrksun/yolgozcu.git
cd yolgozcu

# Bağımlılıkları yükle
pip install fastapi uvicorn python-multipart

# Sunucuyu başlat
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
# Fen işleri harita panosu
open index.html          # veya VS Code Live Server

# Sürücü ekranı
open driver.html

# Mobil uygulama
open mobile.html
```

### Demo Simülatörü

```bash
# Gerçek kamera olmadan demo için
pip install requests
python simulate_camera.py
```

---

## 📡 API

Sunucu başladıktan sonra Swagger UI: `http://localhost:8000/docs`

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| `GET` | `/api/defects` | Tüm hasarları GeoJSON olarak döner |
| `GET` | `/api/report` | Mali özet raporu |
| `POST` | `/api/detect` | Yeni hasar tespiti ekler |
| `DELETE` | `/api/detections` | Tüm kayıtları temizler |

### Örnek İstek

```bash
curl -X POST "http://localhost:8000/api/detect" \
  -H "Content-Type: application/json" \
  -d '{
    "lat": 40.9901,
    "lon": 29.0234,
    "address": "Moda Caddesi, Kadıköy",
    "damage_type": "çukur",
    "severity": "Kritik",
    "width_cm": 85.5,
    "depth_cm": 14.2,
    "material_cost": 5200.00,
    "labor_cost": 3120.00,
    "logistic_cost": 2080.00,
    "total_cost": 10400.00
  }'
```

### Örnek Yanıt

```json
{
  "status": "ok",
  "id": 31,
  "severity": "Kritik",
  "total": 31
}
```

---

## 📊 Demo Sonuçları

```
Toplam Tespit  : 30 hasar noktası
Kritik         : 15 (%50)
Orta           : 11 (%37)
Hafif          :  4 (%13)
─────────────────────────────────
Toplam Malzeme : 130.803,84 ₺
Toplam İşçilik :  78.482,29 ₺
Toplam Lojistik:  52.321,55 ₺
─────────────────────────────────
Tahmini Bütçe  : 261.607,68 ₺
```

---

## 👥 Ekip

| İsim | GitHub |
|------|--------|
| **Ömer Faruk Güneş** | [@omerfrksun](https://github.com/omerfrksun) |
| **Furkan İlbak** | — |
| **Ebubekir Erişgin** | — |

> iş'te Yapay Zeka Hackathonu — Esenler Belediyesi & Teknopark İstanbul

---

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

<div align="center">

**YolGözcü** — Akıllı Yol Takip Sistemi

*iş'te Yapay Zeka Hackathonu 2024*

</div>
