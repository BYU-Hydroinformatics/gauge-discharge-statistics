# This is a sample Python script.
import functions as function
import pandas as pd
from glob import glob
import os

directory = 'observed_discharge'
df = pd.DataFrame()
for filename in glob('/Users/Downloads/ObservedDischarge-selected/*/Observed_Data/*.csv') + \
                glob('/Users/joshogden/Downloads/ObservedDischarge-selected/*/*/Observed_Data/*.csv'):
    if os.path.getsize(filename) > 0:
        df = pd.concat([df, function.calculate_stats(filename)])

# sort alphabetically by first column
df = df.sort_values(by=['gauge_id'])

# save to csv
df.to_csv('stats_updated.csv', index=False)

# create graphs
function.create_plots(df)
print("completed")
'''
## edit peru_116.csv dates to be 19xx instead of 20xx for the ones that are wrong
# read in peru_116.csv to df
df = pd.read_csv('/Users/student/PycharmProjects/gauge-discharge-statistics/observed_discharge/observed_discharge/peru_116.csv')

# Specify the column containing the years
year_column = 'Datetime'

# Convert years starting with '20' to start with '19' for a specific number of lines
line_limit = 8034  # Set the desired number of lines to modify

df_subset = df.head(line_limit).copy()  # Select the specified number of lines and make a copy
# change datetime column to datetime format
df_subset[year_column] = pd.to_datetime(df_subset[year_column], format='%Y-%m-%d %H:%M:%S')
# change datetime column to string format
df_subset[year_column] = df_subset[year_column].dt.strftime('%Y-%m-%d %H:%M:%S')
# replace 20 with 19
df_subset[year_column] = df_subset[year_column].str.replace('20', '19')
# change datetime column back to datetime format
df_subset[year_column] = pd.to_datetime(df_subset[year_column], format='%Y-%m-%d %H:%M:%S')
# change datetime column back to object format
df_subset[year_column] = df_subset[year_column].dt.strftime('%Y-%m-%d %H:%M:%S')

# Update the modified subset back into the original DataFrame
df.update(df_subset) # pretty sure this line is the issue

# Save the modified DataFrame to a new CSV file in observed_discharge
df.to_csv('/Users/student/PycharmProjects/gauge-discharge-statistics/observed_discharge/observed_discharge/peru_116.csv', index=False)
'''
# TODO: possible improvement - combine some box plots into one graph - do it in R?