import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re
from urllib3 import request
from html import unescape
from copy import deepcopy
from json import dumps, loads
from os.path import exists
from os import mkdir
try: import gc; gc.enable()
except: pass