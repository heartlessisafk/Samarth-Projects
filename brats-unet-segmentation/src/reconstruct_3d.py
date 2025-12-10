import os
import argparse
import numpy as np
from skimage import measure
from tqdm import tqdm


"""
3D reconstruction:

- Loads prediction mask .npy (C, D, H, W).
- Selects whole tumor channel (0).
- Uses marching cubes to extract surface mesh.[web:11][web:14]
- Saves as .obj and .stl.
"""


def mask_to_mesh(mask, level=0.5):
    verts, faces, normals, values = measure.marching_cubes(
        mask.astype(float), level=level, spacing=(1.0, 1.0, 1.0)
    )
    return verts, faces


def save_as_obj(verts, faces, path):
    with open(path, "w") as f:
        for v in verts:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for face in faces:
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")


def save_as_stl(verts, faces, path):
    with open(path, "w") as f:
        f.write("solid tumor\n")
        for face in faces:
            v1, v2, v3 = verts[face[0]], verts[face[1]], verts[face[2]]
            f.write(" facet normal 0 0 0\n")
            f.write("  outer loop\n")
            f.write(f"   vertex {v1[0]} {v1[1]} {v1[2]}\n")
            f.write(f"   vertex {v2[0]} {v2[1]} {v2[2]}\n")
            f.write(f"   vertex {v3[0]} {v3[1]} {v3[2]}\n")
            f.write("  endloop\n")
            f.write(" endfacet\n")
        f.write("endsolid tumor\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mask_path", type=str, required=True, help="Predicted mask .npy")
    parser.add_argument("--out_dir", type=str, required=True)
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    mask = np.load(args.mask_path)  # (C, D, H, W)
    wt_mask = mask[0] > 0.5

    verts, faces = mask_to_mesh(wt_mask)
    base = os.path.splitext(os.path.basename(args.mask_path))[0]

    obj_path = os.path.join(args.out_dir, f"{base}.obj")
    stl_path = os.path.join(args.out_dir, f"{base}.stl")

    save_as_obj(verts, faces, obj_path)
    save_as_stl(verts, faces, stl_path)

    print(f"Saved 3D meshes: {obj_path}, {stl_path}")


if __name__ == "__main__":
    main()
