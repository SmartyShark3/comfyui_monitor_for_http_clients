import os
import sys
import subprocess
import importlib.util

def is_installed(package_name):
    """Check if a python package is installed."""
    try:
        # Special check for packages with different import names
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False

def install_requirements():
    """Installs dependencies if they are missing."""
    requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    
    # Check if psutil is already present before running pip
    if not is_installed("psutil"):
        print("[ComfyUI Monitor] psutil dependency is missing. Installing...")
        try:
            # Run pip using the executable running ComfyUI
            subprocess.check_call([
                sys.executable, 
                "-m", 
                "pip", 
                "install", 
                "-r", 
                requirements_file
            ])
            print("[ComfyUI Monitor] Dependencies installed successfully.")
        except Exception as e:
            print(f"[ComfyUI Monitor] Error installing dependencies: {e}")
            print("[ComfyUI Monitor] Please install psutil manually (e.g. pip install psutil)")
    else:
        # Already satisfied
        pass

if __name__ == "__main__":
    install_requirements()
