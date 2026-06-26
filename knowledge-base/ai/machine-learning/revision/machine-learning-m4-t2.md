# Ascendrite Revision Layer: Advanced Cross-Validation Protocols

## 1. Nested Cross-Validation (Double Loop)

Avoids **selection bias** by decoupling hyperparameter optimization (inner loop) from generalization performance evaluation (outer loop).

*   **Outer Loop ($K_{\text{outer}}$ folds):**
    *   Estimates generalization performance.
    *   For fold $k$, hold out $k$-th block as outer test set. Train optimal model on the rest.
*   **Inner Loop ($K_{\text{inner}}$ folds):**
    *   Executes hyperparameter search (grid/random search).
    *   Runs on the active outer training set.
    *   Selects parameters $\theta^*$ that maximize validation score.
*   *Computational Complexity:* $\text{Total Runs} = K_{\text{outer}} \times (P \times K_{\text{inner}} + 1)$, where $P$ is the number of tuning configurations.

---

## 2. Stratified Group K-Fold

Used when data contains multiple correlated samples from the same entity (e.g. patients, users).
*   **Group K-Fold constraint:** Guarantees that all observations from a specific group are allocated strictly to the same fold. Prevents group-level target leakage.
*   **Stratification constraint:** Partition groups such that the target label distribution in each fold matches the global class distribution as closely as possible.
*   *Validation Diagnostic:* If validation score drops significantly when moving from random K-Fold to Group K-Fold, the model is overfitting to entity identifiers rather than learning generalizable patterns.

---

## 3. Time-Series Splits & Temporal Causality

For autocorrelated, ordered time-series. Standard random K-Fold causes **future-lookahead leakage** (interpolating validation targets from adjacent training observations).

### Windows
*   **Expanding Window (Cumulative):**
    *   Train fold $k$ on $\{t_1, \dots, t_{k}\}$
    *   Validate fold $k$ on $\{t_{k+1}, \dots, t_{k+h}\}$
    *   Training size increases at each step.
*   **Sliding Window:**
    *   Train fold $k$ on a fixed past window $\{t_{k-W}, \dots, t_k\}$
    *   Validate fold $k$ on $\{t_{k+1}, \dots, t_{k+h}\}$
    *   Preferred for non-stationary distributions to discard stale data.
