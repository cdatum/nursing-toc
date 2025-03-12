# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 13:35:16 2024

@author: Christopher Galluzzo
Import RSS feeds from Ovid and parse the table of contents into HTML
Updated for new 2025 title list
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

journals = {
'anc' :{'id':'00149525','title':'Advances in Neonatal Care','html':'advances_in_neonatal.html'},
'ans' :{'id':'00012272','title':'Advances in Nursing Science','html':'advances_in_nursing_science.html'},
'cin' :{'id':'00024665','title':'CIN: Computers, Informatics, Nursing','html':'CIN.html'},
'hmr' :{'id':'00004010','title':'Health Care Management Review','html':'health_care_mgt_review.html'},
'jona':{'id':'00005110','title':'JONA: Journal of Nursing Administration','html':'JONA.html'},
'jcn' :{'id':'00005082','title':'Journal of Cardiovascular Nursing','html':'journal_cardiovascular_nursing.html'},
'jhpn':{'id':'00129191','title':'Journal of Hospice & Palliative Nursing','html':'journal_hospice_pallliative_nursing.html'},
'jin' :{'id':'00129804','title':'Journal of Infusion Nursing','html':'journal_infusion_nursing.html'},
'jncq':{'id':'00001786','title':'Journal of Nursing Care Quality','html':'journal_nursing_care_quality.html'},
'ne'  :{'id':'00006223','title':'Nurse Educator','html':'nurse_educator.html'},
'nmgt':{'id':'00006247','title':'Nursing Management','html':'nursing_mgt.html'},
'orth':{'id':'00006416','title':'Orthopaedic Nursing','html':'orthopaedic_nursing.html'},
'prof':{'id':'01269241','title':'Professional Case Management','html':'professional_case_mgt.html'},
'nep' :{'id':'00024776','title':'Nursing Education Perspectives','html':'nursing_education_perspectives.html'},
'ajn' :{'id':'00000446','title':'AJN - American Journal of Nursing','html':'american_journal_of_nursing.html'},
'nmie':{'id':'00152258','title':'Nursing Made Incredibly Easy','html':'nursing_made_incredibly_easy.html'},
'nur' :{'id':'00152193','title':'Nursing','html':'nursing.html'},
'mcn' :{'id':'00005721','title':'MCN: American Journal of Maternal Child Nursing','html':'mcn.html'},
'hhn' :{'id':'01845097','title':'Home Healthcare Now','html':'home_healthcare_now.html'},
'dccn':{'id':'00003465','title':'Dimensions of Critical Care Nursing','html':'dimensions_critical_care_nursing.html'}

    }



# Update the permalink in the rss to include the ezproxy server info
def update_permalink(url):
    #permalink = url.replace("ovid.com/","ovid.com.ezproxy.ccac.edu/")
    permalink = url.replace("https","https://ezproxy.ccac.edu/login?url=https")
    return permalink
    #return permalink.replace("https","http")


def get_cover_art_url(url):   
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'})    
    page = urllib.request.urlopen(req,  timeout=20).read()
    soup = BeautifulSoup(page,'lxml') #xml parser     
    
    try:
        srcurl = soup.find_all('div', class_="toc-jtoc-left")      
        srcurl = srcurl[0].find('img')
        srcurl = srcurl['src']
        
        #img src begins with gibberish; find where https begins
        url_start = "https://ovidsp.dc2.ovid.com/ovid-a/"
        
        img_url = url_start + srcurl
        return img_url
    
    except:
        print("Cover image not found ")
        return "Image not found"
        
    
    

def get_cover_art(url):
    # this function locates the current cover img and converts it to a base64 string
    # sometimes the remote img urls don't load the image, so this is a workaround that embeds it in our page
    
    img_url = get_cover_art_url(url)
    # get current cover image
    print("img_url: " + img_url)
    
    if (img_url != "Image not found"):
        response = requests.get(img_url)    
        img = Image.open(BytesIO(response.content))
        
        output = BytesIO()
        img.save(output, format='JPEG')
        im_data = output.getvalue()
        image_data = base64.b64encode(im_data)
        image_data = image_data.decode()
        image_data = 'data:image/jpg;base64,' + image_data  
        return image_data
    else:
        return "https://libguides.ccac.edu"


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
              
# this is the main function that processes the items in the 'journals' variable [list]
def process_rss_feed(title, journal_id, html): 
    
    #Setup urls for rss and cover art
    url = "https://ovidsp.ovid.com/rss/journals/" + journal_id + "/current.rss"
    cover_url = "https://ezproxy.ccac.edu/login?url=https://ovidsp.ovid.com/ovidweb.cgi?T=JS&NEWS=n&CSC=Y&PAGE=toc&D=ovft&AN=" + journal_id + "-000000000-00000"
    
 
    # Open RSS feed
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})    
    page = urllib.request.urlopen(req, timeout=20).read() #.decode('utf-8')
    soup = BeautifulSoup(page,'xml') #xml parser
    #print(title)
    
    # Get journal title & vol info for naming the .html file
    journal_title = soup.title.get_text()
    file_title = format_filename(journal_title, html)
            
    # Check to see if this month's file exists locally. If not, create it
    exists = os.path.isfile(file_title)
    if exists == False:    
        file = open(file_title, 'w', encoding='utf-8')
        file.close()
        
        # Get cover art url for this issue. Get first article fron issue and extract url
        cover_img = get_cover_art(cover_url)  
        
                   
        # Open file and write data
        file = open(file_title, 'w', encoding='utf-8')    
        file.write("<div class='journalTitle'>" + journal_title + "</div>\n")
        
        # Find all of the articles and put them in a list
        article_list = soup.find_all('item')
                        
        for item in article_list:        
            article_title = item.title.get_text()
            description = item.description.get_text()
            permalink = update_permalink(item.link.get_text())
              
                
            toc = "<div class='article'><div class='articleTitle'><a target='_blank' href='" + permalink + "' aria-label='" + article_title + " - opens in new window'>" + article_title + "</a></div>" + "<div class='articleDesc'>" + description + "</div></div>"            
            file.write(BeautifulSoup(toc, 'html.parser').prettify())
        file.write("<div class='coverImg'><img src='" + cover_img + "'  alt='cover image'></div>" )    
        file.close()
        print(title + "\n") # print the title that was just processed          

'''
for journal, details in journals.items():    
    title = details['title']
    url = details['url']
    html = details['html']
    cover = details['cover']
    process_rss_feed(title,url,html,cover)
'''
for journal, details in journals.items():    
    title = details['title']
    journal_id = details['id']
    html = details['html']    
    process_rss_feed(title,journal_id,html)
