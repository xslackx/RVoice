from abs.consume_feed import FeedNews
from syndication import *

class Phoronix(FeedNews):
    def __init__(self) -> None:
        self.schema["origin"] = "Phoronix"
        self.articles = []
        self.rss_link = "https://www.phoronix.com/rss.php"
        self.feed_file = f"{self.out_feeds_dir}{urllib.parse.urlsplit(self.rss_link).netloc}.feed.xml"
        
        try:
            self.check_out_dirs()
        except: raise Exception("Cannot create the out_minicast_dir or out_feeds_dir in FeedNews abs")
        
        super().__init__()
        
    def parse_feed(self) -> bool:
        root = ET.parse(f"{self.feed_file}")
        items = []
        
        for child in root.iter():
            if child.tag == "item":
                items.append(child)
        
        def explode(data: list):
            let = deepcopy(self.schema)
            for element in data:
                if element.tag == 'title': let["title"] = element.text
                if element.tag == 'link': let["link"] = element.text
                if element.tag == 'description': let["description"] = unescape(element.text)
                if element.tag == 'pubDate': let["pub_date"] = element.text
                if element.tag == '{http://purl.org/dc/elements/1.1/}creator':
                    let["creator"] = element.text
                    let["raw_html"] = "parsed"
                    let["content"] = ["none", "none"]
                    let["category"] = ["none", "none"]
                    return let
            
        self.articles = list(map(explode, items))
        
        if len(self.articles) <= 0:
            return False
        return True      
