import os
import glob
from typing import List, Tuple

import torch
from torch.utils.data import Dataset
import numpy as np


class BratsNumpyDataset(Dataset):
    """
    Expects .npz files with keys:
    - 'image': (C, D, H, W)
    - 'mask':  (C, D, H, W) or (1, D, H, W)
    """

    def __init__(self, file_paths: List[str]):
        self.file_paths = file_paths

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        path = self.file_paths[idx]
        data = np.load(path)
        image = data["image"]
        mask = data["mask"]
        return torch.from_numpy(image).float(), torch.from_numpy(mask).float()


def get_train_val_loaders(processed_dir, batch_size, val_split, num_workers, seed):
    npz_files = sorted(glob.glob(os.path.join(processed_dir, "*.npz")))
    assert len(npz_files) > 0, "No processed .npz files found."

    import numpy as np
    np.random.seed(seed)
    np.random.shuffle(npz_files)

    n_total = len(npz_files)
    n_val = int(n_total * val_split)
    val_files = npz_files[:n_val]
    train_files = npz_files[n_val:]

    train_ds = BratsNumpyDataset(train_files)
    val_ds = BratsNumpyDataset(val_files)

    from torch.utils.data import DataLoader
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True,
                              num_workers=num_workers, pin_memory=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False,
                            num_workers=num_workers, pin_memory=True)

    return train_loader, val_loader

