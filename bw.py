import requests
from bs4 import BeautifulSoup
import random
import cloudscraper
import time
from ebooklib import epub

get_chapter_content_list =  []
get_novel_title = ""
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

# def get_proxy():
#     url = "https://www.free-proxy-list.net/"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     proxy_list = []
#     for row in soup.find("table", {"id": "proxylisttable"}).find_all("tr")[1:]:
#         columns = row.find_all("td")
#         ip = columns[0].text
#         port = columns[1].text
#         proxy_list.append(f"http://{ip}:{port}")

#     print(proxy_list)
#     # proxies = response.text.split("\r\n")
#     # proxies = ["http://" + proxy for proxy in proxies if proxy]
#     proxy = random.choice(proxy_list)
#     proxy_dict = {"http": proxy, "https": proxy}
#     print(proxy_dict)
#     return proxy_dict
def novel_url(input):
    search_url = f"https://novelbin.me/search?keyword=" + "+".join(input.split(" "))
    return search_url



def get_response_and_content(url):
    
    retries = 6
    try:
        scraper = cloudscraper.create_scraper()
        # proxy_dict = get_proxy()
        response = scraper.get(url)
        if response.status_code == 200:
            print(f"Everything is working fine. response code - {response.status_code}")
            soup = BeautifulSoup(response.text,"html.parser")

        elif response.status_code == 429:
            print("429 elif")
            for i in range(5):
                header = random.choice(headers)
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
def get_chapter_content(url):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    soup = BeautifulSoup(response.text,"html.parser")
    global novel_title
    novel_title = soup.find("div",class_ ="novel-title")

    chapter_content = soup.find("div",class_ = "chr-c")
    novel_text = "\n".join([p.text for p in chapter_content.find_all("p")])

    global chapter_content_list
    get_chapter_content_list.append(chapter_content)
    return chapter_content
def get_homepage_url(search_url):
    soup = get_response_and_content(search_url)
    
    homepage_url = soup.find("h3",class_="novel-title")

    homepage_url = homepage_url.find("a")["href"]
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


# def chap_list(homepage_url):
#     soup = get_response_and_content(homepage_url)
#     chap_list = soup.find_all("a",href = True)
#     print(chap_list)

def create_epub(novel_title, chapters):
    book = epub.EpubBook()

    # Set metadata
    book.set_identifier('000001')
    book.set_title(novel_title)
    book.set_language('en')
    book.add_author('Unknown')

    epub_chapter =  []

    for i ,(title,content) in enumerate(chapters):
        chapter = epub.EpubHtml(title=title, file_name=f'chap_{i+1}.xhtml', lang='en')
        chapter.content = f"<h1>{title}</h1><p>{content}</p>"
        book.add_item(chapter)
        epub_chapter.append(chapter)

    book.toc = epub_chapter

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ['nav'] + epub_chapter
    epub.write_epub(f"{novel_title}.epub", book,{})
    print("epud created successfully")

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
    get_chapter_content(temp_chap)

    temp_chap = prev_chap(temp_chap)
create_epub(novel_title=novel_title,chapters=get_chapter_content_list[::-1])

stop_time = time.time()
print(f"Total time elapsed is {(stop_time - start_time)//60} minutes and {(stop_time -start_time)%60} seconds")
