import os
import subprocess
from collections import Counter
from PIL import Image
import numpy as np

# ---------------------------
# CONFIG
# ---------------------------
PROJECT = "."
DATA_RAW = f"{PROJECT}/data/raw"
DATASET = "masoudnickparvar/brain-tumor-mri-dataset"

# ---------------------------
# STEP 1: CREATE STRUCTURE
# ---------------------------
os.makedirs(f"{DATA_RAW}", exist_ok=True)
os.makedirs(f"{PROJECT}/notebooks", exist_ok=True)
os.makedirs(f"{PROJECT}/scripts", exist_ok=True)

print("✓ Project structure ready")

# ---------------------------
# STEP 2: INSTALL KAGGLE
# ---------------------------
print("Installing kaggle...")
subprocess.run(["pip", "install", "-q", "kaggle"], check=True)

# ---------------------------
# STEP 3: DOWNLOAD DATASET
# ---------------------------
if not os.listdir(DATA_RAW):
    print("Downloading dataset...")
    subprocess.run([
        "kaggle", "datasets", "download",
        "-d", DATASET,
        "-p", DATA_RAW,
        "--unzip"
    ], check=True)
else:
    print("Dataset already exists, skipping download")

# ---------------------------
# STEP 4: LOCATE DATA
# ---------------------------
base = os.listdir(DATA_RAW)[0]
BASE_PATH = os.path.join(DATA_RAW, base)

TRAIN = os.path.join(BASE_PATH, "Training")
TEST = os.path.join(BASE_PATH, "Testing")

# ---------------------------
# STEP 5: CLASS COUNTS
# ---------------------------
def count_classes(path):
    counts = {}
    for cls in os.listdir(path):
        cls_path = os.path.join(path, cls)
        counts[cls] = len([
            f for f in os.listdir(cls_path)
            if f.lower().endswith((".jpg", ".png", ".jpeg"))
        ])
    return counts

train_counts = count_classes(TRAIN)
test_counts = count_classes(TEST)

print("\nTraining class counts:")
for k, v in train_counts.items():
    print(f"{k:10s}: {v}")

print("\nTesting class counts:")
for k, v in test_counts.items():
    print(f"{k:10s}: {v}")

# ---------------------------
# STEP 6: IMAGE SIZE CHECK
# ---------------------------
sizes = []
sampled_img = None

for cls in os.listdir(TRAIN):
    cls_path = os.path.join(TRAIN, cls)
    for img_name in os.listdir(cls_path)[:25]:
        img_path = os.path.join(cls_path, img_name)
        with Image.open(img_path) as img:
            sizes.append(img.size)
            sampled_img = img
    break

sizes = np.array(sizes)

print(f"\nUnique image sizes (sample): {len(np.unique(sizes, axis=0))}")
print("Example sizes:", np.unique(sizes, axis=0)[:5])

# ---------------------------
# STEP 7: IMAGE MODE
# ---------------------------
print("\nImage mode:", sampled_img.mode)

# ---------------------------
# FINAL CONCLUSIONS
# ---------------------------
dominant = max(train_counts, key=train_counts.get)

print("\n--- PHASE 1 SUMMARY ---")
print("Dominant class       :", dominant)
print("Resizing required    : YES (variable image sizes)")
print("Grayscale relevance  : YES (MRI data, RGB is duplicated)")
print("Memorization risk    : HIGH (slice-level data)")
print("Training started     : NO")
print("-----------------------")
