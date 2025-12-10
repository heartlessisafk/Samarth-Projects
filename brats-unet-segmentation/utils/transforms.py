import numpy as np
import torch
import SimpleITK as sitk
from scipy.ndimage import zoom


def load_nii(path: str):
    img = sitk.ReadImage(path)
    arr = sitk.GetArrayFromImage(img)  # (D, H, W)
    spacing = img.GetSpacing()[::-1]   # convert (x,y,z) → (z,y,x)
    return arr.astype(np.float32), np.array(spacing, dtype=np.float32)


def save_nii(volume: np.ndarray, ref_spacing, out_path: str):
    img = sitk.GetImageFromArray(volume.astype(np.float32))
    img.SetSpacing(tuple(ref_spacing[::-1]))
    sitk.WriteImage(img, out_path)


def resample_volume(volume: np.ndarray, original_spacing, target_spacing):
    zoom_factors = original_spacing / target_spacing
    return zoom(volume, zoom_factors, order=1)


def normalize_intensity(volume: np.ndarray, clip=(-1000, 4000)):
    v = np.clip(volume, clip[0], clip[1])
    mean = v.mean()
    std = v.std() + 1e-8
    return (v - mean) / std


def to_tensor(volume: np.ndarray):
    # Expect (C, D, H, W)
    return torch.from_numpy(volume).float()


def center_crop_or_pad(volume: np.ndarray, target_shape):
    # volume: (C, D, H, W)
    c, d, h, w = volume.shape
    td, th, tw = target_shape
    out = np.zeros((c, td, th, tw), dtype=volume.dtype)
    sd = max((td - d) // 2, 0)
    sh = max((th - h) // 2, 0)
    sw = max((tw - w) // 2, 0)

    d_start = max((d - td) // 2, 0)
    h_start = max((h - th) // 2, 0)
    w_start = max((w - tw) // 2, 0)

    d_end = d_start + min(td, d)
    h_end = h_start + min(th, h)
    w_end = w_start + min(tw, w)

    out[:, sd:sd + (d_end - d_start),
        sh:sh + (h_end - h_start),
        sw:sw + (w_end - w_start)] = volume[:, d_start:d_end,
                                            h_start:h_end,
                                            w_start:w_end]
    return out
