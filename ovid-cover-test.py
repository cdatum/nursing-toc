# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 10:05:54 2020

@author: Yellow
"""

import urllib.request
from bs4 import BeautifulSoup




journals = {'nep' : {'title': 'Nursing Education Perspectives',    'url': 'http://ovidsp.ovid.com/rss/journals/00024776/current.rss', 'html': 'nursing_education_perspectives.html',    'cover': 'https://journals.lww.com/neponline/pages/default.aspx'},
            'ajn' : {'title': 'AJN - American Journal of Nursing', 'url': 'http://ovidsp.ovid.com/rss/journals/00000446/current.rss', 'html': 'american_journal_of_nursing.html',       'cover': 'https://journals.lww.com/ajnonline/pages/default.aspx'},
            'nmie': {'title': 'Nursing Made Incredibly Easy',      'url': 'http://ovidsp.ovid.com/rss/journals/00152258/current.rss', 'html': 'nursing_made_incredibly_easy.html',      'cover': 'https://journals.lww.com/nursingmadeincrediblyeasy/pages/default.aspx'},
            'nur' : {'title': 'Nursing',                           'url': 'http://ovidsp.ovid.com/rss/journals/00152193/current.rss', 'html': 'nursing.html',                           'cover': 'https://journals.lww.com/nursing/pages/default.aspx'},
            'ncc' : {'title': 'Nursing Critical Care',             'url': 'http://ovidsp.ovid.com/rss/journals/01244666/current.rss', 'html': 'nursing_critical_care.html',             'cover': 'https://journals.lww.com/nursingcriticalcare/pages/default.aspx'},
            'mcn' : {'title': 'MCN: American Journal of Maternal Child Nursing', 'url': 'http://ovidsp.ovid.com/rss/journals/00005721/current.rss', 'html': 'mcn.html',                 'cover': 'https://journals.lww.com/mcnjournal/pages/default.aspx'},
            'hhn' : {'title': 'Home Healthcare Now',               'url': 'http://ovidsp.ovid.com/rss/journals/01845097/current.rss', 'html': 'home_healthcare_now.html',               'cover': 'https://journals.lww.com/homehealthcarenurseonline/pages/default.aspx'},
            
           }

webpage = "https://journals.lww.com/neponline/pages/default.aspx"
page = urllib.request.urlopen(webpage,  timeout=20).read()
soup = BeautifulSoup(page,'lxml') #xml parser

srcurl = soup.find_all('div', class_="ejp-footer__smart-control-section-image-container")
srcurl = srcurl[0].find('img')
srcurl = srcurl['src']
print(srcurl)



'''
Works for some of the pages
page = urllib.request.urlopen(webpage,  timeout=20).read()
soup = BeautifulSoup(page,'lxml') #xml parser

srcurl = soup.find_all('div', class_="coverImage")
srcurl = srcurl[0].find('img')
srcurl = srcurl['src']
print(srcurl)
'''

# req = urllib.request(url , headers={'User-Agent': 'Mozilla/5.0'})

#imgurl = soup.find_all("div", class_="coverImage")
#imgurl = soup.select("div.coverImage img[src]")



'''
imgurl = soup.select("div.coverImage img")
for img in imgurl:
    print(img['src'])
'''




'''
id_soup = BeautifulSoup('<p id="my id"></p>')
id_soup.p['id']
# 'my id'
'''

'''

# Create a URL for each issue's cover img based on the issn, date, and issue #
def get_cover_art_url(url):   
    #Soupify
    soup = BeautifulSoup(page,'xml') #xml parser
    print(soup)
    
    #Find cover img
'''