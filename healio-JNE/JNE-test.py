# -*- coding: utf-8 -*-
"""
Download current issue of Healio toc (JNE)
Created on Tue Sep 20 09:41:54 2022

@author: cgalluzzo
"""
import urllib.request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import os
'''

urllib2.urlopen(url, "healio.html")
'''
url = "https://journals.healio.com/toc/jne/current"
healio = {'jne' : {'title': 'Journal of Nursing Education', 'html': 'journal_nursing_education.html'} }


def get_jne(url):    
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'})
    page = urllib.request.urlopen(req,  timeout=20).read()
    soup = BeautifulSoup(page,'lxml') #xml parser
    print(soup)
    return soup



def process_rss_feed(title, html):

    # List to hold articles
    articles = []

    # Open html page for parsing
   
    # Get the title
    entries = soup.find_all('section', class_='table-of-content__section')
    
    for item in entries:
        #Get the title, permalink, and authors
        #Load each article into the 'articles' list and then write all of them to the html file
        article_title = item.find('h5', class_='issue-item__title')
        permalink = 'https://journals-healio-com.ezproxy.ccac.edu/doi/' + article_title.contents[0]['id']
        article_title = article_title.get_text()
        

        #Get author names. Some have multiple authors; those go in a list
        authors = item.find('ul', class_='loa').find_all('li') #list of authors
        
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

soup = get_jne(url)
print(soup)

for journal, details in healio.items():
    title = details['title']
    html = details['html']
    process_rss_feed(title,html)