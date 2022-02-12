from urllib.request import urlopen, Request
from urllib.parse import urlparse, urljoin
from urllib.error import URLError
import ssl
import sys
from bs4 import BeautifulSoup
from time import time

HEADERS_REQUEST = { 'User-Agent':'''
                                        Mozilla/5.0 (X11; Ubuntu;
                                        Linux x86_64;rv:54.0)
                                        Gecko/20100101 Firefox/54.0'''}
CONTEXT = ssl.create_default_context()
CONTEXT.check_hostname = False
CONTEXT.verify_mode=ssl.CERT_NONE

def time_it(func):
    def wrapper(*args, **kwargs):
        start = time()
        value_r = func(*args, **kwargs)
        end = time()
        print(f'For funtion {func.__name__} it takes {end-start}')
        return value_r
    return wrapper



class LinkParser:
    def __init__(self,web_site):
        self.web_site = web_site

    #@time_it
    def _cleanUrl(self): 
        '''
        Cleans the url given by the user and provides the landing page of the url
        returns: DOMBytes, url
        DOMBytes HTML document in bytes
        url Clean URL
        '''
        web_site = self.web_site
        
        if (web_site.endswith('/') ) :
            web_site = web_site[:-1] 

        try:
            req = Request(web_site, headers=HEADERS_REQUEST)
        except:
            web_site = 'http://' + web_site
            req = Request(web_site, headers=HEADERS_REQUEST)

        doc = urlopen(req, context=CONTEXT)

        if 'text/html' == doc.info().get_content_type():
            docBytes = doc.read()
            return docBytes, web_site
        else:
            return '', "Not html page"


    @time_it
    def getLinks(self):
        '''
        Cleans input url and returns html from such url if valid and all links (href) cointain within the html of given url
        returns tuple (links_from_base, html, web_site):
        '''
        html, web_site = self._cleanUrl()
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup('a')
        links_from_base = set()
        for tag in tags:
            href = tag.get('href', None)
            if href is None or href.endswith('.pdf'): continue

            href = href.strip()
            up = urlparse(href)
            if (len(up.scheme)<1):
                href = urljoin (web_site,href)
            ipos = href.find('#')
            if (ipos>1): href = href[:ipos]
            if (href.endswith('/')): href=href[:-1]
            pos = href.find('</a>')
            if (pos > 1): href = href[:pos]
            if (web_site in href):
                links_from_base.add(href)

        links_from_base = list(links_from_base)
        return links_from_base, html, web_site
