import os
import tempfile
import glob
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import numpy as np
import torch

from src.config import Config
from models.unet3d import UNet3D
from utils.transforms import load_nii, resample_volume, normalize_intensity, center_crop_or_pad
from src.reconstruct_3d import mask_to_mesh, save_as_obj
from utils.io_utils import ensure_dir

app = Flask(__name__)
CORS(app)

cfg = Config()
device = torch.device(cfg.DEVICE if torch.cuda.is_available() else "cpu")

# Load model once at startup
CHECKPOINT_PATH = os.path.join(cfg.CHECKPOINT_DIR, "unet3d_best.pth")
model = UNet3D(in_channels=cfg.IN_CHANNELS, num_classes=cfg.NUM_CLASSES)
if os.path.exists(CHECKPOINT_PATH):
    ckpt = torch.load(CHECKPOINT_PATH, map_location=device)
    model.load_state_dict(ckpt["model_state"])
model.to(device)
model.eval()


def preprocess_api_case(case_dir):
    modalities = ["t1", "t1ce", "t2", "flair"]
    images = []
    spacing_ref = None
    for m in modalities:
        path = glob.glob(os.path.join(case_dir, f"*_{m}.nii*"))
        if len(path) != 1:
            raise ValueError(f"Expected one file for modality {m}, got {len(path)}.")
        vol, spacing = load_nii(path[0])
        spacing_ref = spacing if spacing_ref is None else spacing_ref
        vol = resample_volume(vol, spacing, cfg.TARGET_SPACING)
        vol = normalize_intensity(vol, cfg.INTENSITY_CLIP)
        images.append(vol)
    vol_stack = np.stack(images, axis=0)
    vol_stack = center_crop_or_pad(vol_stack, cfg.PATCH_SIZE)
    return vol_stack, spacing_ref


def run_model(image_vol):
    x = torch.from_numpy(image_vol[None]).float().to(device)
    with torch.no_grad():
        logits = model(x)
        probs = torch.sigmoid(logits)
        preds = (probs > 0.5).float().cpu().numpy()[0]
    return preds


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/predict", methods=["POST"])
def predict():
    """
    Expects multipart/form-data with four files:
    - t1, t1ce, t2, flair (NIfTI .nii or .nii.gz)
    Returns:
    - JSON with dice placeholder and URLs for mask .npy and mesh .obj.
    """
    if "t1" not in request.files:
        return jsonify({"error": "Upload four files named t1, t1ce, t2, flair"}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        # Save uploaded files with BraTS-like names
        for key in ["t1", "t1ce", "t2", "flair"]:
            f = request.files[key]
            if f.filename == "":
                return jsonify({"error": f"Empty filename for {key}"}), 400
            out_path = os.path.join(tmpdir, f"case_{key}.nii.gz")
            f.save(out_path)

        image_vol, spacing_ref = preprocess_api_case(tmpdir)
        preds = run_model(image_vol)
        wt_mask = preds[0] > 0.5

        # Save mask and 3D mesh
        ensure_dir(cfg.RESULTS_DIR)
        mask_path = os.path.join(cfg.RESULTS_DIR, "api_mask.npy")
        np.save(mask_path, preds)

        verts, faces = mask_to_mesh(wt_mask)
        mesh_path = os.path.join(cfg.RESULTS_DIR, "api_mesh.obj")
        save_as_obj(verts, faces, mesh_path)

    return jsonify({
        "mask_path": "/download/mask",
        "mesh_path": "/download/mesh",
        "dice_estimate": None
    })


@app.route("/download/mask", methods=["GET"])
def download_mask():
    path = os.path.join(cfg.RESULTS_DIR, "api_mask.npy")
    if not os.path.exists(path):
        return jsonify({"error": "Mask not found"}), 404
    return send_file(path, as_attachment=True, download_name="mask.npy")


@app.route("/download/mesh", methods=["GET"])
def download_mesh():
    path = os.path.join(cfg.RESULTS_DIR, "api_mesh.obj")
    if not os.path.exists(path):
        return jsonify({"error": "Mesh not found"}), 404
    return send_file(path, as_attachment=True, download_name="tumor.obj")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)

