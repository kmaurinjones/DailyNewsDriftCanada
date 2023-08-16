import pandas as pd
from dateutil import parser
from datetime import date
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from tqdm import tqdm
classifier = pipeline("zero-shot-classification", model = "facebook/bart-large-mnli")
from general_funcs import *

### scraping CBC ###

url = "https://www.cbc.ca/news"

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    links = soup.find_all("a")
    cbc_headlines = []
    for link in links:
        headline = link.h3
        href = link['href']

        # make sure both are not None
        if (headline and href):
            cbc_headlines.append((headline.text, "https://www.cbc.ca" + href))
else:
    cbc_headlines = None

### scraping CTV ###

url = "https://www.ctvnews.ca/canada"

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    links = soup.find_all("h3", attrs = {'class' : 'c-list__item__title'})
    ctv_headlines = []
    for link in links:

        # get url and text
        if link.a:
            href = link.a['href'].strip()
            text = link.a.text.strip()

            # make sure both are not None
            if (text and href):
                ctv_headlines.append((text, href))
else:
    ctv_headlines = None

### scraping Global ###

url = "https://globalnews.ca/canada/"

response = requests.get(url)
print(response.status_code)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    links = soup.find_all("a", attrs = {'class' : 'c-posts__inner'})

    global_headlines = []
    for link in links:

        # get span element -- text is here
        if link.span:
            href = link['href'].strip()
            text = link.span.text.strip()

            # make sure both are not None
            if (text and href):
                global_headlines.append((text, href))
else:
    global_headlines = None

def sa_headlines(headlines_urls: list, labels: list, source: str = None):
    """
    Performs Sentiment Analysis (SA) on a list of headlines and returns a dictionary 
    containing the results and other associated data.

    Args:
        headlines_urls (list): A list of tuples where each tuple consists of two elements:
                               1) A headline as a string 
                               2) The corresponding URL as a string
        labels (list): A list of labels to classify each headline.
                       e.g., ['negative', 'positive', 'neutral']
        source (str, optional): The source or origin of the headlines. Defaults to None.

    Returns:
        dict: A dictionary containing the following keys:
              - 'source': List of sources for each headline.
              - 'date': List of dates when each SA was performed.
              - 'headline': List of the provided headlines.
              - 'url': List of URLs corresponding to each headline.
              - 'chosen_label': List of chosen sentiment labels based on the analysis.
              - 'chosen_label_val': List of sentiment values corresponding to the chosen labels.
              - Each label from the `labels` list will also be a key, containing a list of scores.
              - 'compound': (Only if 'negative' and 'positive' and 'neutral' are in `labels`) List of compound scores.

    Raises:
        Any exceptions raised by the `classifier` function will propagate up.

    Note:
        This function assumes the existence of a function named `classifier` 
        which is used for performing the sentiment analysis.

    Examples:
        headlines = [("Great day at the park", "http://example.com/1"), 
                    ("Terrible weather today", "http://example.com/2")]
        labels = ['negative', 'positive', 'neutral']
        result = SA_headlines(headlines, labels, "NewsSource")
    """
    responses_dict = {lab:[] for lab in labels}

    # Initialize the dictionary with keys and empty lists
    responses_dict = {
        'source' : [],
        'date' : [],
        "headline" : [],
        'url' : [],
        "chosen_label" : [],
        'chosen_label_val' : [],
        **responses_dict,  # empty list for each passed label
    }

    # Check if 'negative' and 'positive' labels are provided, and initialize 'compound'
    if ('negative' and 'positive') in labels:
        responses_dict['compound'] = []

    date = get_today_iso()

    # Eliminate duplicate headlines
    headlines_urls = list(set(headlines_urls))

    # Process each headline and perform SA
    for head_text, url in tqdm(headlines_urls, desc = source):
  
        # Add meta data to dictionary
        responses_dict['source'].append(source.strip())
        responses_dict['date'].append(date.strip())
        responses_dict['headline'].append(head_text.strip())
        responses_dict['url'].append(url)

        # Perform Sentiment Analysis using the `classifier` function
        response = classifier(head_text, labels)

        # Add the SA results to the dictionary
        for i in range(len(labels)):
            score = response['scores'][response['labels'].index(labels[i])]
            responses_dict[labels[i]].append(score)

        # Calculate compound score if 'negative', 'positive', and 'neutral' are provided
        if ('negative' and 'positive' and 'neutral') in labels:
            compound = (responses_dict['positive'][-1] - responses_dict['negative'][-1]) * (1 - responses_dict['neutral'][-1])
            responses_dict['compound'].append(compound)
            responses_dict['chosen_label_val'].append(compound)

            # Derive sentiment label from compound score
            if compound >= 0.1:
                responses_dict['chosen_label'].append("positive")
            elif compound <= -0.1:
                responses_dict['chosen_label'].append('negative')
            else:
                responses_dict['chosen_label'].append("neutral")
        # If only one label provided, use the model's label
        else:
            responses_dict['chosen_label_val'].append(response['scores'][0])
            responses_dict['chosen_label'].append(response['labels'][0])

    return responses_dict

### Perform SA on all found headlines

labels = ['positive', 'negative', 'neutral']

# all respective sources and headlines
sources_headlines = [
    ("Global", global_headlines),
    ('CTV', ctv_headlines),
    ('CBC', cbc_headlines)
]

master_results = {}

for source, headlines in sources_headlines:

    # make sure both are not None -- there could be some scraping error and return empty headlines
    if (source and headlines):

        sa_results = sa_headlines(headlines_urls = headlines, labels = labels, source = source)

        # just overwrite the whole dict with the first results
        if not master_results:
            master_results = sa_results

        # afterwards, add everything to each list
        else:
            for key, val in sa_results.items():
                master_results[key].extend(val)

master_df = pd.DataFrame(master_results)

### WRITING DAILY FULL DF TO CSV
master_df.to_csv(f"../data/{get_today_iso()}_SA_full.csv", index = False)

grouped_df = master_df.groupby(['date', 'source']).mean(numeric_only = True).reset_index()
new_labs = []

for row in grouped_df.index:
    val = grouped_df.loc[row, 'chosen_label_val']

    if val >= 0.1:
        new_labs.append('positive')
    elif val <= -0.1:
        new_labs.append('negative')
    else:
        new_labs.append('neutral')

### WRITING DAILY GROUPED DF TO CSV
grouped_df['chosen_label'] = new_labs
grouped_df.to_csv(f"../data/{get_today_iso()}_SA_grouped.csv", index = False)