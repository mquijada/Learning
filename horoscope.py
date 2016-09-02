
#Import requests and BeautifulSoup
import requests
from bs4 import BeautifulSoup

page = requests.get("http://www.elle.com/horoscopes/daily/a107/aquarius-daily-horoscope/")

# Displays all content on webpage
page.content

#Create the soup
soup = BeautifulSoup(page.content, 'html.parser')

#print date and aquarius horoscope 
date = soup.find_all("h3", {"class": "body-el-subtitle standard-body-el-subtitle article-sub-title"})
horoscope = soup.find_all("p", {"class": "body-el-text standard-body-el-text"})

for text in date:
    print text.contents[0].strip()
    
for text in horoscope:
    print text.contents[0].strip()
    


