from abs.consume_feed import FeedNews
from syndication import *

class Lwn(FeedNews):
    def __init__(self, link) -> None:
        self.schema["origin"] = "Lwn"
        self.rss_link = "https://lwn.net/headlines/rss"
        self.feed_file = f"{self.out_feeds_dir}{urllib.parse.urlsplit(self.rss_link).netloc}.feed.xml"
        self.check_out_dirs()

        super().__init__()
        
    def parse_feed(self) -> bool:
        items = self.iter_root()
        
        
        def compound(b1, b2):
            return b1 if b1 is not None \
                else b2 if b2 is not None \
                    else None
            
        def iter_elements(data):
            let = deepcopy(self.schema)
            for element in data:
                if element.tag == "title": element.txt
                if element.tag == "link": pass
                if element.tag == '{http://purl.org/dc/elements/1.1/}creator':
                    let["creator"] = compound(element.text, "Unknown")
                if element.tag == "description": pass
                if element.tag == "pubDate": pass