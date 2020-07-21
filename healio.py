# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 09:44:34 2020

@author: Christopher Galluzzo
Import RSS feeds from Ovid and parse the table of contents into HTML
"""

import urllib.request
from bs4 import BeautifulSoup
import os


'''
HEALIO XML
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
   <channel xmlns:dc="http://purl.org/dc/elements/1.1/">
      <title>Journal of Nursing Education</title>
      <link>https://www.healio.com/</link>
      <description />
      <language>en-us</language>
      <managingEditor>itsupport@wyanokegroup.com (TBD)</managingEditor>
      <lastBuildDate>Mon, 20 Jul 2020 20:06:37 Z</lastBuildDate>
      <image>
         <url>https://www.healio.com:8085/~/media/images/healiofeedlogo.png</url>
         <title>Journal of Nursing Education</title>
         <link>https://www.healio.com/</link>
      </image>
      <link href="https://www.healio.com" rel="self" type="application/rss+xml" />
      <item>
         <guid isPermaLink="true">https://www.healio.com/nursing/journals/jne/2020-7-59-7/9d200cd8-06cd-44b3-8f29-31377ffaaa17/using-social-media-to-engage-nurse-practitioner-students-in-complex-health-care-topics</guid>
         <link>https://www.healio.com/nursing/journals/jne/2020-7-59-7/9d200cd8-06cd-44b3-8f29-31377ffaaa17/using-social-media-to-engage-nurse-practitioner-students-in-complex-health-care-topics</link>
         <title>Using Social Media to Engage Nurse Practitioner Students in Complex Health Care Topics</title>
         <description>When developing curriculum, educators in advanced practice nursing programs often struggle to find innovative methods to build competencies outlined by the National Organization of Nurse Practitioner Faculties (NONPF, 2017a, 2017b) and introduce Doctor of Nursing Practice (DNP) Essentials (American Association of Colleges of Nursing, 2006). Topics such as health policy and informatics can be particularly difficult to incorporate in learning activities. Faculty at the University of Alabama at Birmingham School of Nursing grappled with ideas to present various complex topics while keeping</description>
         <pubDate>Mon, 29 Jun 2020 20:59:00 Z</pubDate>
         <dc:creator>Kelley Stallworth, DNP, WHNP-BC</dc:creator>
      </item>     
   </channel>
</rss>

'''

# Healio -Journal of Nursing Education: https://www.healio.com/sws/feed/journal/jne
# https://www-healio-com.ezproxy.ccac.edu/
# https://www-healio-com.ezproxy.ccac.edu/nursing/journals/jne/2020-7-59-7/9d200cd8-06cd-44b3-8f29-31377ffaaa17/using-social-media-to-engage-nurse-practitioner-students-in-complex-health-care-topics

# Set the URLs to open

healio = {'jne' : {'title': 'Journal of Nursing Education',    'url': 'https://www.healio.com/sws/feed/journal/jne', 'html': 'journal_nursing_education.html'} }


# Update the permalink in the rss to include the ezproxy server info
def update_permalink(url):
    permalink = url.replace("https://www.healio.com","https://www-healio-com.ezproxy.ccac.edu")
    return permalink

# Create a URL for each issue's cover img based on the issn, date, and issue #
def get_cover_art_url(url):
    prefix = "http://ovidsp.dc2.ovid.com/sp-4.07.0b/ovidweb.cgi?S=JHCLFPEGEGEBOOBHJPAKKEBFNBCNAA00&Graphic="
    suffix = "00000|CV|C|jpg"
    url = prefix + url[91:110] + suffix
    return url

def process_rss_feed(title, url, html):
    # Open RSS feed    
    page = urllib.request.urlopen(url, timeout=20).read() #.decode('utf-8')
    soup = BeautifulSoup(page,'xml') #xml parser
    
    # Get cover art url for this issue. Get first article fron issue and extract url
    article = soup.find('item')
    cover_img = get_cover_art_url(article.link.get_text())
    
    # Get the title    
    journal_title = soup.title.get_text()   
    page = soup.find_all('item')
    
    
    # Check to see if file exists locally. If not, create it
    exists = os.path.isfile(html)
    if exists == False:    
        file = open(html, 'w', encoding='utf-8')
        file.close()
            
    # Open file and write data
    file = open(html, 'w', encoding='utf-8')    
    file.write("<div class='journalTitle'>" + journal_title + "</div>\n")
    file.write("<div class='coverImg'><img src='" + cover_img + "'  alt='cover image'></div>" )
            
    for item in page:        
        article_title = item.title.get_text()
        permalink = update_permalink(item.link.get_text())
        author = item.creator.get_text()
                    
        toc = "<div class='article'><div class='articleTitle'><a target='_blank' href='" + permalink + "'>" + article_title + "</a></div>" + "<div class='articleDesc'>" + "<div class='author'><span>" + author + "</span></div></div></div>"            
        file.write(BeautifulSoup(toc, 'html.parser').prettify())
    file.close()          

for journal, details in healio.items():    
    title = details['title']
    url = details['url']
    html = details['html']
    process_rss_feed(title,url,html)