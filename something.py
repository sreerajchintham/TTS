import requests
from bs4 import BeautifulSoup
import time
import random
from concurrent.futures import ThreadPoolExecutor
class BookWeaver:
    def __init__(self):
        self.novel_chapter_urls = []
        self.header = [
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

        self.novel_input_name = input("Please input the NOVEL NAME: ")
        
        
    def generate_search_url(self):
        search_url_novelbin = "https://novelbin.com/search?keyword="+ "+".join(self.novel_input_name.split(" "))
        print(search_url_novelbin)
        return search_url_novelbin
    def get_url_content(self,given_url):
        
        for attempts in range(5):
            headers = random.choice(self.header)
            response = requests.get(url=given_url,headers=headers)
            if response.status_code == 200:
                
                return response
            
                
            elif response.status_code == 403:
                print(f"Access denied (403) for {given_url}. You might be blocked.")
                return None
            
            elif response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 2))  # Default to 5 seconds
                print(f"Rate limited! Retrying in {retry_after} seconds...")
                time.sleep(retry_after)
                continue

            else:
                wait_time = 2 ** attempts  # Exponential backoff (2, 4, 8, etc.)
                print(f"Error {response.status_code} for {given_url}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                continue
        
        return response
    def get_novel_url(self,search_url):
        response = self.get_url_content(search_url)
        soup = BeautifulSoup(response.text, "html.parser")
        first_search_result = soup.find("h3",class_="novel-title")
        if not first_search_result:
            print(response.text)
            print("Novel Not Found")
            return None
            
        else:
            first_search_result = soup.find("h3",class_="novel-title")
            novel_url = first_search_result.find("a")["href"]
        
        return novel_url
        
    def first_chapter(self,novel_url):
        response = self.get_url_content(novel_url)
        soup = BeautifulSoup(response.text, "html.parser")
        first_chap_url = soup.find("a",title="READ NOW")["href"]
        self.novel_chapter_urls.append(first_chap_url)
        return first_chap_url
    def next_chapter(self,novel_url):
        response = self.get_url_content(novel_url)
        soup = BeautifulSoup(response.text, "html.parser")
        next_chap_url = soup.find("a",id="next-chap")["href"]
        self.novel_chapter_urls.append(next_chap_url)
        print(f"{next_chap_url}")
        return next_chap_url
    def get_chap_content(self,url):
        response = self.get_url_content(url)
        soup = BeautifulSoup(response.text,'html.parser')
        paragraphs = [p.text for p in soup('p')]
        return "\n\n".join(paragraphs)
    def multi_processing(self):
        with ThreadPoolExecutor(max_workers=100) as pool:
            all_chapters = pool.map(BookWeaver.get_chap_content, self.novel_chapter_urls)
        return '\n\n\n\n'.join(all_chapters)



bw = BookWeaver()
number_Of_chapters = input("Enter the number of chapters")
searched_url =bw.generate_search_url()
novel_url =bw.get_novel_url(searched_url)
print(novel_url,"novel_url")
first_chap_url = bw.first_chapter(novel_url)
print(first_chap_url,"first_chap_url")
chapetres = []
for i in range(int(number_Of_chapters)):

    print("entered the loop")
    chapetres.append(bw.get_chap_content(first_chap_url))

    first_chap_url = bw.next_chapter(first_chap_url)




    




        



