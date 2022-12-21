import pandas as pd
import os


def function_to_calculate_stats(str_path_csv_file: str) -> pd.DataFrame:
    """
    calculate stats for a single csv file
    parameters:
    str_path_csv_file : str
        path to csv file

    returns:
    pd.DataFrame
        a dataframe with stats for each column in the csv file
    """
    df = pd.read_csv(str_path_csv_file, index_col=0)
    df.index = pd.to_datetime(df.index)

    # dictionary to keep track of stats
    calculated_stats = {}

    # calculate stats and add to the dictionary

    # calculate mean
    calculated_stats['mean'] = df.mean()

    # calculate median
    calculated_stats['median'] = df.median()

    # calculate min
    calculated_stats['min'] = df.min()

    # calculate 25th percentile
    calculated_stats['q1'] = df.quantile(0.25)

    # calculate 75th percentile
    calculated_stats['q3'] = df.quantile(0.75)

    # calculate max
    calculated_stats['max'] = df.max()

    # calculate skew
    calculated_stats['skew'] = df.skew()

    # calculate std
    calculated_stats['stdev'] = df.std()

    # make return dataframe
    df_to_return = pd.DataFrame(calculated_stats)
    # set the index value to be the gauge_id which is the name of the csv file
    df_to_return.index = [os.path.basename(str_path_csv_file).replace('.csv', ''), ]

    return df_to_return
