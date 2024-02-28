import math
import numpy as np

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