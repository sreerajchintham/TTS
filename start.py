from gtts import gTTS
import re
import requests
from bs4 import BeautifulSoup

header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"}
url = "https://novelbin.com/b/shadow-slave/chapter-1-nightmare-begins"

def get_chapter_content(url):
    response = requests.get(url,headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')
    chapter_content = soup.find("div",class_ = "chr-c")
    if chapter_content.text:
        novel_text = "\n".join([p.text for p in chapter_content.find_all("p")])   
    else:
        print("Chapter Not Found!")
        return
    return novel_text

def create_text_file_and_audio(url):
    chapter_text = get_chapter_content(url)
    response = requests.get(url,headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')
    novel_name = soup.find(class_="novel-title").text.strip()
    chapter_title = soup.find(class_="chr-title").text.strip()
    file_name = re.sub(r'[\/:*?"<>|]', '', novel_name + " " + chapter_title)
    with open(f"{file_name}.txt", "w",encoding="utf-8") as file:
        file.write(chapter_text)
    language = 'en'
    tts = gTTS((chapter_text), lang=language, slow=False)
    tts.save(f"{file_name}.mp3")



# def create_pdf_file(url):
create_search_url()


# get_chapter_content(url=url)
# create_text_file_and_audio(url=url)