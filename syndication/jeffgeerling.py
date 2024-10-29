from abs.consume_feed import FeedNews
from syndication import *

class Itsfoss(FeedNews):
    def __init__(self) -> None:
        self.schema["origin"] = "Itsfoss"
        self.rss_link = "https://www.jeffgeerling.com/blog.xml"
        self.feed_file = f"{self.out_feeds_dir}{urllib.parse.urlsplit(self.rss_link).netloc}.feed.xml"

        try:
            self.check_out_dirs()
        except: raise Exception("Cannot create the out_minicast_dir or out_feeds_dir in FeedNews abs")

        super().__init__()
    
    def parse_feed() -> bool:
        pass
    
    def send_feed(provider: str, article: dict) -> dict:
        return super().send_feed(article)

    def get_wave(res: dict) -> bool:
        return super().get_wave()