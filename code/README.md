# Carotis-AI — Developer Quick-Start

## Voraussetzungen
- Docker Desktop ≥ 4.30
- Python 3.11 (für lokale Entwicklung ohne Docker)
- Node.js 22 (für Frontend-Entwicklung)

---

## Mit Docker (empfohlen)

```bash
# 1. Env-Datei anlegen
cp code/backend/.env.example code/backend/.env
# API_KEY setzen (mindestens 32 Zeichen)

# 2. Stack starten
docker compose -f code/docker-compose.yml up --build

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# API-Docs: http://localhost:8000/docs  (nur im dev-Modus)
```

---

## Ohne Docker — Backend

```bash
cd code/backend
python -m venv .venv && .venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env   # API_KEY anpassen
uvicorn app.main:create_app --factory --reload --port 8000
```

---

## Ohne Docker — Frontend

```bash
cd code/frontend
npm install
# .env.local anlegen:
echo "VITE_API_URL=http://localhost:8000" > .env.local
echo "VITE_API_KEY=<dein-api-key>" >> .env.local
npm run dev
```

---

## ML-Pipeline

```bash
cd code
# Training (benötigt GPU-VM oder lokale GPU)
python -m ml.training.train \
  --data-root /path/to/data \
  --epochs 100 \
  --checkpoint-dir /path/to/checkpoints

# ONNX-Export nach Training
python -m ml.inference.onnx_export \
  --checkpoint /path/to/checkpoints/best.pt \
  --output /models/mfsd_unet.onnx
```

---

## Smoke-Tests

```bash
cd code
pip install pytest pytest-asyncio httpx
pytest tests/test_smoke.py -v
```

---

## Wichtige Hinweise

- ❌ **Niemals echte Patientendaten** in Git, Cloud, E-Mail oder externe APIs
- ❌ **Niemals** ONNX-Inferenz auf einem Cloud-Server ausführen
- ✅ Alle DICOM-Dateien werden vor der Verarbeitung in-memory anonymisiert
- ✅ SQLite-Audit-Trail speichert nur Hashes + numerische Werte
