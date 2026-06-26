# Ascendrite Revision Layer: Normalization Layers

## 1. Batch Normalization Forward Pass

For input mini-batch $\mathcal{B} = \{\mathbf{x}_1, \dots, \mathbf{x}_B\}$, each element $\mathbf{x}_i \in \mathbb{R}^d$:
1.  **Batch Mean:**
    $$\mathbf{\mu}_{\mathcal{B}} = \frac{1}{B} \sum_{i=1}^B \mathbf{x}_i$$
2.  **Batch Variance:**
    $$\mathbf{\sigma}_{\mathcal{B}}^2 = \frac{1}{B} \sum_{i=1}^B (\mathbf{x}_i - \mathbf{\mu}_{\mathcal{B}})^2$$
3.  **Normalize:**
    $$\hat{\mathbf{x}}_i = \frac{\mathbf{x}_i - \mathbf{\mu}_{\mathcal{B}}}{\sqrt{\mathbf{\sigma}_{\mathcal{B}}^2 + \epsilon}}$$
4.  **Affine Scale & Shift:**
    $$\mathbf{y}_i = \mathbf{\gamma} \odot \hat{\mathbf{x}}_i + \mathbf{\beta}$$
    where $\mathbf{\gamma}, \mathbf{\beta} \in \mathbb{R}^d$ are learnable scaling and shifting parameter vectors.

---

## 2. Batch Normalization Backward Pass (Analytical Gradients)

Let $\mathbf{g}_i = \frac{\partial J}{\partial \mathbf{y}_i}$ be the incoming gradient. Gradients are computed element-wise:
*   **Scale Parameter Gradient:**
    $$\frac{\partial J}{\partial \mathbf{\gamma}} = \sum_{i=1}^B \mathbf{g}_i \odot \hat{\mathbf{x}}_i$$
*   **Shift Parameter Gradient:**
    $$\frac{\partial J}{\partial \mathbf{\beta}} = \sum_{i=1}^B \mathbf{g}_i$$
*   **Input Activation Gradient:**
    $$\frac{\partial J}{\partial \mathbf{x}_i} = \frac{\mathbf{\gamma}}{B \sqrt{\mathbf{\sigma}_{\mathcal{B}}^2 + \epsilon}} \odot \left( B \mathbf{g}_i - \sum_{j=1}^B \mathbf{g}_j - \hat{\mathbf{x}}_i \odot \sum_{j=1}^B \mathbf{g}_j \odot \hat{\mathbf{x}}_j \right)$$

---

## 3. Normalization Taxonomy Comparison

For a 4D tensor input of shape $(N, C, H, W)$:
*   **Batch Normalization:** Normalizes across the batch dimension ($N$) independently for each channel ($C$). Statistics shape: $(1, C, 1, 1)$. Dependent on batch size.
*   **Layer Normalization:** Normalizes across the channel ($C$) and spatial ($H, W$) dimensions independently for each sample ($N$). Statistics shape: $(N, 1, 1, 1)$. Independent of batch size; suited for Transformers/sequence inputs.
*   **Instance Normalization:** Normalizes across spatial ($H, W$) dimensions independently for each sample ($N$) and channel ($C$). Statistics shape: $(N, C, 1, 1)$. Used in image style transfer.
*   **Group Normalization:** Divides the $C$ channels into $G$ groups, and normalizes across the channels in each group and the spatial ($H, W$) dimensions. Statistics shape: $(N, G, 1, 1)$. Suited for small batch sizes in vision models.
