# Ascendrite Interview Prep: Transfer Learning

## Q1: How do you choose between Feature Extraction and Fine-Tuning when applying transfer learning? Explain using the quadrant of dataset size vs. domain similarity.

### Standard Answer
The decision to use feature extraction or fine-tuning depends on the size of the target dataset and its similarity to the source pre-training dataset. This can be conceptualized as a quadrant:

```
                  Domain Similarity
                  High                Low
             +-------------------+-------------------+
        High |  Quadrant 1       |  Quadrant 2       |
             |  Fine-Tuning      |  Fine-Tuning      |
             |  (or Feature Ext) |  (Full network)   |
Dataset Size +-------------------+-------------------+
         Low |  Quadrant 3       |  Quadrant 4       |
             |  Feature Ext      |  Tricky / Partial |
             |  (Freeze backbone)|  (Feature Ext +)  |
             +-------------------+-------------------+
```

**1. High Similarity, Large Dataset (Quadrant 1):**
Fine-tuning is highly effective here. Since the dataset is large, we can optimize the weights without overfitting, and the high similarity ensures that we start from a strong initialization.

**2. Low Similarity, Large Dataset (Quadrant 2):**
Since the dataset is large and the domain is different, we should apply **Full Fine-Tuning**. The pre-trained weights still provide a better starting point than random initialization, but we need to update all layers to adapt to the new domain.

**3. High Similarity, Small Dataset (Quadrant 3):**
We should apply **Feature Extraction** (freeze the backbone). The small dataset increases the risk of overfitting, but because the domain similarity is high, the pre-trained features are already relevant.

**4. Low Similarity, Small Dataset (Quadrant 4):**
This is the most challenging quadrant. Since the dataset is small, fine-tuning the entire network will cause overfitting. Since the similarity is low, the features are not relevant. The best approach is to freeze the early backbone layers (which capture general shapes like edges) and fine-tune only the higher layers and head, or use alternative data augmentation strategies.

---

## Q2: Why is it critical to set Batch Normalization layers to evaluation mode (`model.eval()`) when freezing a backbone for fine-tuning?

### Standard Answer
During training, a Batch Normalization (BN) layer calculates the mean and variance of the current mini-batch to normalize activations, and updates its running statistics (mean and variance) using an exponential moving average.

If you freeze a convolutional backbone but leave the BN layers in training mode:
1.  **Running Statistics Distortion:** The fine-tuning target dataset is often small. If the BN layers continue to calculate mini-batch statistics, small or unrepresentative batches will distort the pre-trained running statistics.
2.  **Feature Representation Drift:** When the running statistics drift, the scale and shift of the features change. This distorts the activations passed to subsequent frozen layers, degrading performance.
3.  **Evaluation Mode Solution:** By setting the BN layers to evaluation mode (using `model.eval()`), the BN layers freeze their running statistics and use the pre-trained mean and variance. This preserves the scale and alignment of features throughout the frozen backbone.

---

## Q3: What is Catastrophic Forgetting, and what training protocols prevent it during fine-tuning?

### Standard Answer
**Catastrophic Forgetting** occurs when a pre-trained network is trained on a new task, and the gradient updates from the new task disrupt the weights of the pre-trained backbone, causing it to lose its pre-trained knowledge.

To prevent catastrophic forgetting, we use three main protocols:

**1. Differential Learning Rates (Learning Rate Scaling):**
We apply different learning rates to the backbone and the new classification head:
$$\eta_{\text{backbone}} \approx 0.1 \times \eta_{\text{head}}$$
This ensures that the pre-trained weights are updated with small increments, preventing large gradients from disrupting the features.

**2. Two-Stage Training Protocol:**
*   **Stage 1:** Freeze the backbone entirely and train only the new classification head. This allows the head to learn task-specific mappings without changing the backbone.
*   **Stage 2:** Unfreeze the backbone and fine-tune the entire network with a small learning rate.

**3. Gradual Unfreezing:**
Instead of unfreezing the entire backbone at once, we unfreeze layers incrementally, starting from the highest convolutional layers (which are task-specific) down to the lower layers (which are general).
