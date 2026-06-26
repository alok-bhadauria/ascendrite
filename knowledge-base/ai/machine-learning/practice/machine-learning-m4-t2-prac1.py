import numpy as np


def time_series_split(
    n_samples: int, n_splits: int
) -> list[tuple[np.ndarray, np.ndarray]]:
    """Generates train and validation indices for an expanding-window Time-Series split.

    Args:
        n_samples: Total number of observations in the dataset.
        n_splits: Number of walk-forward validation splits to perform.

    Returns:
        list of tuple: A list containing (train_indices, val_indices) for each split, where:
            - train_indices: np.ndarray containing indices from 0 up to split_boundary.
            - val_indices: np.ndarray containing indices from split_boundary to split_boundary + test_size.

    Note:
        - Let test_size = n_samples // (n_splits + 1).
        - For split i (from 0 to n_splits - 1):
          - The validation fold starts at index: (i + 1) * test_size
          - The validation fold ends at index: (i + 2) * test_size
          - The training fold contains all indices from 0 up to: (i + 1) * test_size
    """
    test_size = n_samples // (n_splits + 1)
    splits = []

    for i in range(n_splits):
        # Calculate split boundaries
        split_boundary = (i + 1) * test_size
        val_end = (i + 2) * test_size

        # Generate index arrays
        train_idx = np.arange(0, split_boundary)
        val_idx = np.arange(split_boundary, val_end)

        splits.append((train_idx, val_idx))

    return splits
