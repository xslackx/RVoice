from abs.consume_feed import FeedNews
from syndication import *

class Phoronix(FeedNews):
    def __init__(self) -> None:
        self.schema = {
            "title": str,
            "pub_date": str,
            "raw_html": str,
            "description": str,
            "content": [],
            "link": str,
            "creator": str,
            "category": []
        }
        self.articles = []
        self.rss_link = "https://www.phoronix.com/rss.php"
        self.feed_file = f"{self.out_feeds_dir}{urllib.parse.urlsplit(self.rss_link).netloc}.feed.xml"
        super().__init__()
    
    def consume_feed() -> bool:
        pass
    
    def get_wave(res: dict) -> bool:
        return super().get_wave()
    
    def parse_feed() -> bool:
        pass
    
    def send_feed(provider: str, article: dict) -> dict:
        return super().send_feed(article)
    