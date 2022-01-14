# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 11:43:37 2021

@author: cgalluzzo
"""

# This script scrapes the Healio site for current table of contents (they discontinued the RSS)
# Healio website https://journals.healio.com/toc/jne/60/4

import urllib.request
from bs4 import BeautifulSoup
import os

'''
Directions:

    1. Download the current table of contents page ("Save page as...") from the healio site (https://journals.healio.com/toc/jne/current) as 'healio.html'
    2. Place the healio.html file in the same directory as this script
    3. Run script
    4. View the resulting html in journal_nursing_education.html

'''
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
        print(len(authors))
        names = ''
        
        # if an article doesn't have authors, this might throw an error. Just erase the article from the healio.html file or insert placeholder
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


print ("Instructions: 1: Download webpage at https://journals.healio.com/toc/jne/current")
print ("2: Save it as 'healio.html' ")
print ("3: run this script then open journal_nursing_education.html to access the HTML")
for journal, details in healio.items():
    title = details['title']
    url = details['url']
    html = details['html']
    process_rss_feed(title,url,html)
