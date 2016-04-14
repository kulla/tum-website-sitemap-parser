class Node(object):

    def __init__(self, name, link):
        self.name = str(name)
        self.link = link
        self.children = []

    def append_nodes_from_html(self, ul, base_url):
        for li in ul.find_all("li", recursive=False):
            a = li.find("a", recursive=False)

            if a:
                node = Node(a.string, base_url.rstrip("/") + a["href"])
            else:
                strong = li.find("strong", recursive=False)
                node = Node(strong.string, None)

            subul = li.find("ul", recursive=False)

            if subul:
                node.append_nodes_from_html(subul, base_url)

            self.children.append(node)

    def __str__(self, level=0):
        result = " "*level + self.name

        for child in self.children:
            result += "\n" + child.__str__(level+1)

        return result
