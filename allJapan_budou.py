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

debug = 0
temp =[]
result = []
kbrDelResult  = []
phone_list = []
new_result = []


url = "https://www.mapple.net/sp/budogari/"
r   = requests.get(url)

soup = BeautifulSoup(r.text, "html.parser")

links = []
result = []
for link in soup.find_all('a'):
    links.append(link.get('href'))


numOfLinks = len(links)

i = 0
while (i < numOfLinks):
  url = links[i] 
  if ("http" in url) and ("budogari" in url) and ("www" in url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    facility_list = soup.select('section.post_body h2')
    address_list = soup.select('section.post_body dd:nth-of-type(1)')

    for facility, address in zip(facility_list, address_list):
      temp = list(zip(facility,address))
      result.extend(temp)
  i = i + 1

result_set = set(tuple(x) for x in result)
#kbrDelResult = [list (x) for x in result_set]
result2 = [list (x) for x in result_set]

#result2 =  [[t] for t in kbrDelResult[0]]

i = 0
while (i < len(result2)):
  print(result2[i])
  i = i+1

################# upto here all OK ###################################
options = Options()
options.add_argument('--headless')
#driver = webdriver.Chrome(chrome_options=options)
driver = webdriver.Chrome()
driver.get("http:/www.google.com")
print("result2  length is ",  len(result2))

i = 0
while(i < len(result2)):
  print("LOOP START", i)
  #search_box = driver.find_element_by_name('q')
  search_box = driver.find_element(By.NAME, 'q')

  try:
    search_box.clear()
    search_box.send_keys(str(result2[i][0]) + '  ' + str(result2[i][1]))
    search_box.send_keys(Keys.RETURN)
    search_result_url = driver.current_url
  except InvalidElementStateException:
    pass


  html2 = requests.get(search_result_url).text
  soup2 = BeautifulSoup(html2, 'html.parser')


  match = re.search(r'電話.+?>(0\d{1,4}-)?\d{1,4}-\d{4}<', str(soup2))
  if match:
      text = match.group(0)
      match   = re.search(r'(\d{2,4}-\d{2,4}-\d{4})', text)
      if match:
        phone_number = match.group(1)
        phone_list.append ( phone_number)
        print ( phone_number)


      else:
        phone_list.append ("no number")
        print("I am sorry, no number found")

  else:
    phone_list.append ("no number")
    print("I am sorry, no number")

  i = i + 1


############################## end loop ###########
## new loop
i = 0
while (i < len(result2)):
    try:
      new_result.append(result2[i] + [phone_list[i]])
    except IndexError as e:
      print("IndexError is occured ", e)

    i = i +1

print(new_result)
print("length is  :", len(new_result))

outCsvFile = 'budou_facility.csv'
############################## Create CSV file ###########
if os.path.exists(outCsvFile):
  os.remove(outCsvFile)


#with open('budou_facility.csv', 'w', newline='\r\n') as csvfile:
#with open('budou_facility.csv', 'w') as csvfile:
with open(outCsvFile, 'w', newline='\n') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(new_result)

    #for i in range(len(new_result)):
    #  for j in range(len(new_result[i])):
    #    writer.writerow(new_result [i][j])











