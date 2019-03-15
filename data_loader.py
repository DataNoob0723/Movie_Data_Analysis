#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 19:01:45 2019

@author: zeyuyan
"""

from sklearn.datasets import load_files
import pickle

# Import data
train_reviews = load_files("imdb_sentiment_data/train/", encoding="utf-8")
text_train, sent_train = train_reviews.data, train_reviews.target

test_reviews = load_files("imdb_sentiment_data/test/", encoding="utf-8")
text_test, sent_test = test_reviews.data, test_reviews.target

# Store data as Pickle files
with open("pickle_data/text_train.pickle", "wb") as f:
    pickle.dump(text_train, f)

with open("pickle_data/sent_train.pickle", "wb") as f:
    pickle.dump(sent_train, f)

with open("pickle_data/text_test.pickle", "wb") as f:
    pickle.dump(text_test, f)

with open("pickle_data/sent_test.pickle", "wb") as f:
    pickle.dump(sent_test, f)



