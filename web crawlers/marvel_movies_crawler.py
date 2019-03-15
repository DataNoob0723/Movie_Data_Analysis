# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 20:10:13 2019

@author: Zeyu Yan
"""

import requests
import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup

base_url = "https://www.boxofficemojo.com"
extract_url = base_url + "/movies/?"
replace_url = extract_url + "page=intl&"
start_url = "https://www.boxofficemojo.com/franchises/chart/?id=avengers.htm"
ua_header = {"User-Agent" : "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1 Trident/5.0;"}

start_html = requests.get(start_url, headers=ua_header).text
start_selector = etree.HTML(start_html)

row = 2
crawl = True

while crawl == True:
    try:
        movie_title = str(start_selector.xpath(f'//*[@id="body"]/table[2]/tr/td[1]/table/tr/td/table[1]/tr[{row}]/td[2]/font/a/b/text()')[0])
        valid_movie_title = movie_title.replace(": ", " ")
        print(valid_movie_title)
        new_url = base_url + str(start_selector.xpath(f'//*[@id="body"]/table[2]/tr/td[1]/table/tr/td/table[1]/tr[{row}]/td[2]/font/a/@href')[0])
        print(new_url)
        valid_url = new_url.replace(extract_url, replace_url)
        print(valid_url)
        valid_html = requests.get(valid_url, headers=ua_header).text
        soup = BeautifulSoup(valid_html, 'html.parser')
        tr = soup.select('td[valign="top"] table tr[bgcolor="#dcdcdc"]')[0]
        trs = [repr(sib) for sib in tr.next_siblings]
        data = []
        for tr in trs:
            tr = BeautifulSoup(tr, 'html.parser')
            tds = tr.select('td')
            tds = [td.get_text() for td in tds]
            data.append(tds)
        df = pd.DataFrame(data)
        df = df.dropna()
        df.reset_index(drop=True, inplace=True)
        df = df.drop([0])
        df.reset_index(drop=True, inplace=True)
        df.columns = ["Country", "Dist.", "Release Date", "Opening Wknd", "% of Total", "Total Gross", "As of"]
        output_data_file = f"csv_files/Marvel_Global_Box_Office/{valid_movie_title}_global_box_office.csv"
        df.to_csv(output_data_file)
    except:
        crawl = False
    row += 1
