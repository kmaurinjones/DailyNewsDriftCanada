import os
import pandas as pd
from general_funcs import *
import plotly.express as px


def find_csv_files(directory_path):
    """Returns a list of all .csv files in the given directory"""
    return [file for file in os.listdir(directory_path) if file.endswith('.csv')]

# Example usage
directory_path = 'data/'  # current directory
csv_files = find_csv_files(directory_path)
days_to_display = 60
most_recent_x_days = sorted(csv_files)[::-1][:days_to_display*2] # twice as many because there are two files for each day

### Making grand ground and full dfs of 10 most recent days

grouped_dfs = []
full_dfs = []
for fpath in most_recent_x_days:
    df = pd.read_csv(directory_path + fpath)

    # grouped dfs
    if "grouped" in fpath:
        grouped_dfs.append(df)

    # full dfs
    else:
        full_dfs.append(df)

grouped_df_recent = pd.concat(grouped_dfs, axis = 0, ignore_index = True).sort_values(by = 'date', ascending = True).reset_index(drop = True)
grouped_df_recent['date_str'] = grouped_df_recent['date'].apply(lambda x: get_date_str(x))

full_df_recent = pd.concat(full_dfs, axis = 0, ignore_index = True).sort_values(by = 'date', ascending = True).reset_index(drop = True)
full_df_recent['date_str'] = full_df_recent['date'].apply(lambda x: get_date_str(x))

# ### THIS IS THE PLOT -- this should be called in the app.py file

# def show_grand_plot():

#     fig = px.line(grouped_df_recent, x = 'date_str', y = 'compound', color = 'source',
#             #   color_discrete_map = {"CBC": "#EC1D2D", "CTV": "#0046D4", "Global": "#231F20"},
#             #   title = "Sentiment Valency over Time",
#               markers = True)

#     # Updating layout with font sizes and title position
#     fig.update_layout(
#         title = {
#             'text': "Sentiment of Canadian News Outlets Over Time",
#             'y': 0.95,
#             'x': 0.5,
#             'xanchor': 'center',
#             'yanchor': 'top',
#             'font': {
#                 'size': 20  # or any desired font size
#             }
#         },
#         xaxis_title = "Date",
#         xaxis_title_font_size = 16,  # or any desired font size
#         xaxis_tickfont_size = 14,  # or any desired font size
#         yaxis_title = "Sentiment Valence",
#         yaxis_title_font_size = 16,  # or any desired font size
#         yaxis_tickfont_size = 14   # or any desired font size
#     )
#     return fig




import pandas as pd
import plotly.express as px

def show_grand_plot():
    # Assuming that 'date_str' is a string; converting it to datetime for sorting
    grouped_df_recent['date_str'] = pd.to_datetime(grouped_df_recent['date_str'])
    grouped_df_recent.sort_values('date_str', inplace=True)

    # Identify the last 7 days
    last_day = grouped_df_recent['date_str'].max()
    first_day_of_last_week = last_day - pd.Timedelta(days=6)

    fig = px.line(grouped_df_recent, x='date_str', y='compound', color='source', markers=True)

    # Updating layout
    fig.update_layout(
        title = {
            'text': "Sentiment of Canadian News Outlets Over Time",
            'y': 0.99, # height of title on plot
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20}
            },
        xaxis_title="Date",
        xaxis_title_font_size=16,
        xaxis_tickfont_size=14,
        yaxis_title="Sentiment Valence",
        yaxis_title_font_size=16,
        yaxis_tickfont_size=14,
        # Adding date range selector
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=3, label="3m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(step="all", label="All")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date",
            # Default to the last 7 days
            range=[first_day_of_last_week, last_day]
        )
    )
    return fig