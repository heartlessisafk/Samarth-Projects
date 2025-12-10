import torch
import torch.nn as nn
import torch.nn.functional as F


class DoubleConv(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv3d(in_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm3d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv3d(out_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm3d(out_channels),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.block(x)


class UNet3D(nn.Module):
    def __init__(self, in_channels=4, num_classes=1, base_filters=32):
        super().__init__()

        self.inc = DoubleConv(in_channels, base_filters)

        self.down1 = nn.Sequential(
            nn.MaxPool3d(2),
            DoubleConv(base_filters, base_filters * 2)
        )
        self.down2 = nn.Sequential(
            nn.MaxPool3d(2),
            DoubleConv(base_filters * 2, base_filters * 4)
        )
        self.down3 = nn.Sequential(
            nn.MaxPool3d(2),
            DoubleConv(base_filters * 4, base_filters * 8)
        )

        self.bottom = DoubleConv(base_filters * 8, base_filters * 16)

        self.up3 = nn.ConvTranspose3d(base_filters * 16, base_filters * 8, kernel_size=2, stride=2)
        self.conv3 = DoubleConv(base_filters * 16, base_filters * 8)

        self.up2 = nn.ConvTranspose3d(base_filters * 8, base_filters * 4, kernel_size=2, stride=2)
        self.conv2 = DoubleConv(base_filters * 8, base_filters * 4)

        self.up1 = nn.ConvTranspose3d(base_filters * 4, base_filters * 2, kernel_size=2, stride=2)
        self.conv1 = DoubleConv(base_filters * 4, base_filters * 2)

        self.outc = nn.Conv3d(base_filters * 2, num_classes, kernel_size=1)

    def forward(self, x):
        x1 = self.inc(x)
        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)

        xb = self.bottom(x4)

        xu3 = self.up3(xb)
        x = torch.cat([xu3, x4], dim=1)
        x = self.conv3(x)

        xu2 = self.up2(x)
        x = torch.cat([xu2, x3], dim=1)
        x = self.conv2(x)

        xu1 = self.up1(x)
        x = torch.cat([xu1, x2], dim=1)
        x = self.conv1(x)

        logits = self.outc(x)
        return logits
