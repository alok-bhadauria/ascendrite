# Ascendrite Interview Prep: Normalization Layers

## Q1: Derive the backpropagation equations for Batch Normalization from first principles.

### Standard Answer
Let $J$ be the scalar loss. The outputs of the Batch Normalization layer are:
$$\mathbf{y}_i = \mathbf{\gamma} \odot \hat{\mathbf{x}}_i + \mathbf{\beta}$$
where $\hat{\mathbf{x}}_i = \frac{\mathbf{x}_i - \mathbf{\mu}}{\sqrt{\mathbf{\sigma}^2 + \epsilon}}$, with $\mathbf{\mu} = \frac{1}{B} \sum_{k=1}^B \mathbf{x}_k$ and $\mathbf{\sigma}^2 = \frac{1}{B} \sum_{k=1}^B (\mathbf{x}_k - \mathbf{\mu})^2$. 

Let $\mathbf{g}_i = \frac{\partial J}{\partial \mathbf{y}_i}$ be the incoming gradient. 
Using the chain rule, we compute the derivatives for each step of the forward computation:

**1. Gradients with respect to parameters:**
$$\frac{\partial J}{\partial \mathbf{\gamma}} = \sum_{i=1}^B \frac{\partial J}{\partial \mathbf{y}_i} \frac{\partial \mathbf{y}_i}{\partial \mathbf{\gamma}} = \sum_{i=1}^B \mathbf{g}_i \odot \hat{\mathbf{x}}_i$$
$$\frac{\partial J}{\partial \mathbf{\beta}} = \sum_{i=1}^B \frac{\partial J}{\partial \mathbf{y}_i} \frac{\partial \mathbf{y}_i}{\partial \mathbf{\beta}} = \sum_{i=1}^B \mathbf{g}_i$$

**2. Gradient with respect to normalized inputs $\hat{\mathbf{x}}_i$:**
$$\frac{\partial J}{\partial \hat{\mathbf{x}}_i} = \frac{\partial J}{\partial \mathbf{y}_i} \frac{\partial \mathbf{y}_i}{\partial \hat{\mathbf{x}}_i} = \mathbf{g}_i \odot \mathbf{\gamma}$$

**3. Gradient with respect to variance $\mathbf{\sigma}^2$:**
Since $\mathbf{\sigma}^2$ affects all $\hat{\mathbf{x}}_j$, we sum over the batch:
$$\frac{\partial J}{\partial \mathbf{\sigma}^2} = \sum_{j=1}^B \frac{\partial J}{\partial \hat{\mathbf{x}}_j} \odot \frac{\partial \hat{\mathbf{x}}_j}{\partial \mathbf{\sigma}^2} = \sum_{j=1}^B (\mathbf{g}_j \odot \mathbf{\gamma}) \odot \left( -\frac{1}{2}(\mathbf{x}_j - \mathbf{\mu}) \odot (\mathbf{\sigma}^2 + \epsilon)^{-3/2} \right)$$
$$\frac{\partial J}{\partial \mathbf{\sigma}^2} = -\frac{\mathbf{\gamma}}{2}(\mathbf{\sigma}^2 + \epsilon)^{-3/2} \odot \sum_{j=1}^B \mathbf{g}_j \odot (\mathbf{x}_j - \mathbf{\mu})$$

**4. Gradient with respect to mean $\mathbf{\mu}$:**
The mean affects the activations directly through the numerator of $\hat{\mathbf{x}}_j$ and indirectly through the variance $\mathbf{\sigma}^2$:
$$\frac{\partial J}{\partial \mathbf{\mu}} = \left( \sum_{j=1}^B \frac{\partial J}{\partial \hat{\mathbf{x}}_j} \odot \frac{\partial \hat{\mathbf{x}}_j}{\partial \mathbf{\mu}} \right) + \frac{\partial J}{\partial \mathbf{\sigma}^2} \odot \frac{\partial \mathbf{\sigma}^2}{\partial \mathbf{\mu}}$$
$$\frac{\partial J}{\partial \mathbf{\mu}} = \left( \sum_{j=1}^B (\mathbf{g}_j \odot \mathbf{\gamma}) \odot \left( -\frac{1}{\sqrt{\mathbf{\sigma}^2 + \epsilon}} \right) \right) + \frac{\partial J}{\partial \mathbf{\sigma}^2} \odot \left( \frac{1}{B} \sum_{j=1}^B -2(\mathbf{x}_j - \mathbf{\mu}) \right)$$
Since $\sum_{j=1}^B (\mathbf{x}_j - \mathbf{\mu}) = 0$, the second term becomes zero, leaving:
$$\frac{\partial J}{\partial \mathbf{\mu}} = -\frac{\mathbf{\gamma}}{\sqrt{\mathbf{\sigma}^2 + \epsilon}} \odot \sum_{j=1}^B \mathbf{g}_j$$

