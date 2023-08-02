import pandas as pd
import os
import matplotlib.pyplot as plt


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
    dataf = pd.read_csv(str_path_csv_file, index_col=0)

    # make a copy of dataf to work with
    df = dataf.copy()

    # drop possible empty third column
    df = df.dropna(how='all', axis=1)

    # drop rows with empty values
    df = df.dropna()

    # drop rows with negative values
    df = df[df >= 0].dropna()

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

    # calculate number of gaps longer than one month using the difference between the index values
    calculated_stats['n_gaps'] = df.index.to_series().diff().dt.days.gt(31).sum()

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


def function_to_create_graphs(str_path_csv_file: str) -> None:
    """
    create graphs by column for a single csv file
    parameters:
    str_path_csv_file : str
        path to csv file

    returns:
    None
    """
    df = pd.read_csv(str_path_csv_file, index_col=0)
    # convert last observed column to datetime then int
    df['last_obs'] = pd.to_datetime(df['last_obs'], errors='coerce')
    df['last_obs'] = df['last_obs'].dt.year
    # convert float columns to int
    df['last_year'] = df['last_year'].astype(int)
    df['first_year'] = df['first_year'].astype(int)
    # TODO: add in a line that checks for duplicate stream gauge ids and prints them out
    # TODO: fix peru_116 years

    # add unit attribute to each column of the dataframe
    units = ['m3/s', 'm3/s', 'm3/s', 'm3/s', 'm3/s', 'm3/s', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
             ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    tuples = list(zip(df.columns, units))
    df.columns = pd.MultiIndex.from_tuples(tuples, names=['name', 'units'])

    for column in df.columns:
        column_name = column[0]
        column_units = column[1]
        create_histogram(df[column[0]], column_name, column_units)
        create_boxplot(df[column[0]], column_name, column_units)
        include_outliers = False
        create_histogram(df[column[0]], column_name, column_units, include_outliers)
        create_boxplot(df[column[0]], column_name, column_units, include_outliers)


def create_histogram(df_column, column_name, column_units, include_outliers=True):
    """
    create histogram for columns, choosing to include outliers or not
    parameters:
        df_column : pd.DataFrame
            column of data from big dataframe
        column_name : str
            name of column
        column_units : str
            units of column
        include_outliers : bool
            whether to include outliers in the histogram

    returns:
    None
    """
    if not include_outliers:
        iqr = df_column.quantile(0.75) - df_column.quantile(0.25)
        df_column = df_column[(df_column < df_column.quantile(0.75) + 1.5 * iqr) & (df_column > df_column.quantile(0.25)

                                                                                    - 1.5 * iqr)]
    folder_name = 'histograms_with_outliers' if include_outliers else 'histograms_without_outliers'
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    # Generate the file path for saving the histogram
    file_path = os.path.join(folder_name, f'{column_name}_histogram.png')
    # Create and save the histogram
    histogram = df_column.plot.hist(bins=10)
    plt.title(f'{column_name}{" without outliers" if not include_outliers else ""}')
    plt.xlabel(f'{column_name} ({column_units})' if column_units != " " else column_name)
    plt.ylabel('Frequency')
    plt.bar_label(histogram.containers[0])
    histogram.legend().remove()
    plt.savefig(file_path)


def create_boxplot(df_column, column_name, column_units, include_outliers=True):
    """
    create boxplot for columns, choosing to include outliers or not
    parameters:
        df_column : pd.DataFrame
            column of data from big dataframe
        column_name : str
            name of column
        column_units : str
            units of column
        include_outliers : bool
            whether to include outliers in the boxplot

    returns:
    None
    """
    folder_name = 'boxplots_with_outliers' if include_outliers else 'boxplots_without_outliers'
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    # Generate the file path for saving the boxplot
    file_path = os.path.join(folder_name, f'{column_name}_boxplot.png')
    # create and save the boxplot
    df_column.plot.box(showfliers=include_outliers)
    plt.title(f'{column_name}{" without outliers" if not include_outliers else ""}')
    plt.ylabel(f'{column_name} {column_units}')
    plt.xticks([])
    plt.savefig(file_path)
