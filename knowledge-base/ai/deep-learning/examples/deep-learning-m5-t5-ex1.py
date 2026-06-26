import numpy as np


def simulate_ring_allreduce(P: int, M: int, initial_data: list[np.ndarray]) -> list[np.ndarray]:
    """Simulates the Ring AllReduce algorithm across P virtual GPUs.

    Args:
        P: Number of GPUs (processes)
        M: Size of the data array. Must be divisible by P.
        initial_data: List of length P containing NumPy arrays of shape (M,)

    Returns:
        list: Final averaged arrays of shape (M,) for each GPU
    """
    assert M % P == 0, "Data size M must be divisible by number of GPUs P!"
    chunk_size = M // P

    # Make copies to work with locally
    gpus_data = [data.copy().astype(float) for data in initial_data]

    # 1. Scatter-Reduce Phase (P - 1 steps)
    # The goal is to accumulate sums. At the end, GPU p holds the summed chunk (p + 1) % P
    for step in range(P - 1):
        # Prepare transfers to avoid in-place read corruption during the step
        transfers = []
        for p in range(P):
            # Calculate chunk index to send
            send_chunk_idx = (p - step) % P
            send_val = gpus_data[p][send_chunk_idx * chunk_size : (send_chunk_idx + 1) * chunk_size]
            receiver = (p + 1) % P
            transfers.append((receiver, send_chunk_idx, send_val))

        # Apply transfers
        for receiver, chunk_idx, val in transfers:
            gpus_data[receiver][chunk_idx * chunk_size : (chunk_idx + 1) * chunk_size] += val

    # 2. AllGather Phase (P - 1 steps)
    # The goal is to distribute the fully summed chunks around the ring
    for step in range(P - 1):
        transfers = []
        for p in range(P):
            # The chunk index that is fully summed at GPU p is (p + 1) % P
            # At step s, we forward this summed chunk around the ring
            send_chunk_idx = (p + 1 - step) % P
            send_val = gpus_data[p][send_chunk_idx * chunk_size : (send_chunk_idx + 1) * chunk_size]
            receiver = (p + 1) % P
            transfers.append((receiver, send_chunk_idx, send_val))

        # Apply transfers (overwrite, since it's already fully summed)
        for receiver, chunk_idx, val in transfers:
            gpus_data[receiver][chunk_idx * chunk_size : (chunk_idx + 1) * chunk_size] = val

    # 3. Average the gradients (divide by P)
    for p in range(P):
        gpus_data[p] /= P

    return gpus_data


if __name__ == "__main__":
    print("--- Running Ring AllReduce Simulation ---")

    # 4 virtual GPUs, data size M=8 (chunk size = 2)
    P = 4
    M = 8

    # Initialize each GPU with unique gradients
    # GPU 0: [0, 1, 2, 3, 4, 5, 6, 7]
    # GPU 1: [10, 11, 12, 13, 14, 15, 16, 17]
    # ...
    initial_data = [
        np.arange(M, dtype=float) + (p * 10) for p in range(P)
    ]

    print("Initial Data per GPU:")
    for p in range(P):
        print(f"  GPU {p}: {initial_data[p]}")

    # Expected sum array:
    # Sum = GPU 0 + GPU 1 + GPU 2 + GPU 3
    #     = [0+10+20+30, 1+11+21+31, ...] = [60, 64, 68, 72, 76, 80, 84, 88]
    # Expected average = [15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0]
    expected_avg = np.mean(initial_data, axis=0)
    print("\nExpected Averaged Array:\n ", expected_avg)

    # Run Simulation
    final_data = simulate_ring_allreduce(P, M, initial_data)

    print("\nFinal Data per GPU after Ring AllReduce:")
    for p in range(P):
        print(f"  GPU {p}: {final_data[p]}")
        # Assert each GPU matches the exact averaged representation
        assert np.allclose(final_data[p], expected_avg)

    print("\n  [PASS] Ring AllReduce simulation successfully completed and verified.")
