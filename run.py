#!/usr/bin/env python
import os
import sys
import subprocess
from threading import Thread

# Ensure venv is activated by using the venv's Python explicitly
venv_dir = os.path.join(os.path.dirname(__file__), "venv")
venv_python = os.path.join(venv_dir, "Scripts", "python.exe")
venv_pip = os.path.join(venv_dir, "Scripts", "pip.exe")

# If running from global Python, re-run using venv Python
if sys.prefix != venv_dir:
    if os.path.exists(venv_python):
        os.execvp(venv_python, [venv_python, __file__])

def start_frontend():
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    if os.path.isdir(frontend_dir):
        try:
            # start frontend dev server (npm must be installed)
            subprocess.Popen(["npm", "run", "dev"], cwd=frontend_dir)
        except FileNotFoundError:
            print("npm not found - frontend dev server not started")

if __name__ == "__main__":
    Thread(target=start_frontend, daemon=True).start()
    # start uvicorn for the FastAPI app
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
