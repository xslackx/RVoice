from abc import ABC, abstractmethod

class FeedNews(ABC):
    def __init_subclass__(self) -> None:
        self.schema = {}
        self.articles = []
        self.rss_link = ""
        self.out_minicast_dir = ""
        self.out_feeds_dir = ""
        self.mime = "application/rss+xml; charset=UTF-8"
        return super().__init_subclass__()
    @abstractmethod
    def consume_feed() -> bool: pass
    @abstractmethod
    def parse_feed() -> bool: pass
    @abstractmethod
    def send_feed(provider: str, article: dict) -> dict: pass
    @abstractmethod
    def get_wave(res: dict) -> bool: pass