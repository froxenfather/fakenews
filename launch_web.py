import subprocess
from pathlib import Path

# generate root for anyone who downloads this
ROOT = Path(__file__).resolve().parent

# Relative project folders
BACKEND_DIR = ROOT / "webapp" / "backend"
FRONTEND_DIR = ROOT / "webapp" / "frontend"

# backend boomska
backend_cmd = (
    f'start "Fake News Backend" cmd /k '
    f'"cd /d "{BACKEND_DIR}" && pip install -r requirements.txt && python -m uvicorn api:app --reload"'
)

# front end fella
frontend_cmd = (
    f'start "Fake News Frontend" cmd /k '
    f'"cd /d "{FRONTEND_DIR}" && npm.cmd install && npm.cmd run dev"'
)

# Launch both terminals
subprocess.Popen(backend_cmd, shell=True)
subprocess.Popen(frontend_cmd, shell=True)