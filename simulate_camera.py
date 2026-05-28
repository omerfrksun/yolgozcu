"""
YolGözcü - Canlı Kamera Simülatörü
Gerçek kamera olmadan demo için: her 4 saniyede bir yeni hasar tespiti simüle eder.
Kullanım: python simulate_camera.py
"""
import requests
import random
import time
import math

API_URL = "http://127.0.0.1:8000"

# İstanbul'da gerçekçi araç güzergahı (Kadıköy → Üsküdar → Beşiktaş)
ROUTE = [
    {"lat": 40.9901, "lon": 29.0234, "street": "Moda Caddesi, Kadıköy"},
    {"lat": 40.9950, "lon": 29.0200, "street": "Bağdat Caddesi, Kadıköy"},
    {"lat": 41.0000, "lon": 29.0180, "street": "Üsküdar Sahil Yolu"},
    {"lat": 41.0100, "lon": 29.0160, "street": "Çengelköy Caddesi"},
    {"lat": 41.0150, "lon": 29.0152, "street": "Hakimiyeti Milliye Cad., Üsküdar"},
    {"lat": 41.0200, "lon": 29.0130, "street": "Kandilli Caddesi"},
    {"lat": 41.0250, "lon": 29.0100, "street": "Boğaziçi Köprüsü Yaklaşımı"},
    {"lat": 41.0300, "lon": 29.0074, "street": "Barbaros Bulvarı, Beşiktaş"},
    {"lat": 41.0350, "lon": 29.0050, "street": "Çırağan Caddesi, Beşiktaş"},
    {"lat": 41.0400, "lon": 29.0020, "street": "Dolmabahçe Caddesi"},
    {"lat": 41.0422, "lon": 28.9980, "street": "Beşiktaş Merkez"},
]

DAMAGE_TYPES = ["çukur", "çatlak"]
SEVERITIES   = ["Kritik", "Orta", "Hafif", "Orta", "Hafif"]  # ağırlıklı dağılım

def post_detection(lat, lon, address, severity=None):
    damage_type = random.choice(DAMAGE_TYPES)
    sev = severity or random.choice(SEVERITIES)

    if sev == "Kritik":
        material = round(random.uniform(4000, 9000), 2)
        width_cm = round(random.uniform(70, 130), 1)
        depth_cm = round(random.uniform(12, 22), 1)
    elif sev == "Orta":
        material = round(random.uniform(1500, 4000), 2)
        width_cm = round(random.uniform(35, 70), 1)
        depth_cm = round(random.uniform(5, 12), 1)
    else:
        material = round(random.uniform(400, 1500), 2)
        width_cm = round(random.uniform(5, 35), 1)
        depth_cm = round(random.uniform(1, 5), 1)

    labor    = round(material * 0.60, 2)
    logistic = round(material * 0.40, 2)
    total    = round(material + labor + logistic, 2)

    payload = {
        "lat":          lat + random.uniform(-0.001, 0.001),
        "lon":          lon + random.uniform(-0.001, 0.001),
        "address":      address,
        "damage_type":  damage_type,
        "width_cm":     width_cm,
        "depth_cm":     depth_cm,
        "material_cost": material,
        "labor_cost":   labor,
        "logistic_cost": logistic,
        "total_cost":   total,
        "severity":     sev,
    }

    try:
        r = requests.post(f"{API_URL}/api/detect", json=payload, timeout=3)
        if r.status_code == 200:
            print(f"  ✓ [{sev:6}] {damage_type:6} | {address[:35]:35} | {total:>8.0f} TL")
        else:
            print(f"  ✗ HTTP {r.status_code}: {r.text[:60]}")
    except Exception as e:
        print(f"  ✗ Bağlantı hatası: {e}")

def run():
    print("=" * 65)
    print("  YolGözcü Kamera Simülatörü — Başlatılıyor")
    print("=" * 65)
    print(f"  API: {API_URL}")
    print(f"  Güzergah: {len(ROUTE)} durak | Her 4 saniyede 1 tespit")
    print(f"  Durdurmak için: Ctrl+C")
    print("-" * 65)

    detection_count = 0
    route_idx = 0

    while True:
        point = ROUTE[route_idx % len(ROUTE)]
        route_idx += 1

        # Her 5 tespitte bir Kritik çıkar — demo dramatizmi
        if detection_count % 5 == 4:
            forced_sev = "Kritik"
        elif detection_count % 3 == 1:
            forced_sev = "Orta"
        else:
            forced_sev = "Hafif"

        print(f"\n[{detection_count+1:03d}] Kamera karesi işleniyor → {point['street']}")
        post_detection(point["lat"], point["lon"], point["street"], forced_sev)
        detection_count += 1

        time.sleep(4)

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\n\nSimülatör durduruldu.")