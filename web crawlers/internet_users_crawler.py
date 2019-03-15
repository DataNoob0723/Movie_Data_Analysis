# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 12:48:44 2019

@author: Zeyu Yan
"""

import requests
import pandas as pd
from lxml import etree

title_list = [
        "Rank",
        "Country",
        "Internet Users (2016)",
        "Penetration (% of Pop)",
        "Population (2016)",
        "Non-Users (internetless)",
        "Users 1 Year Change (%)",
        "Internet Users 1 Year Change",
        "Population 1 Year Change",
        ]

df_dict = dict()
for title in title_list:
    df_dict[title] = []

base_url = "http://www.internetlivestats.com/internet-users-by-country/"
ua_header = {"User-Agent" : "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1 Trident/5.0;"}
html = requests.get(base_url, headers=ua_header).text
selector = etree.HTML(html)

row = 1
crawl = True

while crawl == True:
    try:
        for i in range(len(title_list)):
            if i == 1:
                df_dict[title_list[i]].append(str(selector.xpath(f'//*[@id="example"]/tbody/tr[{row}]/td[{i + 1}]/a/text()')[0]))
            else:
                df_dict[title_list[i]].append(str(selector.xpath(f'//*[@id="example"]/tbody/tr[{row}]/td[{i + 1}]/text()')[0]))
    except:
        crawl = False
    row += 1

df = pd.DataFrame(df_dict).set_index("Rank")

output_data_file = "csv_files/internet_users_data_2016.csv"
df.to_csv(output_data_file)
    