# DailyNewsDriftCanada

## What is it?

DailyNewsDriftCanada is a tool designed to analyze the sentiment of news headlines from various Canadian media outlets. In an age where we're constantly bombarded with headlines, understanding their overall tone can be challenging. This application offers an objective overview of the emotional context behind these headlines. By monitoring and comparing these sentiments over a duration, the intent is to offer users insights into the evolving media environment, encouraging a more informed and discerning approach to news consumption. Essentially, DailyNewsDriftCanada serves as a guide to understanding the sentiment trends in Canadian news.

## Project Motivation

As has been theorized, emotional intensity and 'clickbait' are thought to be conducive to higher clickthrough rates of webpages. Ancedotally, as someone who typically doesn't read 'the news' - largely because it usually feels highly skewed towards negative news, I thought this would be interesting to see over time, more empirically.

## How does it work?

Every day, news headlines (text and URLs) are scraped from the respective webpages of https://www.cbc.ca/news, https://www.ctvnews.ca/canada, and https://globalnews.ca/canada/. Each headline is then put through a Sentiment Analysis Model (https://huggingface.co/facebook/bart-large-mnli), score how 'positive', 'negative', and 'neutral' each headline is. No further context is used for each headline, as the intent of this project is to evaluate the emotional representation of each headline, just as a person would when reading through the headlines on the webpage.

Using the score for each label, a 'compound' score is then calculated, which takes into account all three labels. This achieves two things: 1) it creates one overall sentiment score for the headline that can be used more comparably in other tasks; and 2) it normalizes the score on a scale from [-1, 1]. This makes for a more visualizable data point on a plot - which is the end goal of the data collection, wrangling, and manipulation used in this project.

The 'compound' score for each headline is created as follows:

$\text{compound} = \left( \text{positive} - \left| \text{negative} \right| \right) \times \left( 1 - \text{neutral} \right)")$

## Contact

Thank you for checking out this project. If you have any questions or feedback, feel free to email me at kmaurinjones@gmail.com