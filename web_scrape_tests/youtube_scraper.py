from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

myurl = "https://www.youtube.com/results?search_query=pepega%20clap"

uClient = uReq(myurl)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")
results_text = page_soup.findAll("body", {"dir": "ltr"})[0].findAll("script")[1]
number = str(results_text).index(r"/watch?v=") + 9
print(str(results_text)[number : number + 11])
