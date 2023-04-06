import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

class MikakugariScraper: ## argument is TodouFuken top url e.g.) 
    def __init__(self, url):
        self.url = url

    def get_links(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, "html.parser")

        # リンクを格納するリスト
        links = []

        # リンクを抽出し、リストに格納する
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                links.append(href)

        # 結果を表示
        ab_links = [urljoin(self.url, link)for link in links]

        filt_links = []
        pattern = r'([0-9]{3}.html)'

        for lk in ab_links:
            if (re.search(pattern, lk))  and (not "#yado" in lk):
                filt_links.append(lk)

        filt_links = list(set(filt_links))

        sorted_urls = sorted(filt_links, key=lambda x: int(x.split("/")[-1].split(".")[0]))

        return sorted_urls   # get all facilities links from each prefecture.

"""  Usage of this class

url = "https://www.jalan.net/theme/mikakugari/mikakugari/01.html"  
scraper = MikakugariScraper(url)
result = scraper.get_links()
print(result)

"""
###################################################################################
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

class FacilityScraper:
    def __init__(self, url):
        self.url = url
        self.facility_name = None
        self.location = None
        self.tel = None

    def scrape(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, "html.parser")
        
        try:
          self.facility_name = soup.find("h1", class_="index_h1").text
          self.location = soup.find('th', text='所在地').find_next_sibling('td').text
          self.tel = soup.find('th', text='問い合わせ先TEL').find_next_sibling('td').text
        except AttributeError:
            print(f"Failed to scrape data from {self.url}")
            return

    def get_facility_info(self):
        return [[self.facility_name, self.location, self.tel]]

"""
# クラスのインスタンスを作成
url = "https://www.jalan.net/theme/mikakugari/mikakugari/001.html"
scraper = FacilityScraper(url)

# データのスクレイピングを実行
scraper.scrape()

# 施設情報を取得
facility_info = scraper.get_facility_info()

# 結果を表示
print(facility_info)
"""

def flatten(lst):
#    多次元のリストを1次元にする関数
    return [item for sublist in lst for item in (flatten(sublist) if isinstance(sublist, list) else [sublist])]


