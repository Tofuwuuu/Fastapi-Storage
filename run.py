#!/usr/bin/env python
"""
Run both FastAPI backend and React frontend together.
"""
import os
import sys
import subprocess
from threading import Thread

# Ensure venv is activated by using the venv's Python explicitly
venv_dir = os.path.join(os.path.dirname(__file__), "venv")
venv_python = os.path.join(venv_dir, "Scripts", "python.exe")

# If running from global Python, re-run using venv Python
if sys.prefix != venv_dir:
    if os.path.exists(venv_python):
        os.execvp(venv_python, [venv_python, __file__])

def start_frontend():
    """Start React frontend dev server using npm"""
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    if os.path.isdir(frontend_dir):
        try:
            # Use shell=True so npm is found in system PATH
            subprocess.Popen("npm run dev", cwd=frontend_dir, shell=True)
            print("✓ Frontend dev server started on http://localhost:5173")
        except Exception as e:
            print(f"✗ Failed to start frontend: {e}")
    else:
        print("✗ frontend directory not found")

if __name__ == "__main__":
    print("=" * 60)
    print("Starting File Storage System")
    print("=" * 60)
    
    # Start frontend in background thread
    Thread(target=start_frontend, daemon=True).start()
    
    # Start backend (blocking)
    import uvicorn
    print("✓ Backend starting on http://127.0.0.1:8000")
    print("\nAccess the app at: http://localhost:5173")
    print("API docs at: http://localhost:8000/docs")
    print("\nPress CTRL+C to stop\n")
    
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
