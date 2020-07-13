import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import os

myurl = (
    "https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=graphics+cards"
)

# opening a connection and grabbing the page
uClient = uReq(myurl)
page_html = uClient.read()  # storing the html page in a variable
uClient.close()

# parses the html we get from uReq
page_soup = soup(page_html, "html.parser")

# grabs all the products on the page
containers = page_soup.findAll("div", {"class": "item-container"})

# get the first product of the list
container = containers[0]

# grab the title by navigating through the html
title = container.div.div.a.img["title"]

print(title)

# cycle through all the containers in our list and print the titles
for container in containers:
    brand = container.div.div.a.img["title"]
    title_container = container.findAll("a", {"class": "item-title"})
    title = title_container[0].text
    price_container = container.findAll("li", {"class": "price-current"})
    price = price_container[0].strong.text
    price = "$" + price + ".99"
    shipping_container = container.findAll("li", {"class": "price-ship"})
    shipping = shipping_container[0].text
    print(brand)
    print(title)
    print(price)
    print(shipping)
    print(" ")
    print(" ")
