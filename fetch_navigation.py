from api import TUMSitemap

if __name__ == "__main__":
    sitemap = TUMSitemap("Fakultätsseite", "http://www.ma.edu.tum.de/")

    with open("outline.html", "w") as fd:
        fd.write(sitemap.to_html())
