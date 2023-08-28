import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt


def calculate_stats(str_path_csv_file: str) -> pd.DataFrame:
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

    # calculate stats and add to a dictionary

    statistics = ['mean', 'median', 'min', 'q1', 'q3', 'max', 'skew', 'std']

    calculated_stats = {}

    for stat in statistics:
        if stat in ['q1', 'q3']:
            calculated_stats[stat] = df.quantile(0.25 if stat == 'q1' else 0.75, numeric_only=True)
        else:
            calculated_stats[stat] = getattr(df, stat)()

    # calculate total measurements
    calculated_stats['n'] = df.count()

    # calculate number of measurements per month
    for month in range(1, 13):
        month_name = pd.to_datetime(str(month), format='%m').strftime('%B')  # should it be 0?
        calculated_stats[f'n_{month_name.lower()}'] = (df.index.month == month).sum()

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


def create_plots(df: pd.DataFrame) -> None:
    """
    create graphs by column for a single csv file
    parameters:
    str_path_csv_file : str
        path to csv file

    returns:
    None
    """
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
    n_col = df.shape[1]
    plot_rows = int(np.sqrt(n_col)) + 1
    plot_cols = plot_rows
    if n_col - np.square(plot_rows - 1) <= plot_rows - 1:
        plot_cols -= 1

    fig, axes = plt.subplots(plot_rows, plot_cols, figsize=(15, 15))
    axes = axes.flatten()
    for i, col in enumerate(df.columns):
        column_name = col[0]
        column_units = col[1]
        ax = axes[i]  # Get the appropriate subplot
        create_histogram(ax, df[col[0]], column_name, column_units)  # Create the histogram
        ax.set_title(col)
    plt.subplots_adjust(wspace=0.4, hspace=0.4)  # Adjust spacing between subplots
    plt.tight_layout()
    plt.show()

    fig, axes = plt.subplots(plot_rows, plot_cols, figsize=(15, 15))
    for i, col in enumerate(df.columns):
        column_name = col[0]
        column_units = col[1]
        ax = axes[i]  # Get the appropriate subplot
        create_boxplot(ax, df[col[0]], column_name, column_units)  # Create the histogram
        ax.set_title(col)
    plt.subplots_adjust(wspace=0.4, hspace=0.4)  # Adjust spacing between subplots
    plt.tight_layout()
    plt.show()
    for column in df.columns:
        column_name = column[0]
        column_units = column[1]
        fig, ax,
        create_histogram(df[column[0]], column_name, column_units)
        create_boxplot(df[column[0]], column_name, column_units)
        include_outliers = False
        create_histogram(df[column[0]], column_name, column_units, include_outliers)
        create_boxplot(df[column[0]], column_name, column_units, include_outliers)


def create_histogram(ax, df_column, column_name, column_units, include_outliers=True):
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
    histogram = df_column.plot.hist(ax=ax, bins=10)
    ax.set_title(f'{column_name}{" without outliers" if not include_outliers else ""}')
    ax.set_xlabel(f'{column_name} ({column_units})' if column_units != " " else column_name)
    ax.set_ylabel('Frequency')
    ax.bar_label(histogram.containers[0])
    histogram.legend().remove()


def create_boxplot(ax, df_column, column_name, column_units, include_outliers=True):
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
    df_column.plot.box(ax=ax, showfliers=include_outliers)
    ax.set_title(f'{column_name}{" without outliers" if not include_outliers else ""}')
    ax.set_ylabel(f'{column_name} {column_units}')
    ax.set_xticks([])
