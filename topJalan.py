import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidElementStateException
import csv
import re
from urllib.parse import urljoin
import libJalan as jln

debug = 0
temp =[]
result = []
links = []

# get all links from top page  (47 都道府県のリンク)  

url  = "https://www.jalan.net/theme/mikakugari/"
r   = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

for link in soup.find_all('a'):
    links.append(link.get('href'))

absolute_links = [urljoin(url, link) for link in links]

filterd_links = []

numOfLinks = len(absolute_links)
i = 0
while (i < numOfLinks):
  url = absolute_links[i] 
  if ("https" in url) and ('theme/mikakugari/mikakugari/' in url) and ("html" in url):
    filterd_links.append(absolute_links[i])
  i = i + 1

prefecture_url = filterd_links # Now get 47 prefectures links

#######################################################################################
############### next step.....   get facility links from one prefectures one by one
#######################################################################################
all_facility = []
i = 0
while ( i < len(prefecture_url)):
  obj_facility_links = jln.MikakugariScraper(prefecture_url[i])
  facility_links = obj_facility_links.get_links()
  all_facility.append(facility_links)

  i = i + 1


all_facility = jln.flatten(all_facility)  ## get ALL facility link from all 47th prefectures

#######################################################################################
############### FINAL step.....  facility name |  address |  phone number 
#######################################################################################

i = 0
result = []
while (i < len(all_facility)):
  obj_r = jln.FacilityScraper(all_facility[i])
  obj_r.scrape()
  temp = obj_r.get_facility_info()
  result.append(temp)
  i = i + 1

#######################################################################################
############### Last  output into csvFile
#######################################################################################
# CSVファイルに書き込む
with open('outputJalan.csv', 'w', encoding='utf-8', newline='\n') as f:
    writer = csv.writer(f)
    for row in result:
        writer.writerow(row[0])

