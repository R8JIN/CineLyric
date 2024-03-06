import re
from collections import Counter
from nltk.corpus import stopwords

class CountVectorizer:
    def __init__(self):
        self.vocab = {}
        self.index_to_word = []
        self.stop_words = set(stopwords.words('english'))
    
    def fit_transform(self, documents):
        self._build_vocab(documents)
        return self._transform(documents)
    
    def _build_vocab(self, documents):
        words = set()
        for doc in documents:
            words.update(self._tokenize(doc))
        
        self.vocab = {word: index for index, word in enumerate(sorted(words))}
        self.index_to_word = [word for word, _ in sorted(self.vocab.items(), key=lambda x: x[1])]
    
    def _transform(self, documents):
        matrix = []
        for doc in documents:
            word_counts = Counter(self._tokenize(doc))
            vector = [word_counts[word] for word in self.index_to_word]
            matrix.append(vector)
        return matrix
    
    def _tokenize(self, text):
        if isinstance(text, list):  # Check if input is a list
            text = ' '.join(text)  # If list, concatenate elements into a single string
        text = re.sub(r'[^\w\s]', '', text.lower())  # Remove symbols and convert to lowercase
        tokens = [word for word in text.split() if word not in self.stop_words]
        return tokens
