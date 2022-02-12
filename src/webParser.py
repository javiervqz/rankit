from urllib.request import urlopen, Request
from urllib.parse import urlparse, urljoin
from urllib.error import URLError
import ssl
import sys
from bs4 import BeautifulSoup




class LinkParser:
    def __init__(self,web_site):
        self.headers = { 'User-Agent':'''
                                        Mozilla/5.0 (X11; Ubuntu;
                                        Linux x86_64;rv:54.0)
                                        Gecko/20100101 Firefox/54.0'''}

        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode=ssl.CERT_NONE
        self.web_site = web_site

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

        if ( web_site.endswith('.htm') or web_site.endswith('.html')):
            pos = web_site.rfind('/')
            web_site = web_site[:pos]

        if not (web_site.startswith('http://') or web_site.startswith('https://')):
            try:
                    req = Request('https://'+web_site, headers=self.headers)
                    doc = urlopen(req, context=self.ctx)
                    self.url = 'https://'+web_site
            except:
                try:
                    req = Request('http://'+web_site, headers=self.headers)
                    doc = urlopen(req, context=self.ctx)
                    self.url = 'http://'+web_site
                except URLError as error:
                    print('Unable to retrive ', error, web_site)
                    exit(1)
        else:
            try:
                    req = Request(web_site, headers=self.headers)
                    doc = urlopen(req, context=self.ctx)
                    self.url = web_site
            except URLError as error:
                    print ('Unable to retrieve ', error, web_site)
                    exit(1)

        if 'text/html' == doc.info().get_content_type():
            docBytes = doc.read()
            return docBytes, self.url
        else:
            return '', "Not html page"



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
            if (href is None): continue

            href = href.strip()
            up = urlparse(href)
            if (len(up.scheme)<1):
                href = urljoin (self.url,href)
            ipos = href.find('#')
            if (ipos>1): href = href[:ipos]
            if (href.endswith('/')): href=href[:-1]
            pos = href.find('</a>')
            if (pos > 1): href = href[:pos]
            if (web_site in href):
                    links_from_base.add(href)

        links_from_base = list(links_from_base)
        return links_from_base, html, web_site
