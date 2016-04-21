import requests

from api import Node
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

class TUMSitemap(object):

    def __init__(self, root_name, base_url):
        self.root = Node(root_name, base_url)
        self.visited = set()

    def fetch_sitemap(self):
        while True:
            urls = self.root.urls - self.visited

            if len(urls) > 0:
                next_url = urls.pop()

                self.visited.add(next_url)

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

    def to_html(self):
        env = Environment(loader = FileSystemLoader("."))

        template = env.get_template("outline.template.html")

        return template.render(sitemap = self.fetch_sitemap())

if __name__ == "__main__":
    sitemap = TUMSitemap("Fakultätsseite", "http://www.ma.edu.tum.de/")

    with open("outline.html", "w") as fd:
        fd.write(sitemap.to_html())
