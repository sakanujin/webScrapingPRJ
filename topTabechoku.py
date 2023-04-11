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
#import libJalan as jln

def get_phone_number(url):
    """指定したURLのページから電話番号を取得する"""
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # 電話番号を含むa要素を探す
    tel_links = soup.find_all("a", href=re.compile(r"tel:"))
    if len(tel_links) > 0:
        # a要素のhref属性から最初の電話番号を抽出
        tel_href = tel_links[0]["href"]
        phone_number = re.sub(r"tel:", "", tel_href)
        return phone_number
    else:
        return ""


# At 1st, get all links from top page of food producer
url  = "https://www.tabechoku.com/producers"
r   = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

producers = []
producer_list = soup.find_all('li', {'class': 'item-wrap'})

for producer in producer_list:
    name = producer.find('h4', {'class': 'producer-name'}).text
    address = producer.find('p', {'class': 'producer-area'}).text
    producers.append([name, address])

################## 2nd webdriver and page transition 
#driver = webdriver.Chrome()

i = 2
while ( i < 128):
  pgNum =  str(i)
  url = 'https://www.tabechoku.com/producers?page=' + pgNum
  print(url)
  r   = requests.get(url)
  soup = BeautifulSoup(r.text, "html.parser")

  producer_list = soup.find_all('li', {'class': 'item-wrap'})

  for producer in producer_list:
    name = producer.find('h4', {'class': 'producer-name'}).text
    address = producer.find('p', {'class': 'producer-area'}).text
    producers.append([name, address])

  i += 1

delDuplicateProducer = list(set(tuple(x) for x in producers))
producers = [list(x) for x in delDuplicateProducer]

###############################   get tellephone number #####
query = producers

i=0 
#while ( i < len(query)): 
while ( i < 250): 
  try:
    url = "https://www.google.com/search?q=" + query[i][0] + query[i][1]
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    search_results = soup.find_all("a", href=re.compile(r"(?<=/url\?q=)(htt.*://.*)"))
    for result in search_results:
      url = re.findall(r"(?<=/url\?q=)(htt.*://.*)", result["href"])[0]
      if "google" not in url and "youtube" not in url:
        phone_number = get_phone_number(url)
        print("number :", i, query[i][0],  query[i][1], phone_number, url)
        #print("search result :",search_result) 
        query[i].append(phone_number)
        query[i].append(url)
      break;
  except:
      pass


  i = i + 1


########################################## create csv file
with open('tabechoku_list.csv', mode='w', newline = '\n', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(query)

