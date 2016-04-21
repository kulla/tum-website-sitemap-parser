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
        assert self.name == other.name

        self.url = self.url or other.url

        assert other.url == None or (self.url == other.url)

        self.children = self.children or other.children

        assert len(other.children) == 0 or len(self.children) == len(other.children)

        for schild, ochild in zip(self.children, other.children):
            schild.merge(ochild)

    def __str__(self, level=0):
        result = " "*level + self.name

        for child in self.children:
            result += "\n" + child.__str__(level+1)

        return result
