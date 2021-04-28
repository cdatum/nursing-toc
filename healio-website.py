# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 11:43:37 2021

@author: cgalluzzo
"""

# This script scrapes the Healio current table of contents
# Healio website https://journals.healio.com/toc/jne/60/4

import urllib.request
from bs4 import BeautifulSoup
import os



# Healio -Journal of Nursing Education: https://www.healio.com/sws/feed/journal/jne
# https://www-healio-com.ezproxy.ccac.edu/
# https://www-healio-com.ezproxy.ccac.edu/nursing/journals/jne/2020-7-59-7/9d200cd8-06cd-44b3-8f29-31377ffaaa17/using-social-media-to-engage-nurse-practitioner-students-in-complex-health-care-topics

# Set the URLs to open

healio = {'jne' : {'title': 'Journal of Nursing Education',    'url': 'healio.html', 'html': 'journal_nursing_education.html'} }


def process_rss_feed(title, url, html):

    # List to hold articles
    articles = []
    
    # Open html page for parsing 
    page = open(url, 'r', encoding='utf-8') 
    soup = BeautifulSoup(page,'lxml') #xml parser
    page.close()
    
    # Get the title    
    entries = soup.find_all('section', class_='table-of-content__section')
    
    for item in entries:
        #Get the title, permalink, and authors
        #Load each article into the 'articles' list and then write all of them to the html file
        article_title = item.find('h5', class_='issue-item__title')
        permalink = 'https://journals-healio-com.ezproxy.ccac.edu' + article_title.contents[0]['href']                  
        article_title = article_title.get_text()
        
        #Get author names. Some have multiple authors; those go in a list
        authors = item.find('ul', class_='loa').find_all('li') #list of authors     
        names = ''        
        for author in authors:
            #names.append(author.get_text())
            names += author.get_text()
              
        toc = "\n<div class='article'><div class='articleTitle'><a target='_blank' href='" + permalink + "'>" + article_title + "</a></div>" + "<div class='articleDesc'>" + "<div class='author'><span>" + names + "</span></div></div></div>\n"            
        articles.append(toc)
    
    
    # Check to see if the output file exists locally. If not, create it
    exists = os.path.isfile(html)
    if exists == False:    
        file = open(html, 'w', encoding='utf-8')
        file.close()
            
    # Open file and write data
    file = open(html, 'w', encoding='utf-8')    
    file.write("<div class='journalTitle'>" + title + "</div>\n")
    
    # write each article to the html file
    for entry in articles:
        file.write(BeautifulSoup(entry, 'html.parser').prettify())
    file.close() 
    


for journal, details in healio.items():    
    title = details['title']
    url = details['url']
    html = details['html']
    process_rss_feed(title,url,html)