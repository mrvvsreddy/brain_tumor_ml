# Phase 1 — Data Audit (Summary)

## Goal
Understand the Brain Tumor MRI dataset before any preprocessing or model training.

---

## Environment
- 🐍 **Python 3.10**
- 🖥️ **Remote GPU server** (NVIDIA L4)
- 💻 **VS Code Remote**
- 🔍 Exploration only (no training)

---

## Dataset Overview
- Dataset downloaded from **Kaggle**
- Data kept unchanged during audit
- Dataset already split into `Training` and `Testing`
- ⚠️ Data is **slice-level** (not patient-level)

---

## Class Distribution

### Training
| Class | Count | Status |
|-------|-------|--------|
| `pituitary` | 1457 | |
| `glioma` | 1321 | |
| `meningioma` | 1339 | |
| `notumor` | **1595** | 🏆 **Dominant** |

### Testing
| Class | Count | Status |
|-------|-------|--------|
| `pituitary` | 300 | |
| `glioma` | 300 | |
| `meningioma` | 306 | |
| `notumor` | **405** | 🏆 **Dominant** |

> ⚠️ **Observation:** `notumor` is the dominant class, so **accuracy alone can be misleading**.

---

## Image Properties
- 🖼️ Image mode: `RGB` (MRI is inherently **grayscale**)
- 📐 Image sizes vary widely (**41+ unique sizes**)

> **Implications:**
> - ✅ Images **must be resized** before training
> - ⏳ Grayscale vs RGB will be decided later
> - 🔲 CNNs require **fixed-size inputs**

---

## ⚠️ Key Risk

> **🚨 CRITICAL: Memorization Risk**
> 
> - Slice-level MRI data contains **many similar images**
> - Train/test split may include slices from **the same patient**
> - This makes memorization easy and **evaluation unreliable**

---

## ✅ Outcome
Phase 1 completed with a clear understanding of:

| Area | Finding |
|------|---------|
| 📊 Class Imbalance | `notumor` is dominant |
| 📐 Image Variability | 41+ sizes, resizing required |
| 🎨 Grayscale Relevance | RGB contains duplicated grayscale |
| ⚠️ Memorization Risk | **HIGH** (slice-level data) |

**No preprocessing or training was performed.**

---

## 🚀 Next Step
Proceed to **Phase 2 — Preprocessing & Dataset Design**
