from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import html
import requests
import json


base_url = "https://www.ajnet.me"
data   =  []

def get_html(url):
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'lxml')
    data =  get_data(soup)
    with open('data.json', 'w') as f:
        json.dump(data, f)

    return None

def get_data(soup):
    cards_section = soup.find("section", {'id': 'news-feed-container'})
    for card in cards_section:
        image_container_div = card.find("div", {"class":"article-card__image-wrap"})
        page_link = card.find("a",{"class":"u-clickable-card__link"})
        label = card.find("h3",{"class":"gc__title"})
        image_container = None
        if image_container_div is not None:
            image_container = image_container_div.find("div",{"class":"responsive-image"}).find("img")
            image_src = None
            if image_container is not None:
                image_src = image_container.get('src')
            
            main_page = None
            if page_link is not None:
                page_req_link = page_link.get('href')
                page_data = requests.get(base_url+page_req_link)
                main_page = BeautifulSoup(page_data.content,'lxml')
                title = main_page.find("h1")
                article = main_page.find("div",{"class":"wysiwyg--all-content"}).find_all("p")
            a_tag = None
            if label is not None:
                a_tag = label.find("a").text.strip()
            print(a_tag)

            x = {
                    "title": a_tag,
                    "image": base_url+image_src,
                    "article": ''.join([p.text for p in article])
                }
            data.append(x)
    return data

get_html("https://www.ajnet.me/where/arab/palestine/")