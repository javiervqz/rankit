from webParser import LinkParser

website = LinkParser('fing.uach.mx')

links_list, html, clean_url = website.getLinks()

print(len(links_list))

for link in links_list:
    print (link)
