# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 12:17:31 2019

@author: Zeyu Yan
"""

import requests
import pandas as pd
from api_config import OMDB_API_key_2

original_df = pd.read_csv("csv_files/marvel_movies_data.csv")
#print(original_df.head())

titles = list(original_df ["Title"])
#print(titles)
titles[2] = "The Avengers"


base_url = "http://www.omdbapi.com/"
first_title = titles[0]
payloads = {
        "t": first_title,
        "apikey": OMDB_API_key_2,
        }
response = requests.get(base_url, params=payloads)
response_json = response.json()

keys_list = list(response_json.keys())

data_dict = dict()
for key in keys_list:
    data_dict[key] = []

for title in titles:
    payloads = {
            "t": title,
            "apikey": OMDB_API_key_2,
            }
    response = requests.get(base_url, params=payloads)
    response_json = response.json()
    for key in data_dict.keys():
        try:
            value = response_json[key]
        except:
            value = "N/A"
        data_dict[key].append(value)

df = pd.DataFrame(data_dict)
output_data_file = "csv_files/marvel_details_data.csv"
df.to_csv(output_data_file)