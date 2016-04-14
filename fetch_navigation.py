# -*- coding: utf-8 -*-

import requests

from api import Node
from bs4 import BeautifulSoup

def get_navigation_from_site(url, title):
    html = BeautifulSoup(requests.get(url).text)

    sitemenu = html.find("nav", class_="sitemenu").find("ul")

    root = Node(title, url)
    root.append_nodes_from_html(sitemenu, url)

    return root

if __name__ == "__main__":
    print get_navigation_from_site("http://www.ma.edu.tum.de/", "Fakultätsseite")
