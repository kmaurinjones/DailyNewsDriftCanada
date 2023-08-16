import os
import pandas as pd
from general_funcs import *
import plotly.express as px

def find_csv_files(directory_path):
    """Returns a list of all .csv files in the given directory"""
    return [file for file in os.listdir(directory_path) if file.endswith('.csv')]

# Example usage
directory_path = '../data/'  # current directory
csv_files = find_csv_files(directory_path)
most_recent_10_days = sorted(csv_files)[::-1][:20]

### Making grand ground and full dfs of 10 most recent days

grouped_dfs = []
full_dfs = []
for fpath in most_recent_10_days:
    df = pd.read_csv('../data/' + fpath)

    # grouped dfs
    if "grouped" in fpath:
        grouped_dfs.append(df)

    # full dfs
    else:
        full_dfs.append(df)

grouped_df_10 = pd.concat(grouped_dfs, axis = 0, ignore_index = True).sort_values(by = 'date', ascending = True).reset_index(drop = True)
grouped_df_10['date_str'] = grouped_df_10['date'].apply(lambda x: get_date_str(x))

full_df_10 = pd.concat(full_dfs, axis = 0, ignore_index = True).sort_values(by = 'date', ascending = True).reset_index(drop = True)
full_df_10['date_str'] = full_df_10['date'].apply(lambda x: get_date_str(x))

### THIS IS THE PLOT -- this should be called in the app.py file

def show_grand_plot():

    fig = px.line(grouped_df_10, x = 'date_str', y = 'chosen_label_val', color = 'source', title = "Sentiment Valency over Time", markers = True)
    fig.update_layout(
        title = "Sentiment of Canadian News Outlets Over Time",
        xaxis_title = "Date",
        yaxis_title = "Sentiment Valence",
        xaxis = dict(type = 'category')  # Set x-axis type to 'category'
    )

    return fig

# fig.show()