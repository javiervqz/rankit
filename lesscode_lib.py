from urllib.request import urlopen, Request
from urllib.error import URLError
import sys

def clean_url(web_site, ctx): # returns HTTP object
	headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'}

	if (web_site.endswith('/') ) :
		web_site = web_site[:-1]
	if ( web_site.endswith('.htm') or web_site.endswith('.html') ) :
		pos = web_site.rfind('/')
		web_site = web_site[:pos]
	if not (web_site.startswith('http://') or web_site.startswith('https://')):
		try:
			req = Request('https://'+web_site, headers=headers)
			doc = urlopen(req, context=ctx)
		except:
			try:
				req = Request("https://" + "www." +web_site, headers=headers)
				doc = urlopen(req, context=ctx)
			except:
				try:
					req = Request('http://'+web_site, headers=headers)
					doc = urlopen(req, context=ctx)
				except:
					try:
						req = Request('http://'+'www.' + web_site, headers=headers)
						doc = urlopen(req,context=ctx)
					except URLError as error:
						print('Unable to retrive ', error)
						sys.exit(0)
	else:
		try:
			req = Request(web_site, headers=headers)
			doc = urlopen(req, context=ctx)
		except URLError as error:
			print ('Unable to retrieve ', error)
			sys.exit(0)
	if len(doc.read()) == 0:
		print ('Unable to retrive, empty page or wrong host')
		sys.exit(0)
	else:
		return doc
