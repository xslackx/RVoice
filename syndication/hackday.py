from abs.consume_feed import FeedNews
from syndication import *

class HackDay(FeedNews):
    def __init__(self) -> None:
        self.schema["origin"] =  "Hackday"
        self.articles = []
        self.rss_link = "https://hackaday.com/blog/feed/"
        self.feed_file = f"{self.out_feeds_dir}{urllib.parse.urlsplit(self.rss_link).netloc}.feed.xml"
        self.check_out_dirs()
         
    def consume_feed(self) -> bool:
        try:
            with urllib.request.urlopen(self.rss_link, timeout=30) as feed:
                if feed.status == 200 and feed.getheaders()[2][1] == self.mime:
                    with open(self.feed_file, "wb") as file:
                        file.write(feed.read())
                        return True
        except:
            return False

    def parse_feed(self) -> bool:
        root = ET.parse(f"{self.feed_file}")
        items = []
        description_re = r"<\/div>(.*)<a"
        content_re = r"<p>(.*)<\/p>"
        html_tags = '<.*?>'
        
        for child in root.iter():
            if child.tag == "item":
                items.append(child)

        def remove_html_tags(text):
            clean = re.compile(html_tags)
            return re.sub(clean, '', text)
 
        def iter_elements(html: str, tag: str):
            matches = ""
            if tag == "description":
                matches = re.finditer(description_re, html, re.MULTILINE)
            
            if tag == "content":
                matches = re.finditer(content_re, html, re.MULTILINE)
                stanzas = []
            
            if tag == "" or tag == None:
                return
                
            for matchNum, match in enumerate(matches, start=1):
                for groupNum in range(0, len(match.groups())):
                    groupNum = groupNum + 1
                    
                    if tag == "description":
                        return unescape(match.group(groupNum))
                    
                    if tag == "content":
                       stanzas.append(remove_html_tags(unescape(match.group(groupNum))))
            
            if len(stanzas) > 0 and tag == "content":
                return stanzas
            
        def explode(data: list):
            let = deepcopy(self.schema)
            for element in data:
                if element.tag == 'title': let["title"] = element.text
                if element.tag == 'link': let["link"] = element.text
                if element.tag == 'description': let["description"] = iter_elements(element.text, "description")
                if element.tag == 'pubDate': let["pub_date"] = element.text
                if element.tag == 'category': let['category'].append(element.text)  
                if element.tag == '{http://purl.org/dc/elements/1.1/}creator':
                    let["creator"] = element.text
                if element.tag == "{http://purl.org/rss/1.0/modules/content/}encoded":
                    let["content"] = iter_elements(element.text, "content")
                    let["raw_html"] = "parsed"
                    return let
        
        self.articles = list(map(explode, items))
        
        if len(self.articles) <= 0:
            return False
        return True
        
    def send_feed(self, provider: str, article: dict) -> dict:
        try:
            req = request(method='POST', url=provider, body=dumps(article), timeout=4600)
        except: return dumps({"status": 'unprocessed'})
        return req.json()
    
    def get_wave(self, res: dict) -> bool:
        try:
            with urllib.request.urlopen(res["link"], timeout=4600) as data:
                with open(f"{self.out_minicast_dir}{res['name']}", 'wb') as wav:
                    wav.write(data.read())
                    return True
        except: return False
