import os
import glob
import argparse
import numpy as np
from tqdm import tqdm

from config import Config
from utils.transforms import load_nii, resample_volume, normalize_intensity, center_crop_or_pad
from utils.io_utils import ensure_dir


"""
Preprocessing pipeline:

- Expects BraTS-like directory with cases, each containing:
  *_t1.nii.gz, *_t1ce.nii.gz, *_t2.nii.gz, *_flair.nii.gz, *_seg.nii.gz
- Loads modalities and segmentation.
- Resamples to target spacing.
- Normalizes each modality independently.
- Stacks into (C, D, H, W) and center-crops/pads.
- Saves .npz to data/processed.
BraTS data reference.[web:5][web:18]
"""


def find_cases(raw_dir):
    case_dirs = sorted([d for d in glob.glob(os.path.join(raw_dir, "*")) if os.path.isdir(d)])
    return case_dirs


def process_case(case_dir, cfg: Config):
    modalities = ["t1", "t1ce", "t2", "flair"]
    images = []
    spacing_ref = None

    for m in modalities:
        path = glob.glob(os.path.join(case_dir, f"*_{m}.nii*"))
        assert len(path) == 1, f"Missing modality {m} in {case_dir}"
        vol, spacing = load_nii(path[0])
        spacing_ref = spacing if spacing_ref is None else spacing_ref
        vol = resample_volume(vol, spacing, cfg.TARGET_SPACING)
        vol = normalize_intensity(vol, cfg.INTENSITY_CLIP)
        images.append(vol)

    image_vol = np.stack(images, axis=0)  # (C, D, H, W)

    seg_path = glob.glob(os.path.join(case_dir, "*_seg.nii*"))
    assert len(seg_path) == 1, f"Missing seg in {case_dir}"
    seg, seg_spacing = load_nii(seg_path[0])
    seg = resample_volume(seg, seg_spacing, cfg.TARGET_SPACING)

    # Convert multi-class labels to multi-channel binary (WT, TC, ET example)
    # BraTS uses labels {0, 1, 2, 4}[web:7][web:12]
    wt = (seg > 0).astype(np.float32)
    tc = np.isin(seg, [1, 4]).astype(np.float32)
    et = (seg == 4).astype(np.float32)
    mask_vol = np.stack([wt, tc, et], axis=0)

    image_vol = center_crop_or_pad(image_vol, cfg.PATCH_SIZE)
    mask_vol = center_crop_or_pad(mask_vol, cfg.PATCH_SIZE)

    return image_vol, mask_vol


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw_dir", type=str, default=Config.RAW_DIR)
    parser.add_argument("--out_dir", type=str, default=Config.PROCESSED_DIR)
    args = parser.parse_args()

    ensure_dir(args.out_dir)

    cfg = Config()
    case_dirs = find_cases(args.raw_dir)

    for case_dir in tqdm(case_dirs, desc="Preprocessing cases"):
        case_id = os.path.basename(case_dir)
        img, msk = process_case(case_dir, cfg)
        out_path = os.path.join(args.out_dir, f"{case_id}.npz")
        np.savez_compressed(out_path, image=img, mask=msk)

    print(f"Saved processed cases to {args.out_dir}")


if __name__ == "__main__":
    main()
