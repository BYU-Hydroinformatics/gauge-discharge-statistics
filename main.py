# This is a sample Python script.
import functions as function
import pandas as pd
import glob
import os

directory = 'observed_discharge'
df = pd.DataFrame()
for filename in glob.glob('/Users/student/PycharmProjects/gauge-discharge-test-code/observed_discharge/*.csv'):
    if os.path.getsize(filename) > 0:
        csv = os.path.join(directory, filename)
        print(csv)
        df = pd.concat([df, function.function_to_calculate_stats(csv)])

# sort alphabetically by first column
df = df.sort_values(by=['gauge_id'])

# save to csv
df.to_csv('stats.csv')

# create graphs
function.function_to_create_graphs('stats.csv')
