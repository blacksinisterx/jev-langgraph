"""Vercel Python entrypoint. Mounts the existing FastAPI app (unchanged,
routes defined without an /api prefix) under /api -- Starlette's Mount
strips the prefix before dispatching, so no route in backend/app/main.py
needs to change for this to work."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from fastapi import FastAPI  # noqa: E402
from app.main import app as backend_app  # noqa: E402

app = FastAPI()
app.mount("/api", backend_app)
