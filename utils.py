import nltk
from nltk.corpus import stopwords
import re

#GPT-authored function to remove non-letter
#characters from a string
def remove_non_letters(text):
    return re.sub(r'[^a-zA-Z\s]', '', text)

# Function to ensure required NLTK resources are available
def get_nltk_resources_in(nltk_data_dir):
    try:
        # Attempt to load nltk recources
        stop_words = set(stopwords.words('english'))
        
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        print("Downloading required NLTK resources...")
        #if failure, then download them
        #in a custom directory, sif it is given
        if len(nltk_data_dir)>0:
            nltk.download('stopwords', download_dir=nltk_data_dir)
            nltk.download('punkt', download_dir=nltk_data_dir)
            nltk.download('punkt_tab', download_dir=nltk_data_dir)
        #if no directory is given,
        #then download in a standard directory
        else:
            nltk.download('stopwords')
            nltk.download('punkt')
            nltk.download('punkt_tab')
        # Reload after downloading
        stop_words = set(stopwords.words('english'))