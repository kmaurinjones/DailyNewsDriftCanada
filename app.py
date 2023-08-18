import streamlit as st
from streamlit_extras.stateful_button import button # for button that can maintain its clicked state
import pandas as pd
import os
from datetime import datetime, timedelta
from general_funcs import *
from plot import *

st.title("**📰🍁 DailyNewsDriftCanada 📈📉**")

# st.write("TEST")

st.divider()

### App Motivation Explained
app_about = """
DailyNewsDriftCanada is a tool designed to analyze the sentiment of news headlines from various Canadian media outlets. In an age where we're constantly bombarded with headlines, understanding their overall tone can be challenging. This application offers an objective overview of the emotional context behind these headlines. By monitoring and comparing these sentiments over a duration, the intent is to offer users insights into the evolving media environment, encouraging a more informed and discerning approach to news consumption. Essentially, DailyNewsDriftCanada serves as a guide to understanding the sentiment trends in Canadian news.
"""
st.write("**What is DailyNewsDriftCanada?**")
st.write(app_about.strip())

########################################################################################################################################################################

# import os
# import pandas as pd
# from general_funcs import *
import plotly.express as px

def find_csv_files(directory_path):
    """Returns a list of all .csv files in the given directory"""
    return [file for file in os.listdir(directory_path) if file.endswith('.csv')]

# Example usage
directory_path = 'data/'  # current directory
csv_files = find_csv_files(directory_path)
days_to_display = 20
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

### THIS IS THE PLOT -- this should be called in the app.py file

def show_grand_plot():

    fig = px.line(grouped_df_recent, x = 'date_str', y = 'compound', color = 'source',
            #   color_discrete_map = {"CBC": "#EC1D2D", "CTV": "#0046D4", "Global": "#231F20"},
            #   title = "Sentiment Valency over Time",
              markers = True)

    # Updating layout with font sizes and title position
    fig.update_layout(
        title = {
            'text': "Sentiment of Canadian News Outlets Over Time",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'size': 20  # or any desired font size
            }
        },
        xaxis_title = "Date",
        xaxis_title_font_size = 16,  # or any desired font size
        xaxis_tickfont_size = 14,  # or any desired font size
        yaxis_title = "Sentiment Valence",
        yaxis_title_font_size = 16,  # or any desired font size
        yaxis_tickfont_size = 14   # or any desired font size
    )

    return fig

# fig.show()

########################################################################################################################################################################

### Show Plot
updated_grand_plot = show_grand_plot()
st.plotly_chart(updated_grand_plot)

# logs_path = "/Users/kmaurinjones/Desktop/ds/github_repos/DailyNewsDriftCanada/logs.txt"
logs_path = "logs.txt"

current_logs = [line.strip() for line in open(logs_path, "r").readlines()]

# Display the time minus 4 hours
st.write(f"*Data last updated: {current_logs[-1]}* EST")

today_date = full_df_recent.sort_values(by = "date", ascending = False)['date'].unique()[0]
today_df = full_df_recent[full_df_recent['date'] == today_date]

## display counts of headlines from each source today
sources = today_df['source'].unique().tolist() # list of all unique sources
counts = [len(today_df[today_df['source'] == source]) for source in sources] # list of counts of each source

st.write(f"*The number of headlines collected from each source today is as follows:*")
for source, count in zip(sources, counts):
    st.markdown(f"*- {source}: {count}*")

### Chart Explanation
chart_explained_1 = """
Sentiment valence, a scale between -1 and 1, measures the emotional tone of text. A score of -1 represents extreme negativity, while 1 indicates extreme positivity. Values closer to 0 signify neutrality. This scale helps quantify sentiments in language, which is useful in Natural Language Processing tasks like sentiment analysis, as used here on the headlines from each of the news sources.
"""
chart_explained_2 = """
This chart is intended to be read from the left side to the right side. Check the legend in the upper right-hand corner of the chart to see which news organization corresponds to which line (look for the same colour), then see how the line changes vertically as it moves from the left to the right. From left to right, if the line goes up, it means the headlines of that particular got more positive (on average) from the previous day. Conversely, if the line goes down from left to right, the headlines got more negative (on average) from the previous day. By comparing how one line's behaviour to another, we can get a general idea of how negative or positive one news outlet is compared to another.
"""

