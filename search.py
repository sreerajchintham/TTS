from bs4 import BeautifulSoup
from gtts import gTTS
import requests
import re
from ebooklib import epub
import time
import selenium
start_time = time.time()
header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"}

def search_url(novel_title):
    search_url = "https://novelbin.com/search?keyword=" +"+".join(novel_title.split())
    chap_search_response = requests.get(url=search_url,headers=header) 
    soup = BeautifulSoup(chap_search_response.text,"html.parser")
    first_result = soup.find("h3",class_= "novel-title")
    if not first_result:
       return "Enter a valid novel title"
        
    return first_result.find("a")["href"]


def homepage_to_first(homepage_url):
    homepage_response = requests.get(url=homepage_url,headers=header)
    soup = BeautifulSoup(homepage_response.text,"html.parser")
    first_chap_url = soup.find("a",class_="btn btn-danger btn-read-now")["href"]
    return first_chap_url

def next_chap(url):
    response = requests.get(url,headers=header)

    soup = BeautifulSoup(response.text,"html.parser")
    print(response.status_code)
    next_chap_url = soup.find("a",id="next_chap")["href"]
    time.sleep(2)
    get_chapter_content(url)
    return next_chap_url


def get_chapter_content(url):
    retries = 5
    for i in range(retries):
        response = requests.get(url,headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')
        chapter_content = soup.find("div",class_ = "chr-c")
        if response.status_code == 200:
            novel_text = "\n".join([p.text for p in chapter_content.find_all("p")])
            break

        else:
            time.sleep(5)
            continue
        # if not chapter_content:
        #     print(f"this is the response {response.status_code}")
        # else:
    #         print("Chapter Not Found!")
    novel_name = soup.find(class_="novel-title").text.strip()
    chapter_title = soup.find(class_="chr-title").text.strip()

    return [novel_name,(chapter_title,novel_text)]
    
    # file_name = re.sub(r'[\/:*?"<>|]', '', novel_name + " " + chapter_title)
    # with open(f"{file_name}.txt", "w",encoding="utf-8") as file:
    #     file.write(novel_text)
    # language = 'en'
    # tts = gTTS((novel_text), lang=language, slow=False)
    # tts.save(f"{file_name}.mp3")




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

def chapter_input():
    novel_title = input("Enter the novel title: \n")
    url_homepage = search_url(novel_title)
    first_chap_url =homepage_to_first(url_homepage)
    chap_url = first_chap_url
    novel_name = get_chapter_content(chap_url)[0]
    chapters = []
    try:
        number_of_chapters = int(input("Enter the number of chapters ypu want to download"))
        for i in range(number_of_chapters): 
            matter = get_chapter_content(chap_url)
            print(chap_url)
            chapters.append(matter[1])
            chap_url = next_chap(chap_url)
            
    except:
        if input == "all":

            while next_chap(chap_url):
                matter = get_chapter_content(chap_url)
                chapters.append(matter[1])
                chap_url = next_chap(chap_url)
                
        else:
            raise "enter valid number or all"
    return novel_name,chapters
tuple_chap = chapter_input()

create_epub(tuple_chap[0],tuple_chap[1])

end_time = time.time()
total_time = (end_time-start_time)
print(f"The time it took is {int(total_time//60)} minutes and {total_time%60:.2f} seconds")



