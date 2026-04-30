# Carotis-AI — Developer convenience targets
# Usage: make <target>
#
# Windows users: use "nmake /F Makefile" or install make via choco / scoop
# or just run the commands directly (they are plain docker / pip calls).

.PHONY: init up down logs test demo demo-model clean help

help:
	@echo ""
	@echo "Carotis-AI development commands:"
	@echo "  make init         — create data directories + copy .env.example"
	@echo "  make demo-model   — generate demo ONNX model (no GPU needed)"
	@echo "  make demo         — full one-shot demo: model + build + start + health"
	@echo "  make up           — build and start all containers"
	@echo "  make down         — stop all containers"
	@echo "  make logs         — tail container logs"
	@echo "  make test         — run smoke tests (no Docker required)"
	@echo "  make clean        — remove containers, images, and volumes"
	@echo ""

init:
	@echo "Creating data directories..."
	mkdir -p data/models data/db data/dicom_temp
	@if [ ! -f backend/.env ]; then cp backend/.env.example backend/.env && echo "Copied .env.example -> .env (edit API_KEY!)"; fi

demo-model:
	@echo "Generating demo ONNX model..."
	@PYTHON=backend/.venv/bin/python; \
	  [ -x "$$PYTHON" ] || PYTHON=python3; \
	  $$PYTHON scripts/generate_demo_model.py

demo: init demo-model
	@echo "Starting Carotis-AI..."
	docker compose up --build -d
	@echo "Waiting for backend health..."
	@for i in $$(seq 1 40); do \
	  curl -sf http://localhost:8000/health > /dev/null 2>&1 && break; \
	  echo "  . ($$i/40)"; sleep 3; \
	done
	@echo ""
	@echo "  Frontend  ->  http://localhost:3000"
	@echo "  API docs  ->  http://localhost:8000/docs"
	@echo "  Health    ->  http://localhost:8000/health"
	@echo ""

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

test:
	@echo "Running smoke tests..."
	@PYTHONPATH=backend python -m pytest tests/test_smoke.py -v 2>/dev/null || \
	  (cd backend && pip install -q -r requirements.txt && cd .. && PYTHONPATH=backend python -m pytest tests/test_smoke.py -v)

clean:
	docker compose down --rmi local --volumes
