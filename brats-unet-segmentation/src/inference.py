import os
import argparse
import numpy as np
import torch

from config import Config
from models.unet3d import UNet3D
from utils.transforms import load_nii, resample_volume, normalize_intensity, center_crop_or_pad
from utils.visualization import save_overlay_grid
from utils.io_utils import ensure_dir, load_checkpoint


def load_model(checkpoint_path, device, in_channels, num_classes):
    model = UNet3D(in_channels=in_channels, num_classes=num_classes)
    ckpt = load_checkpoint(checkpoint_path, map_location=device)
    model.load_state_dict(ckpt["model_state"])
    model.to(device)
    model.eval()
    return model


def preprocess_single_case(modality_paths, seg_spacing=None, cfg: Config = Config()):
    images = []
    spacing_ref = None
    for p in modality_paths:
        vol, spacing = load_nii(p)
        spacing_ref = spacing if spacing_ref is None else spacing_ref
        vol = resample_volume(vol, spacing, cfg.TARGET_SPACING)
        vol = normalize_intensity(vol, cfg.INTENSITY_CLIP)
        images.append(vol)

    image_vol = np.stack(images, axis=0)
    image_vol = center_crop_or_pad(image_vol, cfg.PATCH_SIZE)
    return image_vol, spacing_ref


def run_inference(model, image_vol, device, threshold=0.5):
    with torch.no_grad():
        x = torch.from_numpy(image_vol[None]).float().to(device)
        logits = model(x)
        probs = torch.sigmoid(logits)
        preds = (probs > threshold).float()
    return preds.cpu().numpy()[0]  # (C, D, H, W)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case_dir", type=str, required=True)
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--out_dir", type=str, default=os.path.join(Config.RESULTS_DIR, "inference"))
    args = parser.parse_args()

    cfg = Config()
    device = torch.device(cfg.DEVICE if torch.cuda.is_available() else "cpu")
    ensure_dir(args.out_dir)

    import glob
    modalities = ["t1", "t1ce", "t2", "flair"]
    modality_paths = []
    for m in modalities:
        p = glob.glob(os.path.join(args.case_dir, f"*_{m}.nii*"))
        assert len(p) == 1, f"Missing modality {m}"
        modality_paths.append(p[0])

    image_vol, spacing_ref = preprocess_single_case(modality_paths, cfg=cfg)

    model = load_model(args.checkpoint, device, in_channels=cfg.IN_CHANNELS, num_classes=cfg.NUM_CLASSES)
    pred_mask = run_inference(model, image_vol, device)

    # For visualization, use first channel as whole tumor
    wt_pred = pred_mask[0]
    d, h, w = wt_pred.shape
    case_id = os.path.basename(args.case_dir.rstrip("/"))
    overlay_path = os.path.join(args.out_dir, f"{case_id}_overlay.png")
    save_overlay_grid(image_vol[0], wt_pred, overlay_path)  # use one modality as background

    # Save raw mask
    np.save(os.path.join(args.out_dir, f"{case_id}_mask.npy"), pred_mask)
    print(f"Saved overlay to {overlay_path} and mask .npy to {args.out_dir}")


if __name__ == "__main__":
    main()
