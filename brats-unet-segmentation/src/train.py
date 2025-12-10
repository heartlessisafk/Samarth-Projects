import os
import argparse
import torch
import torch.optim as optim
from torch.cuda.amp import GradScaler, autocast
from tqdm import tqdm

from config import Config
from models.unet3d import UNet3D
from utils.dataset import get_train_val_loaders
from utils.losses import BCEDiceLoss
from utils.metrics import dice_score
from utils.io_utils import ensure_dir, save_checkpoint


def train_epoch(model, loader, optimizer, criterion, device, scaler=None):
    model.train()
    running_loss = 0.0
    running_dice = 0.0

    for images, masks in tqdm(loader, desc="Train", leave=False):
        images = images.to(device)
        masks = masks.to(device)

        optimizer.zero_grad()

        if scaler is not None:
            with autocast():
                logits = model(images)
                loss = criterion(logits, masks)
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            logits = model(images)
            loss = criterion(logits, masks)
            loss.backward()
            optimizer.step()

        running_loss += loss.item() * images.size(0)
        running_dice += dice_score(logits.detach(), masks.detach()) * images.size(0)

    n = len(loader.dataset)
    return running_loss / n, running_dice / n


def eval_epoch(model, loader, criterion, device):
    model.eval()
    running_loss = 0.0
    running_dice = 0.0

    with torch.no_grad():
        for images, masks in tqdm(loader, desc="Val", leave=False):
            images = images.to(device)
            masks = masks.to(device)
            logits = model(images)
            loss = criterion(logits, masks)

            running_loss += loss.item() * images.size(0)
            running_dice += dice_score(logits, masks) * images.size(0)

    n = len(loader.dataset)
    return running_loss / n, running_dice / n


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=Config.NUM_EPOCHS)
    parser.add_argument("--batch_size", type=int, default=Config.BATCH_SIZE)
    parser.add_argument("--lr", type=float, default=Config.LR)
    parser.add_argument("--checkpoint_dir", type=str, default=Config.CHECKPOINT_DIR)
    parser.add_argument("--use_amp", action="store_true")
    args = parser.parse_args()

    cfg = Config()
    device = torch.device(cfg.DEVICE if torch.cuda.is_available() else "cpu")

    ensure_dir(args.checkpoint_dir)

    train_loader, val_loader = get_train_val_loaders(
        cfg.PROCESSED_DIR,
        batch_size=args.batch_size,
        val_split=cfg.VALIDATION_SPLIT,
        num_workers=cfg.NUM_WORKERS,
        seed=cfg.RANDOM_SEED,
    )

    model = UNet3D(in_channels=cfg.IN_CHANNELS, num_classes=cfg.NUM_CLASSES).to(device)
    optimizer = optim.AdamW(model.parameters(), lr=args.lr, weight_decay=cfg.WEIGHT_DECAY)
    criterion = BCEDiceLoss()
    scaler = GradScaler() if args.use_amp and device.type == "cuda" else None

    best_val_dice = 0.0

    for epoch in range(1, args.epochs + 1):
        print(f"\nEpoch {epoch}/{args.epochs}")

        train_loss, train_dice = train_epoch(model, train_loader, optimizer, criterion, device, scaler)
        val_loss, val_dice = eval_epoch(model, val_loader, criterion, device)

        print(f"Train Loss: {train_loss:.4f} | Train Dice: {train_dice:.4f}")
        print(f"Val   Loss: {val_loss:.4f} | Val   Dice: {val_dice:.4f}")

        if val_dice > best_val_dice:
            best_val_dice = val_dice
            ckpt_path = os.path.join(args.checkpoint_dir, f"unet3d_best.pth")
            save_checkpoint(
                {
                    "epoch": epoch,
                    "model_state": model.state_dict(),
                    "optimizer_state": optimizer.state_dict(),
                    "val_dice": val_dice,
                },
                ckpt_path,
            )
            print(f"Saved new best checkpoint to {ckpt_path}")


if __name__ == "__main__":
    main()

