import git
import pandas as pd
from dateutil import parser
from datetime import date
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from tqdm import tqdm
import numpy as np
from scipy.special import softmax
from scraping import *
from transformers import AutoTokenizer, AutoConfig, AutoModelForSequenceClassification
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
print()
from general_funcs import *

### Scraping all headlines -- from scraping.py

cbc_headlines = get_cbc_headlines()
ctv_headlines = get_ctv_headlines()
global_headlines = get_global_headlines()
print()

### used to prompt the SA model
def sa_model(headline: str):
    encoded_input = tokenizer(headline, return_tensors = 'pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    ranking = np.argsort(scores)
    ranking = ranking[::-1]

    results = {}

    for i in range(scores.shape[0]):
        l = config.id2label[ranking[i]]
        s = scores[ranking[i]]
        results[l] = s

    return results

def sa_headlines(headlines_urls: list, source: str = None):
    """
    Performs Sentiment Analysis (SA) on a list of headlines and returns a dictionary 
    containing the results and other associated data.

    Args:
        headlines_urls (list): A list of tuples where each tuple consists of two elements:
                               1) A headline as a string 
                               2) The corresponding URL as a string
        source (str, optional): The source or origin of the headlines. Defaults to None.

    Returns:
        dict: A dictionary containing the following keys:
              - 'source': List of sources for each headline.
              - 'date': List of dates when each SA was performed.
              - 'headline': List of the provided headlines.
              - 'url': List of URLs corresponding to each headline.
              - 'chosen_label': List of chosen sentiment labels based on the analysis.
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

    responses_dict = {
        'source' : [],
        'date' : [],
        "headline" : [],
        'url' : [],
        "chosen_label" : [],
        'positive': [],
        'negative': [],
        'neutral': [],
        'compound' : []
        }

    date = get_today_iso()

    # get rid of any duplicates in headlines list
    headlines_urls = list(set(headlines_urls))

    for head_text, url in tqdm(headlines_urls, desc = source):
  
        # add non-SA things to dict
        responses_dict['source'].append(source.strip())
        responses_dict['date'].append(date.strip())
        responses_dict['headline'].append(head_text.strip())
        responses_dict['url'].append(url)

        # perform SA
        response = sa_model(headline = head_text)

        # add SA results to dict
        for lab, score in response.items():
            responses_dict[lab].append(score)

        # creating compound score from 'negative' and 'positive' and 'neutral' scores
        compound = (responses_dict['positive'][-1] - responses_dict['negative'][-1]) * (1 - responses_dict['neutral'][-1])
        responses_dict['compound'].append(compound)

        # creating SA labels from compound score (a bit more robust than model's labels)
        if compound >= 0.05:
            responses_dict['chosen_label'].append("positive")
        elif compound <= -0.05:
            # responses_dict['chosen_label_val'].append("negative")
            responses_dict['chosen_label'].append('negative')
        else:
            responses_dict['chosen_label'].append("neutral")

    return responses_dict

### Perform SA on all found headlines

# labels = ['positive', 'negative', 'neutral']

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

        sa_results = sa_headlines(headlines_urls = headlines, source = source)

        # just overwrite the whole dict with the first results
        if not master_results:
            master_results = sa_results

        # afterwards, add everything to each list
        else:
            for key, val in sa_results.items():
                master_results[key].extend(val)

master_df = pd.DataFrame(master_results)

# data_dir = "data/"
data_dir = "/Users/kmaurinjones/Desktop/ds/github_repos/DailyNewsDriftCanada/data/"

### WRITING DAILY FULL DF TO CSV
master_df.to_csv(f"{data_dir}{get_today_iso()}_SA_full.csv", index = False)

print(f"Daily full file written to data/ directory")

grouped_df = master_df.groupby(['date', 'source']).mean(numeric_only = True).reset_index()
new_labs = []

for row in grouped_df.index:
    val = grouped_df.loc[row, 'compound']

    if val >= 0.05:
        new_labs.append('positive')
    elif val <= -0.05:
        new_labs.append('negative')
    else:
        new_labs.append('neutral')

### WRITING DAILY GROUPED DF TO CSV
grouped_df['chosen_label'] = new_labs
grouped_df.to_csv(f"{data_dir}{get_today_iso()}_SA_grouped.csv", index = False)

print(f"Daily aggregated file written to data/ directory")

def git_add_commit_push(repo_path, commit_message, remote_name = 'origin', branch = 'main'):
    """
    Add, commit, and push using GitPython.

    Parameters:
    - repo_path: Path to the git repository.
    - commit_message: Commit message.
    - remote_name: The name of the remote (default is 'origin').
    - branch: The branch to push to (default is 'master').
    """

    repo = git.Repo(repo_path)
    
    # Add all changes
    repo.git.add(A=True)

    # Commit
    repo.git.commit(m=commit_message)

    # Push
    origin = repo.remote(name=remote_name)
    origin.push(branch)

    print(f"Repo updated. Commit: '{commit_message}'")

local_repo_path = "/Users/kmaurinjones/Desktop/ds/github_repos/DailyNewsDriftCanada/"

### Current Date + Time Webpage + Commit Messages
from datetime import datetime

def get_current_time_and_date():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")
    return current_date, current_time

date, time = get_current_time_and_date()
# print(f"Last updated: {date} at {time}")

logs_path = "/Users/kmaurinjones/Desktop/ds/github_repos/DailyNewsDriftCanada/logs.txt"

current_logs = [line.strip() for line in open(logs_path, "r").readlines()]
current_logs.append(f"Data last updated: {date}, {time}")

with open(logs_path, "w") as logs_file:
    for line in current_logs:
        logs_file.write(line + "\n")

### commit changes to repo
git_add_commit_push(repo_path = local_repo_path, commit_message = f'Scheduled data update: {date}, {time}')