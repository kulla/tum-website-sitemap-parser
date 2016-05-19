# parse_sitemap.py
#
# Written in 2016 by Stephan Kulla ( http://kulla.me/ )
#
# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain
# worldwide. This software is distributed without any warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# < http://creativecommons.org/publicdomain/zero/1.0/ >.

import requests
import sys

from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

class Node(object):

    def __init__(self, name, url):
        self.name = str(name)
        self.url = url
        self.children = []

    def append_nodes_from_html(self, ul, base_url):
        for li in ul.find_all("li", recursive=False):
            a = li.find("a", recursive=False)

            if a:
                if a["href"].startswith("/"):
                    url = base_url.rstrip("/") + a["href"]
                else:
                    url = a["href"]

                node = Node(a.string, url)
            else:
                strong = li.find("strong", recursive=False)
                node = Node(strong.string, None)

            subul = li.find("ul", recursive=False)

            if subul:
                node.append_nodes_from_html(subul, base_url)

            self.children.append(node)

    @property
    def urls(self):
        result = set([ self.url ])

        for child in self.children:
            result.update(child.urls)

        return result

    def merge(self, other):
        assert self.name.startswith(other.name) or other.name.startswith(self.name)

        self.url = self.url or other.url

        assert (other.url == None or
                self.url.rstrip("/").startswith(other.url.rstrip("/")) or
                other.url.rstrip("/").startswith(self.url.rstrip("/")))

        self.children = self.children or other.children

        assert len(other.children) == 0 or len(self.children) == len(other.children)

        for schild, ochild in zip(self.children, other.children):
            schild.merge(ochild)

    def __str__(self, level=0):
        result = " "*level + self.name

        for child in self.children:
            result += "\n" + child.__str__(level+1)

        return result

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

        template = env.get_template("template.html")

        return template.render(sitemap = self.fetch_sitemap())

if __name__ == "__main__":
    assert len(sys.argv) >= 4

    sitemap = TUMSitemap(sys.argv[1], sys.argv[2])

    with open(sys.argv[3], "w") as fd:
        fd.write(sitemap.to_html())
