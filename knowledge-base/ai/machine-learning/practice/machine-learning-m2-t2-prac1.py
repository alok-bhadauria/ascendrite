import pandas as pd


def chunked_filter_and_save(
    input_file: str, output_file: str, target_column: str, threshold: float
) -> int:
    """Reads input_file in chunks, filters rows where target_column > threshold,

    and writes them to output_file in chunks.
    Should return the total count of filtered rows written.

    Rules:
    1. Memory must remain bounded (no loading the whole file).
    2. Write headers only for the first chunk to avoid duplicated titles.
    """
    total_written = 0
    chunk_size = 10000

    # Stream the data in chunks
    chunks = pd.read_csv(input_file, chunksize=chunk_size)

    for i, chunk in enumerate(chunks):
        # Filter rows
        filtered_chunk = chunk[chunk[target_column] > threshold]
        num_rows = len(filtered_chunk)

        if num_rows > 0:
            # Write to output file.
            # If it's the first chunk being written, write the header.
            # Otherwise, append without header.
            mode = "w" if total_written == 0 else "a"
            header = True if total_written == 0 else False

            filtered_chunk.to_csv(
                output_file, mode=mode, header=header, index=False
            )
            total_written += num_rows

    return total_written
