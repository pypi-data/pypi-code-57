def read_parquet_current_folder(
    pattern=False, print_filenames=False, subfolder=False, columns=""
):
    """This function takes in arguments and reads and then joins together all parquet
    files that matches the pattern given

    Keyword Arguments:
        pattern {string} -- this will take the string given and use it as the pattern
        for the globbing of the parquetfiles (default: {False})

        print_filenames {bool} -- enter True if you want to see printed out all of the
        files that were used to create the dataframe (default: {False})

        subfolder {string} -- if the parquet files you want to glob are in a 
        subfolder enter that string (default: {False})

        columns {list} -- this must be a list of strings that match the column names
        that are used in the dataframe the default will load all of the columns

    Returns:
        dataframe -- this is the concatinated dataframe from the files globbed
    """
    import pathlib
    import pandas as pd
    import pyarrow.parquet as pq
    import pyarrow as pa
    from pprint import pprint

    def read_in_parquet_files(files, dta, columns):
        """this function reads each file from the glob and merges them together into one
        pandas dataframe

        Arguments:
            files {list} -- this is list of pathlib path objects for parquet files

            dta {None} -- this is a NoneType for testing for previous dataframe reading

            columns {list} -- this must be a list of strings that match the column names
            that are used in the dataframe the default will load all of the columns

        Returns:
            dataframe -- this is the merged pandas dataframe
        """
        if len(files) == 0:
            print(
                f"function read_parquet_current_folder did not find any parquet files matching the pattern given in the current folder"
            )
        else:
            for file in files:
                if dta is None:
                    if columns == "":
                        dta = pq.read_table(file)
                    else:
                        dta = pq.read_table(file, columns=columns)
                    dta = dta.to_pandas()
                else:
                    if columns == "":
                        dta1 = pq.read_table(file)
                        dta1 = dta1.to_pandas()
                    else:
                        dta1 = pq.read_table(file, columns=columns)
                        dta1 = dta1.to_pandas()
                    pd.concat([dta, dta1])
            return dta

    path = pathlib.Path(".").parent
    if subfolder:
        path = path / subfolder
        print(path)
    dta = None
    if pattern is False:
        files = list(path.glob("*.parquet"))
        dta = read_in_parquet_files(files, dta, columns)
    elif ".parquet" not in pattern:
        files = list(path.glob(f"{pattern}*.parquet"))
        dta = read_in_parquet_files(files, dta, columns)
    else:
        files = list(path.glob(pattern))
        dta = read_in_parquet_files(files, dta, columns)
    if print_filenames is True:
        pprint([file.name for file in files])
    return dta


def concat_dataframes(dataframes):
    """this simple function concatinates all of the dataframes that are entered

    Arguments:
        dataframes {list of dataframes} -- a list of pandas dataframes

    Returns:
        pandas dataframes -- this is a combined dataframe
    """
    import pandas as pd

    return pd.concat(dataframes)


def read_parquet_by_path(path, columns=None):
    """this function will read in all files given if the path variable is a list of
    pathlib objects or will read in the file if the path is one pathlib object

    Args:
        path (pathlib object): this must be a full path string or a pathlib object for a
        parquet file

        columns (list of strings, optional): this must be a list of strings even if
        there is only one column included, also the columns must be present in the files
        included in the path otherwise it will throw an error. Defaults to None.

    Returns:
        dataframe: this returns the pandas dataframe of the path object or a combined
        pandas dataframe if there was a list of paths given
    """
    import pyarrow as pa
    import pyarrow.parquet as pq
    import pandas as pd

    if type(path) == list:
        dataframe_list = []
        for file in path:
            if columns is None:
                if path.name.endswith(".parquet"):
                    dta = pq.read_table(path)
                    dataframe_list.append(dta.to_pandas())
            else:
                if path.name.endswith(".parquet", columns=columns):
                    dta = pq.read_table(path)
                    dataframe_list.append(dta.to_pandas())
        dta = pd.concat(dataframe_list)
    else:
        if columns is None:
            if path.name.endswith(".parquet"):
                dta = pq.read_table(path)
                dta = dta.to_pandas()
        else:
            if path.name.endswith(".parquet", columns=columns):
                dta = pq.read_table(path)
                dta = dta.to_pandas()
    return dta


def length_parquet_files(files, columns=None):
    """This function will take a list of parquet files and print the name of each file
    along with the number of rows for that file.

    Then at the end will print out the total number of rows for all of the parquet files
    included in the list.
    """
    import pyarrow as pa
    import pyarrow.parquet as pq
    import pandas as pd

    total_len = 0
    for file in files:
        if columns is None:
            dta = pq.read_table(file)
        else:
            dta = pq.read_table(file, columns=columns)
        dta = dta.to_pandas()
        row_num = len(dta)
        print(f"the length of {file.name} is: {row_num}")
        total_len += row_num
    print(f"the length of the files is: {total_num}")


def display_full_dataframe(dta):
    """displays a dataframe without cutting anything off for being too long

    Arguments:
        dta {dataframe} -- a dataframe you wish to display
    """
    import pandas as pd

    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        print(dta)


def limit_dataframe(dta, number_of_rows):
    return dta.iloc[
        0:number_of_rows,
    ]


def save_dataframe_as_parquet(dta, filename="output.parquet", pathlib_destination=""):
    """this function saves a pandas dataframe as a parquet file compressed with the
    zstandard compression algorithm

    Arguments:
        dta {pandas dataframe} -- the dataframe you want saved

    Keyword Arguments:
        filename {str} -- the name of the file you want saved, if you use this option
        the file will be saved in the same folder as the script used
        (default: {"output.parquet"})

        pathlib_destination {pathlib object} -- if you use this option make sure that
        you have both the folder and filename that is part of the pathlib object
        (default: {""})
    """
    import pathlib
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq

    if pathlib_destination != "":
        filename = pathlib.Path(".")
        if "/" in pathlib_destination:
            destination_list = pathlib_destination.split("/")
            for count, item in enumerate(destination_list):
                filename = filename / f"{destination_list[count]}"
        else:
            filename = filename / pathlib_destination
        filename.parent.mkdir(parents=True, exist_ok=True)
    elif filename == "output.parquet":
        pathlib_destination = pathlib.Path(".").parent / filename
    else:
        print(
            "please enter either a filename (this will save the file into the current filder) or enter a pathlib destination with the filename"
        )
    dta = pa.Table.from_pandas(dta)
    pq.write_table(dta, filename, compression="zstd")
