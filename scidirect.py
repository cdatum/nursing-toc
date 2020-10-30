# -*- coding: utf-8 -*-
"""
Created on Thu Jul  22 09:46:26 2020

@author: Christopher Galluzzo
Import RSS feeds from Science Direct and parse the table of contents into HTML
"""

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import os


'''
Scidirect XML
<?xml version="1.0" encoding="UTF-8"?>
<rss
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:content="http://purl.org/rss/1.0/modules/content/"
  xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
  <channel>
    <title>
      <![CDATA[ScienceDirect Publication: Clinical Simulation in Nursing]]>
    </title>
    <description>
      <![CDATA[ScienceDirect RSS]]>
    </description>
    <link>https://www.sciencedirect.com/journal/clinical-simulation-in-nursing</link>
    <generator>RSS for Node</generator>
    <lastBuildDate>Wed, 22 Jul 2020 09:11:55 GMT</lastBuildDate>
    <copyright>
      <![CDATA[Copyright © 2020 International Nursing Association for Clinical Simulation and Learning. All rights reserved]]>
    </copyright>
    <item>
      <title>
        <![CDATA[Improving Safety of Patients With Autism Spectrum Disorder Through Simulation]]>
      </title>
      <description>
        <![CDATA[<p>Publication date: August 2020</p><p><b>Source:</b> Clinical Simulation in Nursing, Volume 45</p><p>Author(s): Constance E. McIntosh, Cynthia M. Thomas</p>]]>
      </description>
      <link>https://www.sciencedirect.com/science/article/pii/S1876139919302452?dgcid=rss_sd_all</link>
      <guid isPermaLink="false">https://www.sciencedirect.com/science/article/pii/S1876139919302452</guid>
    </item>

'''

# SciDirect for Clinical Simulation in Nursing
# https://ezproxy.ccac.edu/login?url=https://www.sciencedirect.com/journal/clinical-simulation-in-nursing
# https://www.sciencedirect.com/science/article/pii/S1876139920300402?dgcid=rss_sd_all
# https://www-sciencedirect-com.ezproxy.ccac.edu/science/article/pii/S1876139920300426

# Set the URLs to open

scidirect = {'csn' : {'title': 'Clinical Simulation in Nursing',    'url': 'http://rss.sciencedirect.com/publication/science/18761399', 'html': 'clinical_simulation_nursing.html'} }


# Update the permalink in the rss to include the ezproxy server info
def update_permalink(url):
    permalink = url.replace("https://www.sciencedirect.com","https://www-sciencedirect-com.ezproxy.ccac.edu")
    return permalink

# Extract the authors from the xml description
def parse_author(description):
    # find the beginning & end of the authors section
    author_begin = description.find("Author(s): ")
    author_end = len(description)
    # extract the range. Add 11 chars to beginning and remove 4 from end
    author = description[author_begin + 11:author_end - 4]
    
    return author

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
              

def process_rss_feed(title, url, html):    
    # Open RSS feed    
    url = "http://rss.sciencedirect.com/publication/science/18761399"
    req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page,'xml') #xml parser
    #print(soup)

    # Get journal title & vol info for naming the .html file 
    journal_title = soup.title.get_text()
    file_title = format_filename(journal_title, html)   
    page = soup.find_all('item')
    
    
    # Check to see if file exists locally. If not, create it
    exists = os.path.isfile(html)
    if exists == False:    
        file = open(html, 'w', encoding='utf-8')
        file.close()
            
    # Open file and write data
    file = open(html, 'w', encoding='utf-8')  
    file.write("<div class='journalTitle'>" + journal_title + "</div>\n")
            
    for item in page:        
        article_title = item.title.get_text()
        permalink = update_permalink(item.link.get_text())
        description = item.description.get_text()
        author = parse_author(description)
                            
        toc = "\n<div class='article'><div class='articleTitle'><a target='_blank' href='" + permalink + "'>" + article_title + "</a></div>" + "<div class='articleDesc scidirectDesc'><div class='author'><span>" + author + "</span></div></div></div>\n"            
        file.write(BeautifulSoup(toc, 'html.parser').prettify())
    file.close()          

for journal, details in scidirect.items():    
    title = details['title']
    url = details['url']
    html = details['html']
    process_rss_feed(title,url,html)