from core.feed import News
import urllib.parse

class basicFeed(News):
    def __init__(self, origin, link) -> None:
        self.schema["origin"] = origin
        self.rss_link = link
        self.articles = []
        self.feed_file = f"{self.out_feeds_dir}{urllib.parse.urlsplit(self.rss_link).netloc}.feed.xml"
        self.check_out_dirs()
        super().__init__(origin, link)
    
