import requests
from bs4 import BeautifulSoup
import random
import cloudscraper
import time

start_time = time.time()
headers = [
{
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive",
},
{
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/119.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.bing.com/",
    "DNT": "1",
    "Connection": "keep-alive",
},
{
    "User-Agent": "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "https://www.google.com/",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
},
{
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "https://duckduckgo.com/",
    "DNT": "1",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
},
{
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "https://www.google.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}
]

session = requests.Session()
header = random.choice(headers)

def novel_url(input):
    search_url = f"https://novelbin.me/search?keyword=" + "+".join(input.split(" "))
    return search_url



def get_response_and_content(url):
    retries = 6
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url)
        if response.status_code == 200:
            print(f"Everything is working fine{response.status_code}")
        elif response.status_code == 429:
            print("429 elif")
            for i in range(5):
                print("429 for loop")
                time.sleep(random.uniform(1.0,5.0))
                response = scraper.get(url)
                if not response:
                    print("429 nest if not")
                    continue
                    
                else:
                    print("429 nested else")
                    break
        else:
            print(f"RESPONSE CODE{response.status_code}")
    #     if response.status_code != 200:
        
    #         print(f"Failed to fetch {url} (Status Code: {response.status_code})")
    #         for i in range(1,retries) :
    #             print(f"Retrying times {i} ")
    #             response = scraper.get(url)
    #             if response.status_code == 200:
    #                 soup = BeautifulSoup(response.text,"html.parser")
    #                 return soup
    #             else:
    #                 continue
    except ConnectionError:
        print("connect reset error")
        response = scraper.get(url)

    soup = BeautifulSoup(response.text,"html.parser")
    return soup


def get_homepage_url(search_url):
    soup = get_response_and_content(search_url)
    
    homepage_url = soup.find("h3",class_="novel-title")
    print(homepage_url)
    homepage_url = homepage_url.find("a")["href"]
    print(homepage_url)
    return homepage_url
def get_first_chap_url(home_page_url):
    soup = get_response_and_content(home_page_url)
    first_chap = soup.find("a",class_="btn btn-danger btn-read-now")["href"]
    return first_chap
def get_next_chap_url(url):
    soup = get_response_and_content(url)
    next_chap = soup.find("a",id="next_chap")["href"]
    return next_chap
def latest_chap(search_url):
    soup = get_response_and_content(search_url)
    # latest_chap_title = soup.find("span",class_="chr-text chapter-title").text
    # print(latest_chap_title)
    # latest_chap_url = soup.find("div").find_all("a",href=True)
    novel_links = [a["href"] for a in soup.find_all("a", href=True) if "/novel-book/" in a["href"]]
    latest_chap_url = novel_links[1]
    return latest_chap_url

def prev_chap(chap_url):
    soup = get_response_and_content(chap_url)
    try:
        prev_chap = soup.find("a",id="prev_chap")["href"]


    except :
        return
    return prev_chap


def chap_list(homepage_url):
    soup = get_response_and_content(homepage_url)
    chap_list = soup.find_all("a",href = True)
    print(chap_list)



serch_word = input("Enter : ")
search_url = novel_url(serch_word)
print(search_url)


homepage_url = get_homepage_url(search_url=search_url)
# print(f"Homepage of the novel is {homepage_url}")
# first_chap = get_first_chap_url(homepage_url)
# print(first_chap)
latest_chap_url = latest_chap(search_url)
temp_chap = latest_chap_url
while temp_chap:
    print(temp_chap)
    temp_chap = prev_chap(temp_chap)
    
stop_time = time.time()
print(f"Total time elapsed is {(stop_time - start_time)//60} minutes and {(stop_time -start_time)%60} seconds")
