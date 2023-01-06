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

    # drop possible empty third column
    df = df.dropna(how='all', axis=1)

    # drop rows with empty values
    df = df.dropna()

    df.index = pd.to_datetime(df.index)
    # don't return anything if there are no measurements
    if df.empty:
        return  # return None

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
    calculated_stats['q1'] = df.quantile(0.25, numeric_only=True)

    # calculate 75th percentile
    calculated_stats['q3'] = df.quantile(0.75, numeric_only=True)

    # calculate max
    calculated_stats['max'] = df.max()

    # calculate skew
    calculated_stats['skew'] = df.skew()

    # calculate std
    calculated_stats['stdev'] = df.std()

    # calculate total measurements
    calculated_stats['n'] = df.count()

    # calculate number of measurements per month
    calculated_stats['n_jan'] = df[df.index.month == 1].count()
    calculated_stats['n_feb'] = df[df.index.month == 2].count()
    calculated_stats['n_mar'] = df[df.index.month == 3].count()
    calculated_stats['n_apr'] = df[df.index.month == 4].count()
    calculated_stats['n_may'] = df[df.index.month == 5].count()
    calculated_stats['n_jun'] = df[df.index.month == 6].count()
    calculated_stats['n_jul'] = df[df.index.month == 7].count()
    calculated_stats['n_aug'] = df[df.index.month == 8].count()
    calculated_stats['n_sep'] = df[df.index.month == 9].count()
    calculated_stats['n_oct'] = df[df.index.month == 10].count()
    calculated_stats['n_nov'] = df[df.index.month == 11].count()
    calculated_stats['n_dec'] = df[df.index.month == 12].count()

    # calculate number of gaps longer than one month
    calculated_stats['n_gaps'] = df.resample('M').count().isnull().sum()

    # see if most recent measurement is over a year ago
    calculated_stats['last_obs'] = df.index.max()

    # year of first measurement
    calculated_stats['first_year'] = df.index.year.min()

    # year of last measurement
    calculated_stats['last_year'] = df.index.year.max()

    # calculate average number of measurements per year
    calculated_stats['yearly_avg'] = calculated_stats['n'] / df.index.year.nunique()

    # make return dataframe
    df_to_return = pd.DataFrame(calculated_stats)
    # set the index value to be the gauge_id which is the name of the csv file
    df_to_return.index = [os.path.basename(str_path_csv_file).replace('.csv', ''), ]
    df_to_return.index.name = 'gauge_id'
    return df_to_return
