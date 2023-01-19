# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 09:44:34 2020

@author: Christopher Galluzzo
Import RSS feeds from Ovid and parse the table of contents into HTML
"""

import urllib.request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import os
from PIL import Image
import requests, base64
from io import BytesIO


'''
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<rss version="2.0">
<channel>
<title><![CDATA[Nursing Education Perspectives. Volume 41(4) July/August 2020]]></title>
<link/>http://ovidsp.dc2.ovid.com/ovidweb.cgi
<description><![CDATA[Ovid Technologies Journals@Ovid RSS Feeds. Table of Contents from the most recent issue in Journals@Ovid for Nursing Education Perspectives]]></description>
<copyright><![CDATA[(C) 2020 Lippincott Williams & Wilkins, Inc.]]></copyright>
<lastbuilddate><![CDATA[Thu, 2 Jul 2020 07:31:44 +0000]]></lastbuilddate>
<language>en-us</language>
<generator>Generated by Ovid Technologies.</generator>
<image/>
<title>Ovid Technologies - Journals@Ovid</title>
<url>http://www.ovid.com/site/images/WK_Ovid_white-300px.gif</url>
<link/>http://ovidsp.dc2.ovid.com/ovidweb.cgi

<item>
<title><![CDATA[The Power of Ingenuity.]]></title>
<description><![CDATA[
                    <div class="author">
                    <strong>Author: </strong>
                    <span>Yoder-Wise, Patricia S.</span>
                    </div>
                    <div class="page">
                    <strong>Page: </strong>
                    <span>203-204</span>
                    </div>
                ]]></description>
<guid ispermalink="true"><![CDATA[http://ovidsp.dc2.ovid.com/ovidweb.cgi?T=JS&CSC=Y&NEWS=N&PAGE=fulltext&LSLINK=80&D=ovft&AN=00024776-202007000-00001]]]></guid>
<link/><![CDATA[http://ovidsp.dc2.ovid.com/ovidweb.cgi?T=JS&CSC=Y&NEWS=N&PAGE=fulltext&LSLINK=80&D=ovft&AN=00024776-202007000-00001]]>
</item>


'''

# get cover art from LWW using their RSS feed: https://journals.lww.com/neponline/pages/currenttoc.aspx
# RSS example: https://journals.lww.com/neponline/_layouts/15/OAKS.Journals/feed.aspx?FeedType=CurrentIssue

# Set the URLs to open

journals = {'nep' : {'title': 'Nursing Education Perspectives',     'url': 'http://ovidsp.ovid.com/rss/journals/00024776/current.rss', 'html': 'nursing_education_perspectives.html',    'cover': 'https://ezproxy.ccac.edu/login?url=http://ovidsp.ovid.com/ovidweb.cgi?T=JS&NEWS=n&CSC=Y&PAGE=toc&D=ovft&AN=00024776-000000000-00000'},
            'ajn' : {'title': 'AJN - American Journal of Nursing',  'url': 'http://ovidsp.ovid.com/rss/journals/00000446/current.rss', 'html': 'american_journal_of_nursing.html',       'cover': 'https://ezproxy.ccac.edu/login?url=http://ovidsp.ovid.com/ovidweb.cgi?T=JS&NEWS=n&CSC=Y&PAGE=toc&D=ovft&AN=00000446-000000000-00000'},
            'nmie': {'title': 'Nursing Made Incredibly Easy',       'url': 'http://ovidsp.ovid.com/rss/journals/00152258/current.rss', 'html': 'nursing_made_incredibly_easy.html',      'cover': 'https://ezproxy.ccac.edu/login?url=http://ovidsp.ovid.com/ovidweb.cgi?T=JS&NEWS=n&CSC=Y&PAGE=toc&D=ovft&AN=00152258-000000000-00000'},
            'nur' : {'title': 'Nursing',                            'url': 'http://ovidsp.ovid.com/rss/journals/00152193/current.rss', 'html': 'nursing.html',                           'cover': 'https://ezproxy.ccac.edu/login?url=http://ovidsp.ovid.com/ovidweb.cgi?T=JS&NEWS=n&CSC=Y&PAGE=toc&D=ovft&AN=00152193-000000000-00000'},            
            'mcn' : {'title': 'MCN: American Journal of Maternal Child Nursing', 'url': 'http://ovidsp.ovid.com/rss/journals/00005721/current.rss', 'html': 'mcn.html',                  'cover': 'https://ezproxy.ccac.edu/login?url=http://ovidsp.ovid.com/ovidweb.cgi?T=JS&NEWS=n&CSC=Y&PAGE=toc&D=ovft&AN=00005721-000000000-00000'},
            'hhn' : {'title': 'Home Healthcare Now',                'url': 'http://ovidsp.ovid.com/rss/journals/01845097/current.rss', 'html': 'home_healthcare_now.html',               'cover': 'https://ezproxy.ccac.edu/login?url=http://ovidsp.ovid.com/ovidweb.cgi?T=JS&NEWS=n&CSC=Y&PAGE=toc&D=ovft&AN=01845097-000000000-00000'},
            'dccn': {'title': 'Dimensions of Critical Care Nursing','url': 'http://ovidsp.ovid.com/rss/journals/00003465/current.rss', 'html': 'dimensions_critical_care_nursing.html',  'cover': 'https://ezproxy.ccac.edu/login?url=http://ovidsp.ovid.com/ovidweb.cgi?T=JS&NEWS=n&CSC=Y&PAGE=toc&D=ovft&AN=00003465-000000000-00000'}
            
           }
# Update the permalink in the rss to include the ezproxy server info
def update_permalink(url):
    permalink = url.replace("ovid.com/","ovid.com.ezproxy.ccac.edu/")
    return permalink.replace("https","http")

'''
# Get the URL for the current issue's cover img (e.g., <img src="") based on the issn, date, and issue #
def get_cover_art_url(url):    
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'})
    page = urllib.request.urlopen(req,  timeout=20).read()
    soup = BeautifulSoup(page,'lxml') #xml parser
    srcurl = soup.find_all('div', class_="ejp-footer__smart-control-section-image-container")  
    srcurl = srcurl[0].find('img')
    srcurl = srcurl['src'] 
    return srcurl


# Get the URL for the current issue's cover img (e.g., <img src="") based on the issn, date, and issue #
def get_cover_art_url(url):
     
    #req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'})
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'})
    
    page = urllib.request.urlopen(req,  timeout=20).read()
    soup = BeautifulSoup(page,'lxml') #xml parser
    
    srcurl = soup.find_all('div', class_="ejp-footer__smart-control-section-image-container")    
    srcurl = srcurl[0].find('img')
    srcurl = srcurl['src']
        
    #img src begins with gibberish; find where https begins
    url_start = srcurl.find('https://')
    
    img_url = srcurl[url_start:]
    print("103: " + img_url)
    
    return img_url

def get_cover_art(url, html):
    # this function locates the current cover img and converts it to a base64 string
    # sometimes the remote img urls don't load the image, so this is a workaround that embeds it in our page
    
    img_url = get_cover_art_url(url)
    # get current cover image
    
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    
    output = BytesIO()
    img.save(output, format='JPEG')
    im_data = output.getvalue()
    image_data = base64.b64encode(im_data)
    image_data = image_data.decode()
    image_data = 'data:image/jpg;base64,' + image_data
    return image_data
'''

def get_cover_art_url(url):
     
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'})
    
    page = urllib.request.urlopen(req,  timeout=20).read()
    soup = BeautifulSoup(page,'lxml') #xml parser
    
    srcurl = soup.find_all('div', class_="toc-jtoc-left")
    print( srcurl)    
    srcurl = srcurl[0].find('img')
    srcurl = srcurl['src']
        
    #img src begins with gibberish; find where https begins
    url_start = "https://ovidsp.dc2.ovid.com/ovid-a/"
    
    img_url = url_start + srcurl
    
    return img_url

def get_cover_art(url):
    # this function locates the current cover img and converts it to a base64 string
    # sometimes the remote img urls don't load the image, so this is a workaround that embeds it in our page
    
    img_url = get_cover_art_url(url)
    # get current cover image
    
    response = requests.get(img_url)    
    img = Image.open(BytesIO(response.content))
    
    output = BytesIO()
    img.save(output, format='JPEG')
    im_data = output.getvalue()
    image_data = base64.b64encode(im_data)
    image_data = image_data.decode()
    image_data = 'data:image/jpg;base64,' + image_data  
    return image_data


def format_filename(journal_title, html):
    # this function creates a filename that is unique for each issue
    begin = journal_title.find(")")
    issue_details = journal_title[begin :]
    issue_details = issue_details.replace("/","-")
    issue_details = issue_details.replace(")","-")
    issue_details = issue_details.replace(" ", "")
    
    #update html filename with issue_details
    dot = html.find('.')
    return "toc/" + html[:dot] + issue_details + ".html"
              

def process_rss_feed(title, url, html, cover): 
    # Open RSS feed
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})    
    page = urllib.request.urlopen(req, timeout=20).read() #.decode('utf-8')
    soup = BeautifulSoup(page,'xml') #xml parser
    
    
    # Get journal title & vol info for naming the .html file
    journal_title = soup.title.get_text()
    file_title = format_filename(journal_title, html)
            
    # Check to see if this month's file exists locally. If not, create it
    exists = os.path.isfile(file_title)
    if exists == False:    
        file = open(file_title, 'w', encoding='utf-8')
        file.close()
        
        # Get cover art url for this issue. Get first article fron issue and extract url
        cover_img = get_cover_art(cover)       
                   
        # Open file and write data
        file = open(file_title, 'w', encoding='utf-8')    
        file.write("<div class='journalTitle'>" + journal_title + "</div>\n")
        
        # Find all of the articles and put them in a list
        article_list = soup.find_all('item')
                        
        for item in article_list:        
            article_title = item.title.get_text()
            description = item.description.get_text()
            permalink = update_permalink(item.link.get_text())

            
                
            toc = "<div class='article'><div class='articleTitle'><a target='_blank' href='" + permalink + "'>" + article_title + "</a></div>" + "<div class='articleDesc'>" + description + "</div></div>"            
            file.write(BeautifulSoup(toc, 'html.parser').prettify())
        file.write("<div class='coverImg'><img src='" + cover_img + "'  alt='cover image'></div>" )    
        file.close()
        print(title + "\n") # print the title that was just processed          

for journal, details in journals.items():    
    title = details['title']
    url = details['url']
    html = details['html']
    cover = details['cover']
    process_rss_feed(title,url,html,cover)