st.write("**Chart Explained:**")
st.write(chart_explained_1.strip())
st.write(chart_explained_2.strip())

st.divider()

### See the headlines that contributed to the plot
st.write("**Interested in the headlines that contributed to today's data?**")
show_headlines = button("Show headlines", key = "show_headlines_button")
if show_headlines:

    ### Loading and displaying today's dfs (grouped and full)
    directory_path = "data/"
    # today_date = get_today_iso() # because this is relative to the server's date (which seems to be relative to GMT, which is +4h from EST -- this means that 'today' is different than my 'today' between 8pm and 12am)
    today_date = [line.strip() for line in open(logs_path, "r").readlines()][-1].split(": ")[-1].split(", ")[0] # just the date from the date, time in the update message
    today_dfs_list = [file for file in os.listdir(directory_path) if today_date in file]
    today_grouped = [pd.read_csv(directory_path + df) for df in today_dfs_list if "grouped" in df][0]
    today_full = [pd.read_csv(directory_path + df) for df in today_dfs_list if "full" in df][0]

    st.write("**Aggregated sentiment analysis of today's collected headlines:**")
    st.dataframe(data = today_grouped)

    st.write("**Today's collected headlines:**")
    st.dataframe(data = today_full)

st.divider()

### How the app works
st.write("**Curious about how this app works?**")
show_explained = button("Explain", key = "show_explained_button")
if show_explained:
    ### SA Explained
    sa_defined = """
    Imagine you're watching a series of movie scenes, and after each scene, you're asked to turn a dial based on how the scene made you feel. If the scene made you feel really positive and happy, you'd turn the dial all the way to the right, let's say to the number 1. If the scene made you feel very negative or sad, you'd turn the dial all the way to the left, to the number -1. If the scene didn't make you feel particularly one way or the other, you'd leave the dial in the middle, around 0. The Sentiment Valence value from a sentiment analysis model is like that dial. It's a score that tells us how positive or negative a piece of text is. If a piece of writing has a score close to 1, it's very positive. If it's close to -1, it's very negative. Anything that falls between -0.05 and 0.05 is considered neutral, meaning the text doesn't swing strongly toward happy or sad feelings—it's more in the middle. In simple terms, Sentiment Valence is like a mood ring for text: it gives us a quick read on whether the text feels happy, sad, or somewhere in between.
    """
    st.write("**What is Sentiment Analysis?**")
    st.write(sa_defined.strip())

    ### Methods explained
    how_it_works = """
    Each of the news sources mentioned in the graph above posts several news headlines, which are all posted on specific webpages. The headlines from these webpages are collected through something called Web Scraping. Sentiment Analysis is then performed to quantify how 'negative', 'positive', and 'neutral' each headline is, and these sentiment valencies are then aggregated across each day's posts, which gives us the daily average sentiment valence. This is what is shown in the graph, above.
    """
    st.write("**How does it work?**")
    st.write(how_it_works.strip())

    compound_explained = """
    This is what is actually shown in the graph, above. This score is not a value provided by the Sentiment Analysis model, directly, but instead is a value calculated using each of the positive, negative, and neutral scores. To calculate the compound sentiment score of a headline we subtract the 'negative' score from the 'positive' score, and then multiply the difference by 1 minus the 'neutral' score of the headline. See the formula, below.
    """
    st.write("**'Compound' Score:**")
    st.write(compound_explained.strip())
    st.latex(r"\text{compound\_score} = \left( \text{positive\_score} - \left| \text{negative\_score} \right| \right) \times \left( 1 - \text{neutral\_score} \right)")

st.divider()

eop_message = """
Thanks for checking out DailyNewsDriftCanada. If you have any questions or feedback, feel free to email me at kmaurinjones@gmail.com
"""

st.write(eop_message.strip())