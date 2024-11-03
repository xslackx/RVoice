from abc import ABC, abstractmethod

class FeedNews(ABC):
    def __init_subclass__(self) -> None:
        self.schema = {            
            }
        self.articles = []
        self.rss_link = ""
        self.out_minicast_dir = "./sounds/"
        self.out_feeds_dir = "./feeds/"
        self.mime = "application/rss+xml; charset=UTF-8"
        self.feed_file = ""
        
        return super().__init_subclass__()
    @abstractmethod 
    def consume_feed(self) -> bool: pass
    @abstractmethod    
    def compound(self, b1, b2): pass
    @abstractmethod     
    def remove_html_tags(self, text): pass  
    @abstractmethod                    
    def parse_feed(self) -> bool: pass
    @abstractmethod                    
    def send_feed(self, provider: str, article: dict) -> dict: pass
    @abstractmethod 
    def get_wave(self, res: dict) -> bool: pass
    @abstractmethod 
    def check_out_dirs(self) -> bool: pass
    @abstractmethod             
    def iter_root(self): pass           