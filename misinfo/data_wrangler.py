import pandas as pd


def load_and_process(csv_path, process_fn, chunksize, num_chunks=None):
    """Loads and processes data from a file in chunks, so it can handle large data file.

    Arguments
    ---------
    csv_path : str
        path to the file to read in
    process_fn : function
        a function that takes in a df, procees it and returns processed df
    chunksize : int
        number of rows to read in at a time
    num_chunks : int, optional
        number of chunks to process, if None will process all (default=None)

    Returns
    -------
    processed_df : Pandas.DataFrame
        the procees data frame
    """
    df_reader = pd.read_csv(csv_path, chunksize=chunksize)

    processed_chunks = []
    i = 0
    for chunk in df_reader:
        print(f"Processing chunk {i}")
        processed_chunks.append(process_fn(chunk))
        i += 1
        if num_chunks is not None and i >= num_chunks:
            break

    return pd.concat(processed_chunks)


def get_columns(csv_path, columns, chunksize=200, num_chunks=None):
    """Loads values in given columns from a csv into a pandas dataframe

    Arguments
    ---------
    csv_path : str
        path to the file to read in
    columns : list
        list of column headers to read in
    chunksize : int, optional
        number of rows to read in at a time (default=10000)

    Returns:
    --------
    pandas.DataFrame
        dataframe containing only columns of interest
    """
    def get_cols(df_chunk):
        return df_chunk[columns]

    return load_and_process(csv_path, get_cols, chunksize, num_chunks)
