import re
import numpy as np
from nltk.corpus import stopwords

class TFIDFVectorizer:
    def __init__(self, documents):
        self.documents = documents
        self.stop_words = set(stopwords.words('english'))
        self.vocab = self.build_vocab()
        self.idf = self.calculate_idf()

    def build_vocab(self):
        vocab = set()
        for doc in self.documents:
            words = [re.sub(r'[^\w\s]', '', word.lower()) for word in doc.split()]
            vocab.update(words)
        return sorted(vocab)

    def calculate_tf(self, document): #term-frequency
        tf = {}
        words = [re.sub(r'[^\w\s]', '', word.lower()) for word in document.split()]
        word_count = len(words)
        for word in words:
            tf[word] = tf.get(word, 0) + 1 / word_count
        return tf

    def calculate_idf(self): #inverse document frequency
        idf = {}
        num_documents = len(self.documents)
        for word in self.vocab:
            word_count = sum(1 for doc in self.documents if word.lower() in doc.lower())
            idf[word] = np.log(num_documents / (word_count + 1))
        return idf

    def transform(self, document):
        tfidf_vector = [0] * len(self.vocab)
        tf = self.calculate_tf(document)
        for i, word in enumerate(self.vocab):
            if word.lower() in tf:
                tfidf_vector[i] = tf[word.lower()] * self.idf[word]
        return np.array(tfidf_vector)

def cosine_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    if norm_v1 != 0 and norm_v2 != 0:
        return dot_product / (norm_v1 * norm_v2)
    else:
        return 0 
    

class CountVectorizer:
    def __init__(self, documents):
        self.documents = documents
        self.vocab = self.build_vocab()

    def build_vocab(self):
        vocab = set()
        for doc in self.documents:
            words = doc.replace(",", "").split()
            vocab.update(words)
        return sorted(vocab)

    def transform(self, document):
        count_vector = [0] * len(self.vocab)
        words = document.split()
        for word in words:
            if word in self.vocab:
                index = self.vocab.index(word)
                count_vector[index] += 1
        return np.array(count_vector)

class OneHotEncoder:
    def __init__(self, categories):
        self.categories = categories
        self.category_to_index = {category: i for i, category in enumerate(categories)}

    def transform(self, category):
        one_hot_vector = [0] * len(self.categories)
        for cat in category.split(', '):
            if cat in self.categories:
                index = self.category_to_index[cat]
                one_hot_vector[index] = 1
        return np.array(one_hot_vector)