# Ascendrite Interview Prep: High-Performance Scaling

## Q1: Explain the differences between PyTorch DataParallel (DP) and DistributedDataParallel (DDP). Why is DDP preferred for multi-GPU training?

### Standard Answer
**1. Process vs. Thread Model:**
*   **DataParallel (DP)** is a single-process, multi-threaded architecture. All threads run under a single Python process, which suffers from the **GIL (Global Interpreter Lock)** bottleneck.
*   **DistributedDataParallel (DDP)** is a multi-process architecture. It spawns a completely independent Python process for each GPU, bypassing the GIL completely.

**2. Communication and Coordination:**
*   **DP** uses a single master GPU to coordinate updates. In every step, the master replicates weights to all other GPUs, scatters the input batch, collects output activations, calculates loss, and distributes gradients. The master GPU's PCI-e link becomes a severe bottleneck, leading to poor scaling.
*   **DDP** replicates the model across all GPUs at startup. During training, each process reads its own unique batch slice and computes the forward pass independently. During the backward pass, processes use **Ring AllReduce** to average gradients across all GPUs. Because each process updates its weights independently, there is no master bottleneck. DDP scales linearly.

---

## Q2: Walk through the steps of the Ring AllReduce algorithm. Prove that the total communication volume per GPU is independent of the number of GPUs.

### Standard Answer
Let $P$ be the number of GPUs connected in a logical ring network. Let $M$ be the total size of the gradient array (in number of parameters).
The gradient array is partitioned into $P$ equal chunks of size $\frac{M}{P}$.

**Step 1: Scatter-Reduce Phase ($P - 1$ steps):**
*   In step 1, each GPU $p$ sends its $p$-th chunk of size $\frac{M}{P}$ to its right neighbor, while receiving a chunk from its left neighbor. It adds the received chunk to its local chunk.
*   In step 2, each GPU sends the newly updated chunk.
*   This continues for $P - 1$ steps. At the end of this phase, each GPU holds the exact accumulated sum of exactly one chunk.
*   *Total data sent per GPU in this phase:* $(P - 1) \cdot \frac{M}{P}$.

**Step 2: AllGather Phase ($P - 1$ steps):**
*   The goal is to distribute the summed chunks to all other GPUs.
*   Each GPU sends the fully summed chunk it is responsible for to its right neighbor. Neighbors copy the chunk and forward it.
*   This continues for $P - 1$ steps. At the end, all GPUs hold the complete averaged gradient array of size $M$.
*   *Total data sent per GPU in this phase:* $(P - 1) \cdot \frac{M}{P}$.

**Proof of Communication Volume:**
Adding the volume from both phases:
$$\text{Volume}_{\text{total}} = 2(P - 1) \cdot \frac{M}{P} = 2 \frac{P - 1}{P} M$$

As the number of GPUs $P$ increases to infinity:
$$\lim_{P \to \infty} 2 \frac{P - 1}{P} M = 2M$$

This proves that the communication volume per GPU is bounded by $2M$, which is **independent of the number of GPUs $P$**. This allows the algorithm to scale efficiently to hundreds of nodes.

---

## Q3: How do Column-Parallel and Row-Parallel linear layers split computations in Tensor Parallelism?

### Standard Answer
Tensor Parallelism (Megatron-LM style) partitions individual layer weight matrices across multiple GPUs.

**1. Column-Parallel Linear Layer:**
*   **Partitioning:** The weight matrix $\mathbf{W} \in \mathbb{R}^{in \times out}$ is split vertically into columns across $K$ GPUs:
    $$\mathbf{W} = [\mathbf{W}_1, \mathbf{W}_2, \dots, \mathbf{W}_K]$$
*   **Computation:** Each GPU $i$ receives the complete input $\mathbf{X}$ and computes its output slice:
    $$\mathbf{Y}_i = \mathbf{X}\mathbf{W}_i$$
*   **Communication:** No communication is required during the matrix multiplication. The final output is concatenated along the column dimension:
    $$\mathbf{Y} = [\mathbf{Y}_1, \mathbf{Y}_2]$$

**2. Row-Parallel Linear Layer:**
*   **Partitioning:** The weight matrix $\mathbf{W}$ is split horizontally into rows across $K$ GPUs:
    $$\mathbf{W} = \begin{bmatrix} \mathbf{W}_1 \\ \mathbf{W}_2 \end{bmatrix}$$
*   **Computation:** The input $\mathbf{X}$ must be split along its column dimension to match the rows: $\mathbf{X} = [\mathbf{X}_1, \mathbf{X}_2]$. Each GPU $i$ computes:
    $$\mathbf{Y}_i = \mathbf{X}_i\mathbf{W}_i$$
*   **Communication:** The final output is the sum of these products:
    $$\mathbf{Y} = \mathbf{Y}_1 + \mathbf{Y}_2 = \mathbf{X}_1\mathbf{W}_1 + \mathbf{X}_2\mathbf{W}_2$$
    This requires an **AllReduce (Sum)** step across the $K$ GPUs to aggregate the final representation.
