# Ascendrite Revision Card: High-Performance Scaling

## Distributed Data Parallel (DDP)

*   **Process Structure:** Spawns a separate Python process per GPU, avoiding DP's single-process GIL and master GPU bottlenecks.
*   **Workflow:** Replicates the model across all GPUs. Each GPU processes a unique data slice. Gradients are averaged via AllReduce during backpropagation, keeping models identical.
*   *Note:* DDP replicates the *entire model* on every GPU.

## Ring AllReduce Communication

*   **Algorithm Steps:** Connects $P$ GPUs in a logical ring. Splits the gradient array of size $M$ into $P$ chunks.
    1.  *Scatter-Reduce Phase ($P-1$ steps):* Each GPU sends a chunk and receives a chunk, summing it. At the end, each GPU has the correct averaged total for exactly one chunk.
    2.  *AllGather Phase ($P-1$ steps):* Sends the fully summed chunks around the ring so all GPUs have the full averaged array.
*   **Bandwidth Efficiency:** Total data sent per GPU is:
    $$\text{Volume} = 2 \frac{P - 1}{P} M$$
    As $P \to \infty$, the communication volume per GPU is bounded by $2M$, which is independent of the number of GPUs $P$, enabling linear scaling.

## Model Parallelism

*   **Tensor Parallelism (Intra-layer):** Splits weight matrices across GPUs. Column-parallel linear splits vertically: $\mathbf{W} = [\mathbf{W}_1, \mathbf{W}_2]$, multiplying inputs independently. Row-parallel splits horizontally, combining outputs via AllReduce.
*   **Pipeline Parallelism (Inter-layer):** Splits layers sequentially across GPUs. Splits mini-batches into micro-batches to pipeline execution, reducing idle GPU time (pipeline bubbles).
