import urllib
import ipaddress
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import *
from sklearn.pipeline import Pipeline,make_pipeline
from sklearn.metrics import classification_report
#------------------------------URL lenght------------------------------
def url_len_(lien):
    # print ("\t url lenght")
    return len(lien)

#--------------------------shortening services-------------------------
def shortening_services(lien):
    # print("\t shortinig services")
    match=re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                    'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                    'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                    'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                    'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                    'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                    'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net',lien)
    if match:
        return 0
    else:
        return 1

#----------------------------prefix & suffix---------------------------
def prefix_suffix(lien):
    # print("\t prefix ens suffix")
    lien=urllib.parse.urlsplit(lien)
    if lien.hostname.count("-"):
        return 0
    else:
        return 1

#------------------------------HTTPS token------------------------------
def https_token(lien):
    # print("\t https token")
    if "https://" in lien:
        return 1
    else :
        return 0



#---------------------------iFrame redirection-------------------------
def iframe(response):
    # print("iframe")
    if response == "":
        return 0
    else:
        if response.text.find(r"[<iframe>|<frameBorder>]"):
            return 1
        else:
            return 0
#--------------------------anchor tag---------------------------------
def Anchor_Tag(lien, soup, domain):
    # print("anchor tag")
    i = 0
    unsafe = 0
    for a in soup.find_all('a', href=True):
        if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (
                lien in a['href'] or domain in a['href']):
            unsafe = unsafe + 1
        i = i + 1
    try:
        percentage = unsafe / float(i)
        return percentage
    except Exception:
        return 0

#------------------------------favicon-----------------------------
def Favicon(lien, soup, domain):
    # print("favicon")
    for head in soup.find_all('head'):
        for head.link in soup.find_all('link', href=True):
            dots = [x.start() for x in re.finditer(r'\.', head.link['href'])]
            return 1 if lien in head.link['href'] or len(dots) == 1 or domain in head.link['href'] else 0
    return 1
#-------------------------------SFH---------------------------------
def SFH(lien, soup, domain):
    # print("SFH")
    for form in soup.find_all('form', action=True):
        if form['action'] == "" or form['action'] == "about:blank":
            return 0
        elif lien not in form['action'] and domain not in form['action']:
            return 0
        else:
            return 1
    return 1

#-------------------------request url--------------------------------
def Request_Url(lien, soup, domain):
    # print("request URL")
    i = 0
    success = 0
    for img in soup.find_all('img', src=True):
        dots = [x.start() for x in re.finditer(r'\.', img['src'])]
        if lien in img['src'] or domain in img['src'] or len(dots) == 1:
            success = success + 1
        i = i + 1

    for audio in soup.find_all('audio', src=True):
        dots = [x.start() for x in re.finditer(r'\.', audio['src'])]
        if lien in audio['src'] or domain in audio['src'] or len(dots) == 1:
            success = success + 1
        i = i + 1

    for embed in soup.find_all('embed', src=True):
        dots = [x.start() for x in re.finditer(r'\.', embed['src'])]
        if lien in embed['src'] or domain in embed['src'] or len(dots) == 1:
            success = success + 1
        i = i + 1

    for i_frame in soup.find_all('i_frame', src=True):
        dots = [x.start() for x in re.finditer(r'\.', i_frame['src'])]
        if lien in i_frame['src'] or domain in i_frame['src'] or len(dots) == 1:
            success = success + 1
        i = i + 1

    try:
        percentage = success / float(i)
        return percentage
    except Exception:
        return 0


# -----------------------------linkd in tag -----------------------

def Links_In_Tags(lien, soup, domain):
    # print("links in tags")
    i = 0
    success = 0
    for link in soup.find_all('link', href=True):
        dots = [x.start() for x in re.finditer(r'\.', link['href'])]
        if lien in link['href'] or domain in link['href'] or len(dots) == 1:
            success = success + 1
        i = i + 1

    for script in soup.find_all('script', src=True):
        dots = [x.start() for x in re.finditer(r'\.', script['src'])]
        if lien in script['src'] or domain in script['src'] or len(dots) == 1:
            success = success + 1
        i = i + 1
    try:
        percentage = success / float(i)
        return percentage
    except Exception:
        return 0





def FeaturesExtraction(lien,response):
    features=[]

    # url_length,
    features.append(url_len_(lien))
    # tiny_url,
    features.append(shortening_services(lien))
    # pref_suf,
    features.append(prefix_suffix(lien))
    # https_token,
    features.append(https_token(lien))


    # iframe,
    features.append(iframe(response))

    soup=BeautifulSoup(response.content,'html.parser')

    # anchor_tag,
    features.append(Anchor_Tag(lien,soup, urlparse(lien).hostname))
    # Favicon,
    features.append(Favicon(lien,soup, urlparse(lien).hostname))
    # SFH,
    features.append(SFH(lien,soup, urlparse(lien).hostname))
    # requestURL,
    features.append(Request_Url(lien,soup, urlparse(lien).hostname))
    # LinksInTags
    features.append(Links_In_Tags(lien,soup, urlparse(lien).hostname))
 

    
    return features
