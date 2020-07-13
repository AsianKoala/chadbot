from bs4 import BeautifulSoup as soup


def get_links(filename):
    reddit_links = []
    with open(filename, "r", encoding="utf-8") as f:
        page_soup = soup(f, "html.parser")
        containers = page_soup.findAll("li")
        for container in containers:
            try:
                link = container.findAll("a")[1]["href"]
                reddit_links.append(link)
            except:
                link = container.a["href"]
                reddit_links.append(link)
    return reddit_links


old_links = get_links("old_export.html")
new_links = get_links("new_export.html")

deleted_links = [x for x in old_links if x not in new_links]
print(deleted_links)
