# Bookmark Recommendation For music
import re
import numpy as np
from collections import Counter
# from nltk.corpus import stopwords

class CountVectorizer:
    def __init__(self):
        self.vocab = {}
        self.index_to_word = []
        # self.stop_words = set(stopwords.words('english'))
    
    def fit_transform(self, documents):
        self._build_vocab(documents)
        return self._transform(documents)
    
    def _build_vocab(self, documents):
        words = set()
        for doc in documents:
            words.update(self._tokenize(doc))
#         print(words)
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
        # Remove symbols and convert to lowercase
        text = re.sub(r'[^\w\s]', '', text.lower())
        # Tokenize the text and remove stop words
        tokens = [word for word in text.split()]
        return tokens


def cosine_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    if norm_v1 != 0 and norm_v2 != 0:
        return dot_product / (norm_v1 * norm_v2)
    else:
        return 0