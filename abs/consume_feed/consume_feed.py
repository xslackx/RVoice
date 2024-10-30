from abc import ABC, abstractmethod
from os import mkdir
from os.path import exists
from urllib3 import request
from json import dumps
from urllib.request import urlopen

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

    def consume_feed(self) -> bool:
        try:
            req = request('GET', 
                          self.rss_link, 
                          headers={"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0"})
                
            if req.status == 200 and len(req.data) > 0:
                with open(self.feed_file, 'wb') as file:
                    file.write(req.data)
                    return True
        except:
            return False
        
    @abstractmethod
    def parse_feed(self) -> bool: pass
    
    
    def send_feed(self, provider: str, article: dict) -> dict:
        try:
            req = request(method='POST', url=provider, body=dumps(article), timeout=4600)
        except: return dumps({"status": 'unprocessed'})
        return req.json()
    
    def get_wave(self, res: dict) -> bool:
        try:
            with urlopen(res["link"], timeout=4600) as data:
                with open(f"{self.out_minicast_dir}{res['name']}", 'wb') as wav:
                    wav.write(data.read())
                    return True
        except: return False
    
    def check_out_dirs(self) -> bool:
        for outs_dir in self.out_minicast_dir, self.out_feeds_dir:
            if not exists(outs_dir):
                if mkdir(outs_dir):
                    return True
                else: return False
                