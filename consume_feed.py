import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re
from urllib3 import request
from abc import ABC, abstractmethod
from html import unescape
from copy import deepcopy
from json import dumps, loads
from os.path import exists
from os import mkdir
try: import gc; gc.enable()
except: pass

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
    
class HackDay(FeedNews):
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
        self.rss_link = "https://hackaday.com/blog/feed/"
        self.out_minicast_dir = "./sounds/"
        self.out_feeds_dir = "./feeds/"

        for outs_dir in self.out_minicast_dir, self.out_feeds_dir:
            if not exists(outs_dir):
                mkdir(outs_dir)
         
    def consume_feed(self) -> bool:
        try:
            with urllib.request.urlopen(self.rss_link, timeout=30) as feed:
                if feed.status == 200 and feed.getheaders()[2][1] == self.mime:
                    with open(f"{self.out_feeds_dir}feed.xml", "wb") as file:
                        file.write(feed.read())
                        return True
        except:
            return False

    def parse_feed(self) -> bool:
        root = ET.parse("./feeds/feed.xml")
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
            req = request(method='POST', url=provider, body=dumps(article), timeout=3600)
        except: return dumps({"status": 'unprocessed'})
        return req.json()
    
    def get_wave(self, res: dict) -> bool:
        try:
            with urllib.request.urlopen(res["link"], timeout=3600) as data:
                with open(f"./sounds/{res['name']}", 'wb') as wav:
                    wav.write(data.read())
                    return True
        except: return False