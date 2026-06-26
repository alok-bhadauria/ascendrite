import numpy as np
import pandas as pd


def optimize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Downcasts numeric types and converts object columns to categorical type

    to minimize DataFrame memory footprint.
    """
    optimized_df = df.copy()

    for col in optimized_df.columns:
        col_type = optimized_df[col].dtype

        if col_type == "object":
            # Determine cardinality ratio
            num_unique = len(optimized_df[col].unique())
            num_total = len(optimized_df[col])
            if num_unique / num_total < 0.5:
                optimized_df[col] = optimized_df[col].astype("category")

        elif np.issubdtype(col_type, np.integer):
            optimized_df[col] = pd.to_numeric(
                optimized_df[col], downcast="integer"
            )

        elif np.issubdtype(col_type, np.floating):
            optimized_df[col] = pd.to_numeric(
                optimized_df[col], downcast="float"
            )

    return optimized_df


def compute_chunked_mean(file_path: str, target_column: str, chunk_size: int):
    """Computes the mean of a column in a large file using chunked streaming

    to limit maximum memory footprint.
    """
    running_sum = 0.0
    running_count = 0

    # Read the file in chunks
    chunks = pd.read_csv(file_path, chunksize=chunk_size)

    for chunk in chunks:
        # Check if column exists
        if target_column in chunk.columns:
            # Drop null values for correct mean estimation
            valid_values = chunk[target_column].dropna()
            running_sum += valid_values.sum()
            running_count += len(valid_values)

    if running_count == 0:
        raise ValueError("No valid observations found.")

    return running_sum / running_count
