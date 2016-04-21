import requests

from api import Node
from bs4 import BeautifulSoup

class SitemapFetcher(object):

    def __init__(self, root_name, base_url):
        self.root = Node(root_name, base_url)
        self.visited = set()

    def fetch_sitemap(self):
        while True:
            urls = self.root.urls - self.visited

            if len(urls) > 0:
                next_url = urls.pop()

                self.visited.add(next_url)

                print(next_url)

                if next_url.startswith(self.root.url):
                    self.root.merge(self.parse_sitemap_from_site(next_url))
            else:
                break

        return self.root

    def parse_sitemap_from_site(self, url):
        html = BeautifulSoup(requests.get(url).text)

        sitemenu = html.find("nav", class_="sitemenu").find("ul")

        root = Node(self.root.name, self.root.url)
        root.append_nodes_from_html(sitemenu, self.root.url)

        self.visited.add(url)

        return root

if __name__ == "__main__":
    fetcher = SitemapFetcher("Fakultätsseite", "http://www.ma.edu.tum.de/")

    print(fetcher.fetch_sitemap())
