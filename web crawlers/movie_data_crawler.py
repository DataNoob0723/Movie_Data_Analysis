# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 18:41:49 2019

@author: Zeyu Yan
"""

import requests
import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup
from api_config import OMDB_API_key_2
from tqdm import tqdm

final_dict = dict()

year_tableStartNum_dict = {
        "2018": 7,
        "2017": 6,
        "2016": 7,
        "2015": 8,
        "2014": 7,
        }

month_list = [
        "January–March",
        "April–June",
        "July–September",
        "October–December",
        ]

ua_header = {"User-Agent" : "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1 Trident/5.0;"}


def get_table_summary(table):
    h3 = table.find_previous_sibling('h3')
    table_name = 'NA'
    if h3 is not None:
        table_name = h3.get_text()
    trs = table.select('tbody tr')
    num_trs = len(trs)
    return table_name, num_trs


for year, table_start_num in year_tableStartNum_dict.items():
    url = f"https://en.wikipedia.org/wiki/{year}_in_film"
    response = requests.get(url, headers=ua_header)
    html = response.text
    
    soup = BeautifulSoup(html, 'html.parser')
    
    tables = soup.select('table.wikitable.sortable')
    
    rows_dict = dict()
    
    for table in tables:
        table_name, num_rows = get_table_summary(table)
        for month in month_list:
            if month in table_name:
                rows_dict[month] = num_rows
    
    selector = etree.HTML(html)
    name_list = []
    
    table_num = table_start_num - 1
    
    for month, num_rows in rows_dict.items():
        table_num += 1 
        row = 2
        while row <= num_rows:
            try:
                col = 2
                name = str(selector.xpath(f'//*[@id="mw-content-text"]/div/table[{table_num}]/tbody/tr[{row}]/td[{col}]/i/a/text()')[0])
            except:
                pass
            
            try:
                col = 1
                name = str(selector.xpath(f'//*[@id="mw-content-text"]/div/table[{table_num}]/tbody/tr[{row}]/td[{col}]/i/a/text()')[0])
            except:
                pass
            
            try:
                col = 2
                name = str(selector.xpath(f'//*[@id="mw-content-text"]/div/table[{table_num}]/tbody/tr[{row}]/td[{col}]/i/text()')[0])
            except:
                pass
            
            try:
                col = 1
                name = str(selector.xpath(f'//*[@id="mw-content-text"]/div/table[{table_num}]/tbody/tr[{row}]/td[{col}]/i/text()')[0])
            except:
                pass
            
            if len(name) > 0:
                if name not in name_list:
                    name_list.append(name)
            
            row = row + 1
            print(f"Crawled a name from {year}.")
    
    final_dict[year] = name_list

# Check final_dict
for key, value in final_dict.items():
    print(key)
    print(value)
    print(len(value))
    print("--------------------------")
    print()


# Gather data through OMDB API
year = input("What year of movie data you want please? (2014 to 2018)")

movie_list = final_dict[year]
name = movie_list[0]

base_url = "http://www.omdbapi.com/"
payloads = {
        "t": name,
        "apikey": OMDB_API_key_2,
        }

response = requests.get(base_url, params=payloads)
response_json = response.json()

keys_list = list(response_json.keys())

data_dict = dict()
for key in keys_list:
    data_dict[key] = []
    
for name in tqdm(movie_list):
    payloads = {
            "t": name,
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
print(df.head())

output_data_file = f"csv_files/{year}_movies_data.csv"
df.to_csv(output_data_file)