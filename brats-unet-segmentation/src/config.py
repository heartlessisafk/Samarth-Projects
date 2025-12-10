import os

class Config:
    # Paths
    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    RAW_DIR = os.path.join(DATA_DIR, "raw")
    PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
    RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
    CHECKPOINT_DIR = os.path.join(RESULTS_DIR, "checkpoints")

    # Preprocessing
    TARGET_SPACING = (1.0, 1.0, 1.0)  # mm
    PATCH_SIZE = (128, 128, 128)
    INTENSITY_CLIP = (-1000, 4000)

    # Training
    NUM_EPOCHS = 150
    BATCH_SIZE = 2
    NUM_WORKERS = 4
    LR = 1e-4
    WEIGHT_DECAY = 1e-5
    VALIDATION_SPLIT = 0.2
    RANDOM_SEED = 42
    NUM_CLASSES = 4  # e.g., WT, TC, ET; adapt as needed
    IN_CHANNELS = 4  # BraTS modalities: T1, T1ce, T2, FLAIR

    # Hardware
    DEVICE = "cuda"
    