import torch


def dice_score(logits, targets, threshold=0.5, eps=1e-5):
    probs = torch.sigmoid(logits)
    preds = (probs > threshold).float()

    num = 2.0 * (preds * targets).sum(dim=(2, 3, 4))
    den = (preds + targets).sum(dim=(2, 3, 4)) + eps
    dice = (num / den).mean().item()
    return dice
