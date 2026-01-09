"""
Setup script for Brain Tumor ML project.
Creates virtual environment, installs dependencies, and downloads Kaggle dataset.
"""

import os
import sys
import subprocess
import platform

# ---------------------------
# CONFIG
# ---------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENV_DIR = os.path.join(PROJECT_ROOT, "venv")
REQUIREMENTS_FILE = os.path.join(PROJECT_ROOT, "requirements.txt")
DATA_RAW = os.path.join(PROJECT_ROOT, "data", "raw")
DATASET = "masoudnickparvar/brain-tumor-mri-dataset"
KAGGLE_JSON_SOURCE = os.path.join(PROJECT_ROOT, "kaggle.json")
KAGGLE_DIR = os.path.join(os.path.expanduser("~"), ".kaggle")

# Determine platform-specific paths
IS_WINDOWS = platform.system() == "Windows"
PYTHON_EXECUTABLE = os.path.join(VENV_DIR, "Scripts" if IS_WINDOWS else "bin", "python")
PIP_EXECUTABLE = os.path.join(VENV_DIR, "Scripts" if IS_WINDOWS else "bin", "pip")


def run_command(cmd, description, check=True):
    """Run a command and print status."""
    print(f"\n{'='*50}")
    print(f"📌 {description}")
    print(f"{'='*50}")
    print(f"Running: {' '.join(cmd)}\n")
    result = subprocess.run(cmd, check=check)
    return result.returncode == 0


def main():
    print("\n🧠 Brain Tumor ML - Project Setup")
    print("=" * 50)

    # ---------------------------
    # STEP 1: Create Virtual Environment
    # ---------------------------
    if not os.path.exists(VENV_DIR):
        run_command(
            [sys.executable, "-m", "venv", VENV_DIR],
            "Creating virtual environment..."
        )
        print("✓ Virtual environment created")
    else:
        print("✓ Virtual environment already exists")

    # ---------------------------
    # STEP 2: Upgrade pip
    # ---------------------------
    run_command(
        [PYTHON_EXECUTABLE, "-m", "pip", "install", "--upgrade", "pip"],
        "Upgrading pip..."
    )
    print("✓ pip upgraded")

    # ---------------------------
    # STEP 3: Install Requirements
    # ---------------------------
    if os.path.exists(REQUIREMENTS_FILE):
        run_command(
            [PIP_EXECUTABLE, "install", "-r", REQUIREMENTS_FILE],
            "Installing requirements..."
        )
        print("✓ Requirements installed")
    else:
        print("⚠ requirements.txt not found, skipping...")

    # ---------------------------
    # STEP 4: Create Data Directories
    # ---------------------------
    os.makedirs(DATA_RAW, exist_ok=True)
    print("✓ Data directories created")

    # ---------------------------
    # STEP 5: Setup Kaggle Credentials
    # ---------------------------
    kaggle_executable = os.path.join(VENV_DIR, "Scripts" if IS_WINDOWS else "bin", "kaggle")
    kaggle_json_dest = os.path.join(KAGGLE_DIR, "kaggle.json")
    
    if os.path.exists(KAGGLE_JSON_SOURCE):
        # Create .kaggle directory if it doesn't exist
        os.makedirs(KAGGLE_DIR, exist_ok=True)
        
        # Copy kaggle.json to ~/.kaggle/
        import shutil
        shutil.copy2(KAGGLE_JSON_SOURCE, kaggle_json_dest)
        
        # Set proper permissions (required on Linux/Mac)
        if not IS_WINDOWS:
            os.chmod(kaggle_json_dest, 0o600)
        
        print("✓ Kaggle credentials copied to ~/.kaggle/")
    else:
        if not os.path.exists(kaggle_json_dest):
            print("⚠ kaggle.json not found in project root!")
            print("  Please add kaggle.json to the project folder")
            sys.exit(1)
        else:
            print("✓ Kaggle credentials already exist")

    # ---------------------------
    # STEP 6: Download Kaggle Dataset
    # ---------------------------
    # Check if data already exists
    if os.path.exists(DATA_RAW) and os.listdir(DATA_RAW):
        print("✓ Dataset already exists, skipping download")
    else:
        run_command(
            [kaggle_executable, "datasets", "download",
             "-d", DATASET,
             "-p", DATA_RAW,
             "--unzip"],
            "Downloading Kaggle dataset..."
        )
        print("✓ Dataset downloaded and extracted")

    # ---------------------------
    # FINAL SUMMARY
    # ---------------------------
    print("\n" + "=" * 50)
    print("🎉 SETUP COMPLETE!")
    print("=" * 50)
    print(f"\nTo activate the virtual environment:")
    if IS_WINDOWS:
        print(f"  .\\venv\\Scripts\\activate")
    else:
        print(f"  source venv/bin/activate")
    print(f"\nThen run:")
    print(f"  python phase1_data_setup.py")
    print()


if __name__ == "__main__":
    main()
