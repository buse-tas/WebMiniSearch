import requests
from bs4 import BeautifulSoup
import nltk
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import Counter
from whoosh.qparser import QueryParser
from whoosh.index import open_dir

# FIX #4: Removed "import pdb" — debug tool should not be in production code

from utils import remove_non_letters
from utils import get_nltk_resources_in

# FIX #5: Removed unused hit_to_dict() function


def get_relevant_links(query_to_parse):

    # FIX #10: Use environment variable for NLTK data path instead of hardcoded server path
    nltk_data_dir = os.environ.get('NLTK_DATA_DIR', '')
    get_nltk_resources_in(nltk_data_dir)

    stop_words = set(stopwords.words('english'))

    # open index
    ix = open_dir("indexdir")

    # remove irrelevant characters from query
    query = remove_non_letters(query_to_parse)
    query = query.replace("\n", " ").replace("\r", " ").replace("  ", " ").lower()

    # tokenize query and keep only unique tokens
    query_tokens = set(word_tokenize(query))

    # stem tokens and remove stop words
    ps = PorterStemmer()
    query_tokens_without_stop_words = [
        ps.stem(token) for token in query_tokens if token not in stop_words
    ]

    relevant_links = []

    # FIX #6: Open index searcher once outside the loop for better performance
    with ix.searcher() as searcher:
        for token in query_tokens_without_stop_words:
            whoosh_query = QueryParser("content", ix.schema).parse(token)
            results = searcher.search(whoosh_query)

            for r in results:
                r_to_dict = dict(r)
                if r_to_dict not in relevant_links:
                    relevant_links.append(r_to_dict)

    return relevant_links
