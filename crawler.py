import requests
from bs4 import BeautifulSoup
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from collections import Counter
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, STORED
from whoosh.analysis import StemmingAnalyzer

# FIX #7: OpenAI import uncommented so Response_Generator class doesn't cause NameError
# If you don't have a valid API key, keep the class but don't instantiate it
from openai import OpenAI

from utils import remove_non_letters
from utils import get_nltk_resources_in


# this one is not used since there is no valid api key
class Response_Generator:
    def __init__(self, api_key):
        self.model = OpenAI(api_key=api_key)

    def get_a_response(self, prompt, desired_temperature=1.1, max_response_length=200):
        chat_completion = self.model.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user",
                 "content": prompt
                }
            ],
            temperature=desired_temperature,
            max_tokens=max_response_length
        )
        return chat_completion.choices[0].message.content


get_nltk_resources_in("")
stop_words = set(stopwords.words('english'))


# set the website to be crawled
url_prefix_of_the_crawled_website = 'https://vm009.rz.uos.de/crawl/'
# set the initial web page for the crawler
start_url = url_prefix_of_the_crawled_website + 'index.html'

# push the initial web page url to the list of urls to be visited by the crawler
agenda = [start_url]
# initialize the list of visited links
visited_links = []

# initialize the index schema with 4 attributes/columns
schema = Schema(
    title=TEXT(stored=True, field_boost=2.0),
    page_url=STORED,
    content=TEXT(analyzer=StemmingAnalyzer()),
    content_summary=STORED
)

# create an index instance with a given schema
ix = create_in("indexdir", schema)
writer = ix.writer()

# while there are still links to be visited
while agenda:
    url = agenda.pop()
    visited_links.append(url)
    print("Get ", url)

    r = requests.get(url)

    if r.status_code == 200:

        soup = BeautifulSoup(r.content, 'html.parser')

        list_of_all_links_on_a_page = soup.find_all('a')
        for href in list_of_all_links_on_a_page:
            if href.get('href'):
                if url_prefix_of_the_crawled_website in href.get('href'):
                    link = href.get('href')
                else:
                    link = url_prefix_of_the_crawled_website + href.get('href')
                if not link in visited_links and not link in agenda:
                    agenda.append(link)

        # get page title
        page_title = "Untitled page"
        if soup.title:
            page_title = soup.title.text

        # leave head- and a-tags out of consideration
        for a in soup.find_all('a'):
            a.decompose()
        for head in soup.find_all('head'):
            head.decompose()

        # FIX #8: Use re.sub to properly collapse all whitespace (not just double spaces)
        page_text = re.sub(r'\s+', ' ', soup.get_text()).strip().lower()

        writer.add_document(title=page_title, page_url=url, content=page_text, content_summary=page_text)

        print("_________________________________________________________________")

# save crawling results
writer.commit()
