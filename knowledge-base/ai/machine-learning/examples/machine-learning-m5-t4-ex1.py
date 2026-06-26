import math
import numpy as np


def compute_exact_shapley(
    num_players: int, characteristic_fn: dict[tuple[int, ...], float]
) -> np.ndarray:
    """Computes exact Shapley values for a cooperative game with a given characteristic function.

    Args:
        num_players: The total number of players (features).
        characteristic_fn: A dictionary mapping subsets (represented as sorted tuples of
          player indices) to their payouts (float). Empty set is represented by ().

    Returns:
        np.ndarray: Computed Shapley values of shape (num_players,).
    """
    shapley_values = np.zeros(num_players)
    players = set(range(num_players))

    # Helper function to get the payout of a subset
    def get_v(subset: set[int]) -> float:
        key = tuple(sorted(subset))
        return characteristic_fn.get(key, 0.0)

    # Compute Shapley value for each player
    for i in range(num_players):
        remaining_players = players - {i}
        # Iterate over all possible subsets of remaining players
        # We can represent subsets using binary masks from 0 to 2^(M-1) - 1
        rem_list = list(remaining_players)
        num_subsets = 1 << len(rem_list)

        for mask in range(num_subsets):
            # Construct subset S
            S = {rem_list[j] for j in range(len(rem_list)) if (mask & (1 << j))}

            len_S = len(S)
            # Calculate weight: |S|! * (|F| - |S| - 1)! / |F|!
            weight = (
                math.factorial(len_S)
                * math.factorial(num_players - len_S - 1)
                / math.factorial(num_players)
            )

            # Marginal contribution
            marginal_contribution = get_v(S | {i}) - get_v(S)

            shapley_values[i] += weight * marginal_contribution

    return shapley_values


def verify_axioms(
    num_players: int,
    characteristic_fn: dict[tuple[int, ...], float],
    shapley_values: np.ndarray,
) -> None:
    """Verifies that the computed Shapley values satisfy the four core axioms."""
    print("--- Verifying Game Theory Axioms ---")

    # 1. Efficiency Axiom
    total_attribution = np.sum(shapley_values)
    v_empty = characteristic_fn.get((), 0.0)
    v_full = characteristic_fn.get(tuple(range(num_players)), 0.0)
    expected_diff = v_full - v_empty
    print(f"Efficiency: Sum of attributions = {total_attribution:.4f}")
    print(f"            Expected (v(F) - v(empty)) = {expected_diff:.4f}")
    assert np.allclose(total_attribution, expected_diff), "Efficiency axiom violated!"
    print("  [PASS] Efficiency Axiom")

    # 2. Symmetry Axiom
    # Find symmetric players if any
    for i in range(num_players):
        for j in range(i + 1, num_players):
            is_symmetric = True
            other_players = set(range(num_players)) - {i, j}
            rem_list = list(other_players)
            num_subsets = 1 << len(rem_list)

            for mask in range(num_subsets):
                S = {
                    rem_list[k]
                    for k in range(len(rem_list))
                    if (mask & (1 << k))
                }
                v_S_i = characteristic_fn.get(tuple(sorted(S | {i})), 0.0)
                v_S_j = characteristic_fn.get(tuple(sorted(S | {j})), 0.0)
                if not np.allclose(v_S_i, v_S_j):
                    is_symmetric = False
                    break

            if is_symmetric:
                print(f"Symmetric Players Identified: {i} and {j}")
                print(f"  phi_{i} = {shapley_values[i]:.4f}, phi_{j} = {shapley_values[j]:.4f}")
                assert np.allclose(
                    shapley_values[i], shapley_values[j]
                ), f"Symmetry axiom violated for players {i} and {j}!"
                print("  [PASS] Symmetry Axiom")

    # 3. Dummy Axiom
    for i in range(num_players):
        is_dummy = True
        other_players = set(range(num_players)) - {i}
        rem_list = list(other_players)
        num_subsets = 1 << len(rem_list)

        for mask in range(num_subsets):
            S = {rem_list[k] for k in range(len(rem_list)) if (mask & (1 << k))}
            v_S_i = characteristic_fn.get(tuple(sorted(S | {i})), 0.0)
            v_S = characteristic_fn.get(tuple(sorted(S)), 0.0)
            if not np.allclose(v_S_i, v_S):
                is_dummy = False
                break

        if is_dummy:
            print(f"Dummy Player Identified: {i}")
            print(f"  phi_{i} = {shapley_values[i]:.4f}")
            assert np.allclose(
                shapley_values[i], 0.0
            ), f"Dummy axiom violated for player {i}!"
            print("  [PASS] Dummy Axiom")

    print("All axioms verified successfully.")


if __name__ == "__main__":
    # Define a 3-player cooperative game
    # Let Player 0 be a highly influential player
    # Let Player 1 and Player 2 be symmetric players
    # Let Player 3 be a dummy player (adding him to any subset changes nothing)
    # Total Players = 4
    num_players = 4

    characteristic_fn = {
        (): 0.0,
        # Single players
        (0,): 20.0,
        (1,): 10.0,
        (2,): 10.0,
        (3,): 0.0,
        # Two players
        (0, 1): 40.0,
        (0, 2): 40.0,
        (0, 3): 20.0,
        (1, 2): 25.0,
        (1, 3): 10.0,
        (2, 3): 10.0,
        # Three players
        (0, 1, 2): 70.0,
        (0, 1, 3): 40.0,
        (0, 2, 3): 40.0,
        (1, 2, 3): 25.0,
        # Four players
        (0, 1, 2, 3): 70.0,
    }

    print("Computing exact Shapley values for a 4-player cooperative game:")
    phi = compute_exact_shapley(num_players, characteristic_fn)

    for idx, val in enumerate(phi):
        print(f"Player {idx} Attribution (Shapley Value): {val:.4f}")

    verify_axioms(num_players, characteristic_fn, phi)
