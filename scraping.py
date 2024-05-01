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
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

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
                main_page = page_link.get('href')
            #     article = main_page.find("div",{"class":"wysiwyg--all-content"}).find_all("p")
            
            a_tag = None
            if label is not None:
                a_tag = label.find("a").text.strip()
            print(a_tag)

            x = {
                    "title": a_tag,
                    "image": base_url+image_src,
                    # "article": ''.join([p.text for p in article]),
                    "link": main_page
                }
            data.append(x)
    return data


def get_page (page_link) :
    response = requests.get(page_link)
    main_page = BeautifulSoup(response.content, 'html.parser')
    article_tag = main_page.find("div",{"class":"wysiwyg--all-content"}).find_all("p")
    article = ''.join([p.text for p in article_tag])
    data = {
        "article": article,
    }
    with open('test.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return None


get_page("https://www.ajnet.me/news/2024/5/1/%D8%A3%D8%A8%D8%B1%D8%B2-%D8%AA%D8%B7%D9%88%D8%B1%D8%A7%D8%AA-%D8%A7%D9%84%D9%8A%D9%88%D9%85-%D8%A7%D9%84%D9%80208-%D9%85%D9%86-%D8%A7%D9%84%D8%AD%D8%B1%D8%A8")

get_html("https://www.ajnet.me/where/arab/palestine/")