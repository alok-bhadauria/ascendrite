# Ascendrite Interview Prep: Scalable Data Wrangling with Pandas

## Q1: How do you calculate the mean of a 100 GB numerical column on a machine with only 4 GB of RAM?

### Standard Answer
To compute the mean without loading the entire dataset into memory, we use chunked processing. Rather than loading the file all at once, we instantiate a generator reader using `pd.read_csv(..., chunksize=N)`. During iteration, we accumulate the sum of the elements and the total number of observations. Finally, we compute the ratio of the accumulated sum to the accumulated count.

### Mathematical Formulation
$$\mu = \frac{\sum_{k=1}^K S_k}{\sum_{k=1}^K n_k}$$

where $S_k$ is the sum of chunk $k$ and $n_k$ is the count of valid observations in chunk $k$.

---

## Q2: Why does slicing a DataFrame using `df[0:10]` sometimes lead to unintended memory usage or data corruption?

### Standard Answer
Slicing in Pandas returns a shallow copy or a **view** of the parent DataFrame's data buffer. This has two major consequences:
1.  **Shared Memory Modification:** Modifying the slice using assignment operators will mutate the original parent DataFrame, leading to silent bugs.
2.  **Memory Leakage:** The garbage collector cannot deallocate the parent DataFrame's memory buffer as long as the sliced view remains active in memory. If you slice a 10 row subset from a 10 GB DataFrame and keep only the slice, the entire 10 GB memory block is leaked.

### Interview Trap
Interviewers will ask how to resolve this. The correct answer is to explicitly call `.copy()` on the slice to allocate a fresh, independent memory block and break the reference to the parent data buffer:
```python
clean_subset = df[0:10].copy()
```
This allows the parent memory block to be safely garbage-collected.

---

## Q3: Does calling `.str.lower()` on a column run at native vectorized speed?

### Standard Answer
It depends on the underlying backing array type:
*   **Standard Object Arrays:** If the column is backed by standard Python `object` types, the `.str` accessor acts as a syntactic wrapper around a standard Python for-loop, running at standard Python speed.
*   **PyArrow Arrays:** If the column is backed by Arrow string types (`string[pyarrow]`), the operations are vectorized and execute directly in optimized C++ memory loops.
