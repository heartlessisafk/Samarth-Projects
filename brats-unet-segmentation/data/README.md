# Data Folder

This project uses the **BraTS** brain tumor segmentation dataset.[web:5][web:18]

## Steps

1. Register and download the latest BraTS training dataset from the official CBICA/BraTS website.[web:5]
2. Extract the archives into `data/raw/`, preserving folder names per subject (e.g., `BraTS20_Training_001`).
3. Each subject directory should contain:
   - `*_t1.nii.gz`
   - `*_t1ce.nii.gz`
   - `*_t2.nii.gz`
   - `*_flair.nii.gz`
   - `*_seg.nii.gz` (ground-truth labels)
4. Run:

