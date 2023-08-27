import requests
from bs4 import BeautifulSoup

def get_cbc_headlines():
    """
    Retrieves the latest headlines from the CBC News website.
    
    Returns:
        list or None: A list of tuples, each containing the headline text and its URL.
                     Returns None if an error occurs during retrieval.
    """
    url = "https://www.cbc.ca/news"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            links = soup.find_all("a")
            cbc_headlines = []
            for link in links:
                headline = link.h3
                href = link['href']
                if headline and href:
                    cbc_headlines.append((headline.text, "https://www.cbc.ca" + href))
        else:
            cbc_headlines = None
    except Exception as e:
        cbc_headlines = None
        print(f"ERROR: {e}")
    return cbc_headlines

def get_ctv_headlines():
    """
    Fetches the latest headlines from the CTV News Canada section.
    
    Returns:
        list or None: A list of tuples, each containing the headline text and its URL.
                     Returns None if an error occurs during retrieval.
    """
    url = "https://www.ctvnews.ca/canada"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            links = soup.find_all("h3", attrs={'class': 'c-list__item__title'})
            ctv_headlines = []
            for link in links:
                if link.a:
                    href = link.a['href'].strip()
                    text = link.a.text.strip()
                    if text and href:
                        ctv_headlines.append((text, href))
        else:
            ctv_headlines = None
    except Exception as e:
        ctv_headlines = None
        print(f"ERROR: {e}")
    return ctv_headlines

def get_global_headlines():
    """
    Retrieves the latest headlines from the Global News Canada section.
    
    Returns:
        list or None: A list of tuples, each containing the headline text and its URL.
                     Returns None if an error occurs during retrieval.
    """
    url = "https://globalnews.ca/canada/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            links = soup.find_all("a", attrs={'class': 'c-posts__inner'})
            global_headlines = []
            for link in links:
                if link.span:
                    href = link['href'].strip()
                    text = link.span.text.strip()
                    if text and href:
                        global_headlines.append((text, href))
        else:
            global_headlines = None
    except Exception as e:
        global_headlines = None
        print(f"ERROR: {e}")
    return global_headlines