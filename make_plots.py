import pandas as pd
from functions import create_plots

df = pd.read_csv('stats_updated.csv')
create_plots(df)