**5. Gradient with respect to inputs $\mathbf{x}_i$:**
The input $\mathbf{x}_i$ affects the loss directly via $\hat{\mathbf{x}}_i$, and indirectly via the computed mean $\mathbf{\mu}$ and variance $\mathbf{\sigma}^2$:
$$\frac{\partial J}{\partial \mathbf{x}_i} = \frac{\partial J}{\partial \hat{\mathbf{x}}_i} \odot \frac{\partial \hat{\mathbf{x}}_i}{\partial \mathbf{x}_i} + \frac{\partial J}{\partial \mathbf{\mu}} \odot \frac{\partial \mathbf{\mu}}{\partial \mathbf{x}_i} + \frac{\partial J}{\partial \mathbf{\sigma}^2} \odot \frac{\partial \mathbf{\sigma}^2}{\partial \mathbf{x}_i}$$
$$\frac{\partial J}{\partial \mathbf{x}_i} = (\mathbf{g}_i \odot \mathbf{\gamma}) \odot \frac{1}{\sqrt{\mathbf{\sigma}^2 + \epsilon}} + \frac{\partial J}{\partial \mathbf{\mu}} \odot \frac{1}{B} + \frac{\partial J}{\partial \mathbf{\sigma}^2} \odot \frac{2(\mathbf{x}_i - \mathbf{\mu})}{B}$$

Substituting the expressions for $\frac{\partial J}{\partial \mathbf{\mu}}$ and $\frac{\partial J}{\partial \mathbf{\sigma}^2}$ into the equation and simplifying terms:
$$\frac{\partial J}{\partial \mathbf{x}_i} = \frac{\mathbf{\gamma}}{B \sqrt{\mathbf{\sigma}^2 + \epsilon}} \odot \left( B \mathbf{g}_i - \sum_{j=1}^B \mathbf{g}_j - \hat{\mathbf{x}}_i \odot \sum_{j=1}^B \mathbf{g}_j \odot \hat{\mathbf{x}}_j \right)$$

---

## Q2: Why does Batch Normalization fail when training with very small batch sizes, and how do Layer and Group Normalization address this?

### Standard Answer
**1. BatchNorm Limitation under Small Batches:**
BatchNorm estimates population mean and variance using the statistics of the current mini-batch. When the batch size is very small (e.g. $B=2$), these estimates are highly noisy and have high variance. Consequently, the normalized activations fluctuate wildly, destabilizing training. During inference, the running average statistics accumulated from these noisy batch statistics will be highly inaccurate, causing a severe drop in model validation accuracy.

**2. Layer Normalization Solution:**
LayerNorm calculates statistics across all channel features and spatial coordinates of a *single* input sample:
$$\mu_i = \frac{1}{C \cdot H \cdot W} \sum_{c,h,w} X_{i,c,h,w}$$
Because the mean and variance are calculated independently for each sample, LayerNorm is completely independent of batch size. It performs identically regardless of whether the batch size is 1 or 1000.

**3. Group Normalization Solution:**
GroupNorm divides the channels $C$ of a sample into $G$ groups, and normalizes across the channels in each group and the spatial coordinates. This avoids the drawback of LayerNorm in convolutional vision models (where normalizing across all channels can wash out channel-specific feature boundaries) while retaining complete independence from the batch dimension. It allows stable training of large ResNet architectures on a single GPU with small batches.

---

## Q3: What is the purpose of the learnable affine parameters $\gamma$ and $\beta$ in normalization layers?

### Standard Answer
If we only normalized the activations, the output of the layer would be constrained to have a mean of 0 and variance of 1. 

Forcing this distribution can restrict the representation capacity of the network. For instance, if the subsequent layer uses a Sigmoid activation, constraining inputs to $\mathcal{N}(0, 1)$ forces the activations to stay within the linear regime near the origin ($[-1, 1]$), preventing the network from utilizing the non-linear saturation regions.

To resolve this, we introduce learnable parameters $\gamma$ (scale) and $\beta$ (shift). They perform the affine transformation:
$$y = \gamma \odot \hat{x} + \beta$$
*   They are initialized to $\gamma = \mathbf{1}$ and $\beta = \mathbf{0}$, meaning the layer starts as a standard normalized transformation.
*   During backpropagation, the network learns to adapt these parameters to scaling/shifting coordinates. If the optimal optimization state requires unnormalized activations, the network can learn to set $\gamma = \sqrt{\sigma^2 + \epsilon}$ and $\beta = \mu$, representing the mathematical identity mapping that restores the original unnormalized inputs.
