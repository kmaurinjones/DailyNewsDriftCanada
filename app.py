import streamlit as st
from streamlit_extras.stateful_button import button # for button that can maintain its clicked state
import pandas as pd
import os
from general_funcs import *
from plot import *

st.title("**📰🍁 DailyNewsDriftCanada 📈📉**")

### App Motivation Explained
app_about = """
DailyNewsDriftCanada was born out of a desire to navigate the often tumultuous waters of news media. In today's fast-paced world, headlines flood our screens, and discerning their overall sentiment can be overwhelming. The aim is to provide a clear, concise snapshot of the emotional undertones behind Canadian news outlets' headlines. By tracking and comparing these sentiments over time, we hope to foster a deeper understanding of the media landscape, enabling users to engage with news more thoughtfully and critically. DailyNewsDriftCanada isn't just an app, it's a compass for the modern news consumer.
"""
st.write("**What is DailyNewsDriftCanada?**")
st.write(app_about.strip())

### Show Plot
updated_grand_plot = show_grand_plot()
st.plotly_chart(updated_grand_plot)

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

    st.write("**The aggregated sentiments of today's headlines are:**")
    st.dataframe(data = today_grouped)

    st.write("**All collected headlines from today are:**")
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
    Each of the news sources mentioned in the graph above posts several news headlines, which are all posted on specific webpages. The headlines from these webpages are collected through something called Web Scraping. Sentiment Analysis is then performed to quantify how 'negative', 'positive', and 'neutral' each headline is, and these sentiment valencies are then aggregated across each day's posts, which gives us the daily average sentiment valency. This is what is shown in the graph, above.
    """
    st.write("**How does it work?**")
    st.write(how_it_works.strip())

    compound_explained = """
    This is what is actually shown in the graph, above. The score is not a value provided by the Sentiment Analysis model, directly, but instead of a value calculated using each of the positive, negative, and neutral scores. To calculate the compound sentiment score of a headline we subtract the 'negative' score from the 'positive' score, and then multiply the difference it by 1 minus the 'neutral' score of the headline. See the formula, below.
    """
    st.write("**'Compound' Score:**")
    st.write(compound_explained.strip())
    st.latex(r"\text{compound\_score} = \left( \text{positive\_score} - \left| \text{negative\_score} \right| \right) \times \left( 1 - \text{neutral\_score} \right)")

st.divider()

eop_message = """
Thanks for checking out DailyNewsDriftCanada. If you have any questions or feedback, feel free to email me at kmaurinjones@gmail.com
"""

st.write(eop_message.strip())