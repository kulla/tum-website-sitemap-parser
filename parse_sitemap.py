import sys

from api import TUMSitemap

if __name__ == "__main__":
    assert len(sys.argv) >= 4

    sitemap = TUMSitemap(sys.argv[1], sys.argv[2])

    with open(sys.argv[3], "w") as fd:
        fd.write(sitemap.to_html())
