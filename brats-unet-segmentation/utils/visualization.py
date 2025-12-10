import os
import numpy as np
import matplotlib.pyplot as plt


def overlay_mask(image_slice, mask_slice, alpha=0.4):
    # image_slice: 2D
    # mask_slice:  2D (binary or multi-label)
    img = (image_slice - image_slice.min()) / (image_slice.ptp() + 1e-8)
    mask = mask_slice.astype(bool)

    rgb = np.stack([img, img, img], axis=-1)
    color = np.zeros_like(rgb)
    color[..., 0] = 1.0  # red overlay
    rgb[mask] = (1 - alpha) * rgb[mask] + alpha * color[mask]
    return rgb


def save_overlay_grid(volume, mask, out_path, n_slices=16):
    d = volume.shape[0]
    indices = np.linspace(0, d - 1, n_slices, dtype=int)

    cols = 4
    rows = int(np.ceil(n_slices / cols))

    fig, axes = plt.subplots(rows, cols, figsize=(12, 3 * rows))
    axes = axes.flatten()

    for ax, idx in zip(axes, indices):
        overlay = overlay_mask(volume[idx], mask[idx])
        ax.imshow(overlay)
        ax.set_title(f"Slice {idx}")
        ax.axis("off")

    for ax in axes[len(indices):]:
        ax.axis("off")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close(fig)
