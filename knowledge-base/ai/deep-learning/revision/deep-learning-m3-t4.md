# Ascendrite Revision Card: Transfer Learning

## Paradigms: Feature Extraction vs. Fine-Tuning

*   **Feature Extraction:** The pre-trained network's weights $\mathbf{W}_{\text{backbone}}$ are frozen. A custom classification head $\mathbf{W}_{\text{head}}$ is added and trained from scratch. 
    *   *Best for:* Small datasets that are highly similar to the pre-training dataset.
*   **Fine-Tuning:** The custom head is trained, and the pre-trained weights are also updated. We can update all weights (Full Fine-Tuning) or only a subset of higher layers (Partial Fine-Tuning).
    *   *Best for:* Large datasets, or small datasets that are different from the pre-training domain.

## Layer Freezing Mechanics

*   **Gradient Masking:** Setting weight update updates to zero:
    $$\frac{\partial J}{\partial \mathbf{W}_l} = \mathbf{0}$$
*   **Computational Savings:** Frameworks block gradient calculations on frozen layers (using `requires_grad = False`). This reduces backpropagation memory requirements.
*   **Batch Normalization Gotcha:** BN layers should be kept in evaluation mode (`model.eval()`) during fine-tuning. This prevents target dataset mini-batches from distorting the pre-trained running statistics (mean and variance).

## Custom Head Adaptation & Learning Rates

*   **Catastrophic Forgetting:** The rapid loss of pre-trained knowledge in the backbone when exposed to large gradient updates from an untrained head.
*   **Differential Learning Rates:** Enforcing different learning rates to preserve backbone features:
    $$\eta_{\text{backbone}} \approx 0.1 \times \eta_{\text{head}}$$
*   **Two-Stage Protocol:**
    1.  **Stage 1:** Freeze backbone and train the custom head with a standard learning rate (e.g. $\eta = 10^{-3}$) until convergence.
    2.  **Stage 2:** Unfreeze the backbone (or higher layers) and fine-tune the entire network with a small learning rate (e.g. $\eta = 10^{-5}$).
