from abs.consume_feed.consume_feed import FeedNews
from os import mkdir
from os.path import exists
from urllib3 import request
from json import dumps
from urllib.request import urlopen
from html import unescape
from copy import deepcopy
import xml.etree.ElementTree as ET
import urllib.parse
import re

class News(FeedNews):
    def __init__(self, origin, link) -> None:
        self.schema = {            
            "title": str,
            "pub_date": str,
            "raw_html": str,
            "description": str,
            "content": [],
            "link": str,
            "creator": str,
            "category": [],
            "origin": origin
            }
        self.articles = []
        self.rss_link = link
        self.out_minicast_dir = "./sounds/"
        self.out_feeds_dir = "./feeds/"
        self.mime = "application/rss+xml; charset=UTF-8"
        self.feed_file = f"{self.out_feeds_dir}{urllib.parse.urlsplit(self.rss_link).netloc}.feed.xml"
        super().__init__()
        
    def consume_feed(self) -> bool:
        try:
            agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0"
            req = request('GET', 
                          self.rss_link, 
                          headers={"User-Agent": f"{agent}"})
                
            if req.status == 200 and len(req.data) > 0:
                with open(self.feed_file, 'wb') as file:
                    file.write(req.data)
                    return True
        except:
            return False
        
    def compound(self, b1, b2):
        return b1 if b1 is not None else b2 if b2 is not None else ""
        
    def remove_html_tags(self, text):
        html_tags = '<.*?>'
        clean = re.compile(html_tags)
        return re.sub(clean, '', text)
        
                       
    def parse_feed(self) -> bool:
        items = self.iter_root(self.feed_file)
                    
        def iter_elements(html: str, tag: str):
            description_re = r"<\/div>(.*)<a"
            content_re = r"<p>(.*)<\/p>"
            matches = ""
            stanzas = []
            
            if tag == "description":
                matches = re.finditer(description_re, html, re.MULTILINE)
            
            if tag == "content":
                matches = re.finditer(content_re, html, re.MULTILINE)
                #stanzas = []
            
            if tag == "" or tag == None:
                return
                
            for matchNum, match in enumerate(matches, start=1):
                for groupNum in range(0, len(match.groups())):
                    groupNum = groupNum + 1
                    
                    if tag == "description":
                        return unescape(match.group(groupNum))
                    
                    if tag == "content":
                       stanzas.append(self.remove_html_tags(unescape(match.group(groupNum))))
                       
            if len(stanzas) > 0 and tag == "content":
                return stanzas
            
        def explode(data: list):
            let = deepcopy(self.schema)
            for element in data:
                #print(element.tag)
                if element.tag == 'title': let["title"] = element.text
                if element.tag == 'link':
                    
                    if let["origin"] == "Lwn":
                        pass
                    else:
                        let["link"] = element.text
                
                if element.tag == 'description':
                    
                    if let["origin"] == 'HackDay':
                        let["description"] = iter_elements(element.text, "description")
                    elif let["origin"] == "Phoronix":
                        let["description"] = unescape(element.text)
                    elif let["origin"] == "Lwn":
                        let["description"] = "nodescription"
                    else:
                        let["description"] = element.text
                            
                if element.tag == 'pubDate' :
                    
                    if let["origin"] == 'HackDay':
                        let["pub_date"] = element.text
                    elif let["origin"] == "Lwn":
                        let["pub_date"] = "nodate" 
                    else: 
                        let["pub_date"] = element.text

                if element.tag == 'category':
                    #if let["origin"] == "HackDay":
                    let["category"].append(element.text)
                          
                if element.tag == '{http://purl.org/dc/elements/1.1/}creator':
                    let["creator"] = element.text
                
                if element.tag == 'author':
                    let["creator"] = element.text
                
                if element.tag == "{http://purl.org/rss/1.0/modules/content/}encoded":
                    
                    if let["origin"] == "HackDay":
                        let["content"] = iter_elements(element.text, "content")
                    
                        
                    if let["origin"] == "Lwn" or let["origin"] == "Phoronix":    
                        let["category"].append("none")
                        let["content"].append("none")
                                                   
                    let["raw_html"] = "parsed"
                    return let
        
        self.articles = list(map(explode, items))
        
        if any(self.articles):
            return True
        return False
                       
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
                
    def iter_root(self, file):
        root = ET.parse(file)
        items = []
        
        for child in root.iter():
            if child.tag == "item":
                items.append(child)
        
        if len(items) > 0:
            return items
        else: return []            