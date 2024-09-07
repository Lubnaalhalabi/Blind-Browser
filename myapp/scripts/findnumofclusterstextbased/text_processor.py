import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re

# Class to preprocess text
class TextProcessor:
    def preprocess_text(self, text):
        text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
        text = re.sub(r'\W+', ' ', text)  # Remove non-word characters
        text = re.sub(r'\d+', '', text)   # Remove digits
        text = text.lower()  # Convert to lowercase
        stop_words = set(stopwords.words('english'))
        text = ' '.join(word for word in text.split() if word not in stop_words)
        ps = PorterStemmer()
        text = ' '.join(ps.stem(word) for word in text.split())
        return text