# from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


# Final Cosine similarity
import re
import numpy as np
from nltk.corpus import stopwords

# class TFIDFVectorizer:
#     def __init__(self, documents):
#         self.documents = documents
#         self.stop_words = set(stopwords.words('english'))
#         self.vocab = self.build_vocab()
#         self.idf = self.calculate_idf()

#     def build_vocab(self):
#         vocab = set()
#         for doc in self.documents:
#             words = [re.sub(r'[^\w\s]', '', word.lower()) for word in doc.split() if word.lower() not in self.stop_words]
#             vocab.update(words)
#         return sorted(vocab)

#     def calculate_tf(self, document): #term-frequency
#         tf = {}
#         words = [re.sub(r'[^\w\s]', '', word.lower()) for word in document.split() if word.lower() not in self.stop_words]
#         word_count = len(words)
#         for word in words:
#             tf[word] = tf.get(word, 0) + 1 / word_count
#         return tf

#     def calculate_idf(self): #inverse document frequency
#         idf = {}
#         num_documents = len(self.documents)
#         for word in self.vocab:
#             word_count = sum(1 for doc in self.documents if word.lower() in doc.lower())
#             idf[word] = np.log(num_documents / (word_count + 1))
#         return idf

#     def transform(self, document):
#         tfidf_vector = [0] * len(self.vocab)
#         tf = self.calculate_tf(document)
#         for i, word in enumerate(self.vocab):
#             if word.lower() in tf:
#                 tfidf_vector[i] = tf[word.lower()] * self.idf[word]
#         return np.array(tfidf_vector)

# def cosine_similarity(vec1, vec2):
#     dot_product = np.dot(vec1, vec2)
#     norm_vec1 = np.linalg.norm(vec1)
#     norm_vec2 = np.linalg.norm(vec2)
#     if norm_vec1 != 0 and norm_vec2 != 0:
#         return dot_product / (norm_vec1 * norm_vec2)
#     else:
#         return 0  

import re
import numpy as np

from nltk.corpus import stopwords

import json
import re



class SimpleStemmer:
    def __init__(self):
        self.suffixes = {
            1: ["s", "t", "y"],
            2: ["ed", "er", "ly"],
            3: ["ing", "ize", "ate"],
            4: ["tion", "sion", "ment"]
        }

    def stem(self, word):
        for length, suff_list in self.suffixes.items():
            for suffix in suff_list:
                if word.endswith(suffix):
                    return word[:-length]
        return word

class TFIDFVectorizer:
    def __init__(self, documents):
        self.documents = documents
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = SimpleStemmer()
        self.vocab = self.build_vocab()
        self.idf = self.calculate_idf()

    def build_vocab(self):
        vocab = set()
        for doc in self.documents:
            words = [self.stemmer.stem(re.sub(r'[^\w\s]', '', word.lower())) for word in doc.split() if word.lower() not in self.stop_words]
            vocab.update(words)
        return sorted(vocab)

    def calculate_tf(self, document): #term-frequency
        tf = {}
        words = [self.stemmer.stem(re.sub(r'[^\w\s]', '', word.lower())) for word in document.split() if word.lower() not in self.stop_words]
        word_count = len(words)
        for word in words:
            tf[word] = tf.get(word, 0) + 1 / word_count
        return tf

    def calculate_idf(self): #inverse document frequency
        idf = {}
        num_documents = len(self.documents)
        for word in self.vocab:
            word_count = sum(1 for doc in self.documents if self.stemmer.stem(word.lower()) in [self.stemmer.stem(w) for w in doc.lower().split()])
            idf[word] = np.log(num_documents / (word_count + 1))
        return idf

    def transform(self, document):
        tfidf_vector = [0] * len(self.vocab)
        tf = self.calculate_tf(document)
        for i, word in enumerate(self.vocab):
            if self.stemmer.stem(word.lower()) in tf:
                tfidf_vector[i] = tf[self.stemmer.stem(word.lower())] * self.idf[word]
        return np.array(tfidf_vector)

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    if norm_vec1 != 0 and norm_vec2 != 0:
        return dot_product / (norm_vec1 * norm_vec2)
    else:
        return 0

    
def cosine_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    if norm_v1 != 0 and norm_v2 != 0:
        return dot_product / (norm_v1 * norm_v2)
    else:
        return 0