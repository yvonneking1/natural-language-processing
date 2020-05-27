from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import os

#Codeup Blog Articles

def get_article_title(url):
    """
    takes in url and returns the title of the blog
    """
    headers = {'User-Agent': 'Codeup Data Science'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.text
    return title

def get_article_body(url):
    """
    takes in url and returns the body of the blog
    """
    headers = {'User-Agent': 'Codeup Data Science'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")    
    return soup.find('div', itemprop='text').text

def get_article_dictionary(url):
    """
    takes in a url and using the get_article and get title functions
    returns the blog in a dictionary format
    """
    articles = {"title": get_article_title(url), "content": get_article_body(url)}
    return articles

def dataframe_for_codeup_blog(urls):
    """
    uses a list of urls and loops through each one using the
    get_article_dictionary functions creates a dataframe of the blogs  
    """
    article_dict = []
    for url in urls:
        article_dict.append(get_article_dictionary(url))
    df = pd.DataFrame(article_dict)
    df.to_csv('./codeup_blog_posts.csv')
    return df

def get_codeup_blogs():
    """
    returns a dataframe with the blogs from codeup, 
    creates a csv if one is not present
    """
    filename = "./codeup_blog_posts.csv"

    urls = [
        "https://codeup.com/codeups-data-science-career-accelerator-is-here/",
        "https://codeup.com/data-science-myths/",
        "https://codeup.com/data-science-vs-data-analytics-whats-the-difference/",
        "https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/",
        "https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/",]
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        return dataframe_for_codeup_blog(urls)


# Inshorts news articles

def get_articles_from_topic(url):
    """
    pulls the news articles for inshort specifed url
    """
    headers = {'User-Agent': 'Codeup Data Science'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    output = []

    articles = soup.select(".news-card")

    for article in articles: 
        title = article.select("[itemprop='headline']")[0].get_text()
        body = article.select("[itemprop='articleBody']")[0].get_text()
        author = article.select(".author")[0].get_text()
        published_date = article.select(".time")[0]["content"]
        category = response.url.split("/")[-1]

        article_data = {
            'title': title,
            'body': body,
            'category': category,
            'author': author,
            'published_date': published_date,
        }
        output.append(article_data)


    return output

def make_new_request():
    """
    loops through business, sports, tech, and entertainment articles
    found on inshorts website and creates a dataframe
    and saves articles locally on CSV
    """
    urls = [
        "https://inshorts.com/en/read/business",
        "https://inshorts.com/en/read/sports",
        "https://inshorts.com/en/read/technology",
        "https://inshorts.com/en/read/entertainment"
    ]

    output = []
    
    for url in urls:
        # We use .extend in order to make a flat output list.
        output.extend(get_articles_from_topic(url))
        
    df = pd.DataFrame(output)
    df.to_csv('inshorts_news_articles.csv')
    return df

def get_news_articles():
    """
    checks to see if CSV of articles is saved locally if not will collect
    the data and return a dataframe as well as create the CSV locally
    """
    filename = 'inshorts_news_articles.csv'

    # checks if file exists if not make a new request and creates
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        return make_new_request()