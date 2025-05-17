import importlib
import subprocess
import sys
import os

REQUIREMENTS_FILE = "requirements.txt"

def install_requirements():
    print(f"Installing packages from {REQUIREMENTS_FILE}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS_FILE])

def import_or_install(module_name):
    try:
        return importlib.import_module(module_name)
    except ImportError:
        print(f"Module '{module_name}' not found. Installing requirements...")
        install_requirements()
        # Try again after installation
        try:
            return importlib.import_module(module_name)
        except ImportError as e:
            print(f"Failed to import module '{module_name}' even after installation: {e}")
            sys.exit(1)

if __name__ == "__main__":
    # Example usage: list the required top-level modules here
    modules_needed = [
        "fastapi",
        "uvicorn",
        "anyio",
        "uvloop",
    ]

    for mod_name in modules_needed:
        import_or_install(mod_name)

    print("All required modules are installed.")

