from abc import ABC, abstractmethod
from os import mkdir
from os.path import exists
import urllib.parse

class FeedNews(ABC):
    def __init_subclass__(self) -> None:
        self.schema = {            
            "title": str,
            "pub_date": str,
            "raw_html": str,
            "description": str,
            "content": [],
            "link": str,
            "creator": str,
            "category": [],
            "origin": "FeedNews"
            }
        self.articles = []
        self.rss_link = ""
        self.out_minicast_dir = "./sounds/"
        self.out_feeds_dir = "./feeds/"
        self.mime = "application/rss+xml; charset=UTF-8"
        self.feed_file = ""
        return super().__init_subclass__()
    @abstractmethod
    def consume_feed() -> bool: pass
    @abstractmethod
    def parse_feed() -> bool: pass
    @abstractmethod
    def send_feed(provider: str, article: dict) -> dict: pass
    @abstractmethod
    def get_wave(res: dict) -> bool: pass
    
    def check_out_dirs(self) -> bool:
        for outs_dir in self.out_minicast_dir, self.out_feeds_dir:
            if not exists(outs_dir):
                if mkdir(outs_dir):
                    return True
                else: return False
                