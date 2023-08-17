import streamlit as st
from streamlit_extras.stateful_button import button # for button that can maintain its clicked state
import pandas as pd
import os
from datetime import datetime, timedelta
from general_funcs import *
from plot import *

st.title("**📰🍁 DailyNewsDriftCanada 📈📉**")

st.divider()

### App Motivation Explained
app_about = """
DailyNewsDriftCanada is a tool designed to analyze the sentiment of news headlines from various Canadian media outlets. In an age where we're constantly bombarded with headlines, understanding their overall tone can be challenging. This application offers an objective overview of the emotional context behind these headlines. By monitoring and comparing these sentiments over a duration, the intent is to offer users insights into the evolving media environment, encouraging a more informed and discerning approach to news consumption. Essentially, DailyNewsDriftCanada serves as a guide to understanding the sentiment trends in Canadian news.
"""
st.write("**What is DailyNewsDriftCanada?**")
st.write(app_about.strip())

### Show Plot
updated_grand_plot = show_grand_plot()
st.plotly_chart(updated_grand_plot)

# def get_time_minus_4h():
#     now = datetime.now()
#     four_hours_ago = now - timedelta(hours=4)
#     time_minus_4h = four_hours_ago.strftime("%H:%M:%S")
#     date_of_time_minus_4h = four_hours_ago.strftime("%Y-%m-%d")
#     return date_of_time_minus_4h, time_minus_4h

# date, time = get_time_minus_4h()
# st.write(f"*Data last updated: {date}, {time} EST*")
st.write(f"*Data updated at 10am and 9pm EST, daily*")

### Chart Explanation
chart_explained = """
Sentiment valence, a scale between -1 and 1, measures the emotional tone of text. A score of -1 represents extreme negativity, while 1 indicates extreme positivity. Values closer to 0 signify neutrality. This scale helps quantify sentiments in language, which is useful in Natural Language Processing tasks like sentiment analysis, as used here on the headlines from each of the news sources.
"""
st.write("**Chart Explained:**")
st.write(chart_explained.strip())

st.divider()

### See the headlines that contributed to the plot
st.write("**Interested in the headlines that contributed to today's data?**")
show_headlines = button("Show headlines", key = "show_headlines_button")
if show_headlines:

    ### Loading and displaying today's dfs (grouped and full)
    directory_path = "data/"
    today_date = get_today_iso()
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
    Imagine you're watching a series of movie scenes, and after each scene, you're asked to turn a dial based on how the scene made you feel. If the scene made you feel really positive and happy, you'd turn the dial all the way to the right, let's say to the number 1. If the scene made you feel very negative or sad, you'd turn the dial all the way to the left, to the number -1. If the scene didn't make you feel particularly one way or the other, you'd leave the dial in the middle, around 0. The Sentiment Valence value from a sentiment analysis model is like that dial. It's a score that tells us how positive or negative a piece of text is. If a piece of writing has a score close to 1, it's very positive. If it's close to -1, it's very negative. Anything that falls between -0.1 and 0.1 is considered neutral, meaning the text doesn't swing strongly toward happy or sad feelings—it's more in the middle. In simple terms, Sentiment Valence is like a mood ring for text: it gives us a quick read on whether the text feels happy, sad, or somewhere in between.
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