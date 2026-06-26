import numpy as np


def split_column_parallel(W: np.ndarray, num_gpus: int) -> list[np.ndarray]:
    """Splits a weight matrix column-wise across virtual GPUs.

    Args:
        W: Weight matrix of shape (in_features, out_features)
        num_gpus: Number of partition splits

    Returns:
        list[np.ndarray]: List of split weight tensors
    """
    in_features, out_features = W.shape
    assert out_features % num_gpus == 0, "out_features must be divisible by num_gpus!"
    chunk_size = out_features // num_gpus

    splits = []
    for i in range(num_gpus):
        # Slice columns: W[:, i * chunk_size : (i + 1) * chunk_size]
        w_slice = W[:, i * chunk_size : (i + 1) * chunk_size]
        splits.append(w_slice)

    return splits


if __name__ == "__main__":
    print("--- Running Column-Parallel Tensor Splitting Practice ---")

    # Weight matrix W of shape (in=3, out=6), split across 2 GPUs
    W = np.array(
        [[1, 2, 3, 4, 5, 6],
         [7, 8, 9, 10, 11, 12],
         [13, 14, 15, 16, 17, 18]]
    )

    splits = split_column_parallel(W, num_gpus=2)
    print("GPU 0 split:\n", splits[0])
    print("GPU 1 split:\n", splits[1])

    # GPU 0 should receive columns 0, 1, 2
    expected_0 = np.array(
        [[1, 2, 3],
         [7, 8, 9],
         [13, 14, 15]]
    )
    assert np.allclose(splits[0], expected_0)

    # GPU 1 should receive columns 3, 4, 5
    expected_1 = np.array(
        [[4, 5, 6],
         [10, 11, 12],
         [16, 17, 18]]
    )
    assert np.allclose(splits[1], expected_1)

    print("\n  [PASS] Column-parallel tensor splitting verified successfully.")
