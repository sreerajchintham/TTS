from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
driver = webdriver.Chrome(ChromeDriverManager().install())
response = driver.get('https://novelbin.com/b/empire-of-shadows/chapter-1-the-summer-breeze')
soup = BeautifulSoup(response.text, "lxml")
driver.quit()