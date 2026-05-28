from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, List
import os

app = FastAPI(
    title="YolGozcü API",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fotoğrafları statik dosya olarak sun (driver.html'den erişim için)
if os.path.exists("yol1.jpeg"):
    app.mount("/photos", StaticFiles(directory="."), name="photos")

# Sadece canlı tespitler — her sunucu başlangıcında BOŞ
DB_DEFECTS: List[Dict[str, Any]] = []

@app.on_event("startup")
async def startup_clear():
    """Sunucu her basladiginda eski kayitlari temizle."""
    DB_DEFECTS.clear()
    print("YolGözcü başlatıldı — hasar kayıtları temizlendi.")


@app.get("/")
async def root():
    return {"status": "YolGozcü aktif", "detections": len(DB_DEFECTS)}


@app.get("/api/defects", response_model=Dict[str, Any])
async def get_defects():
    """Canlı hasar tespitlerini GeoJSON olarak döner. Başlangıçta boş."""
    return {"type": "FeatureCollection", "features": DB_DEFECTS}


@app.get("/api/report", response_model=Dict[str, Any])
async def get_report():
    """Mali özet raporu."""
    total_defects   = len(DB_DEFECTS)
    critical_count  = sum(1 for f in DB_DEFECTS if f["properties"]["severity"] == "Kritik")
    total_material  = sum(f["properties"]["material_cost"]  for f in DB_DEFECTS)
    total_labor     = sum(f["properties"]["labor_cost"]     for f in DB_DEFECTS)
    total_logistic  = sum(f["properties"]["logistic_cost"]  for f in DB_DEFECTS)
    total_projected = sum(f["properties"]["total_cost"]     for f in DB_DEFECTS)

    return {
        "total_defects":        total_defects,
        "critical_count":       critical_count,
        "total_material_cost":  round(total_material,  2),
        "total_labor_cost":     round(total_labor,     2),
        "total_logistic_cost":  round(total_logistic,  2),
        "total_projected_cost": round(total_projected, 2),
    }


class DetectionPayload(BaseModel):
    lat:           float
    lon:           float
    address:       str
    damage_type:   str
    width_cm:      float
    depth_cm:      float
    material_cost: float
    labor_cost:    float
    logistic_cost: float
    total_cost:    float
    severity:      str
    photo:         str = ""   # hangi fotoğraf tetikledi


@app.post("/api/detect")
async def add_detection(payload: DetectionPayload):
    """Driver'dan gelen canlı tespiti haritaya ekler."""
    feature = {
        "type": "Feature",
        "id":   len(DB_DEFECTS) + 1,
        "geometry": {
            "type":        "Point",
            "coordinates": [payload.lon, payload.lat]
        },
        "properties": {
            "location_zone": payload.address.split(",")[-1].strip() if "," in payload.address else "Istanbul",
            "address":       payload.address,
            "damage_type":   payload.damage_type,
            "width_cm":      payload.width_cm,
            "depth_cm":      payload.depth_cm,
            "material_cost": payload.material_cost,
            "labor_cost":    payload.labor_cost,
            "logistic_cost": payload.logistic_cost,
            "total_cost":    payload.total_cost,
            "severity":      payload.severity,
            "photo":         payload.photo,
        }
    }
    DB_DEFECTS.append(feature)
    return {"status": "ok", "id": feature["id"], "severity": payload.severity, "total": len(DB_DEFECTS)}


@app.delete("/api/detections")
async def clear_detections():
    """Tüm tespitleri sıfırla — demo yeniden başlatma için."""
    DB_DEFECTS.clear()
    return {"status": "cleared"}