# Ascendrite Revision Layer: Scalable Data Wrangling with Pandas

## 1. Memory Optimization Cheat Sheet

To optimize memory utilization, downcast numeric columns and convert low-cardinality strings to categories.

### Integer Range References
*   `int8`: $[-128, 127]$ (1 byte)
*   `uint8`: $[0, 255]$ (1 byte)
*   `int16`: $[-32768, 32767]$ (2 bytes)
*   `uint16`: $[0, 65535]$ (2 bytes)
*   `int32`: $[-2^{31}, 2^{31}-1]$ (4 bytes)
*   `float32`: $\pm 3.4 \times 10^{38}$ (4 bytes)

### Object vs. Category Cast
*   **Object Type:** Array of pointers (8 bytes per pointer) to python heap strings (~50+ bytes overhead per entry).
*   **Category Type:** Maps unique values to integer keys (`int8`/`int16` depending on category vocabulary cardinality).
*   **Cardinality Constraint:** Only cast `object` to `category` when unique values ratio is under $50\%$:
    $$\frac{N_{\text{unique}}}{N_{\text{total}}} < 0.5$$

---

## 2. Chunking Formula (Out-of-Memory Aggregation)

To process massive files, read in chunks and accumulate values. 

### Running Mean Formulation
Do not average intermediate means. Instead, track the running sum and sample count:
$$\mu = \frac{\sum_{k=1}^K S_k}{\sum_{k=1}^K n_k}$$

where:
*   $S_k = \sum_{i=1}^{n_k} x_{k,i}$ is the sum of chunk $k$.
*   $n_k$ is the row count of chunk $k$.

---

## 3. High-Performance Columnar I/O

| Feature | CSV (Row-Text) | Parquet (Column-Binary) |
| :--- | :--- | :--- |
| **Storage Model** | Row-oriented | Column-oriented |
| **Data Types** | Needs parsing/inference | Preserved in metadata |
| **Query I/O** | Scans entire row | Selects specific columns |
| **Filter Pushdown** | Unsupported | Supported via statistics |
| **Compression** | Poor (text characters) | Superior (typed binary) |
