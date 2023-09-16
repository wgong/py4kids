import re
import requests
from bs4 import BeautifulSoup
import pandas as pd 
import xlsxwriter
from scholarly import scholarly
from time import sleep
from random import randint 
from pathlib import Path
import duckdb
from datetime import datetime 


BROWSER_HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

LANG = "en"
SCHOOL_DICT = {
    "Cornell-CS": {
        "url": "https://www.cs.cornell.edu/people/faculty",
    },
    "UIUC-CS": {
        "url": "https://cs.illinois.edu/about/people/department-faculty",
    },
    "MIT-AID": {
        "url": "https://www.eecs.mit.edu/role/faculty-aid/",
    },
    "MIT-CS": {
        "url": "https://www.eecs.mit.edu/role/faculty-cs/",
    },
    "CMU-CS": {
        "url": "https://csd.cmu.edu/people/faculty",
    },
    "UCB-CS": {
        "url": "https://www2.eecs.berkeley.edu/Faculty/Lists/CS/faculty.html",
    },
    "Stanford-CS": {
        "url": "https://cs.stanford.edu/directory/faculty",
    },
    "Princeton-CS": {
        "url": "https://www.cs.princeton.edu/people/faculty?type=main",
    },
    "UWash-CS": {
        "url": "https://www.cs.washington.edu/people/faculty",
    },
    "UPenn-CS": {
        "url": "https://directory.seas.upenn.edu/computer-and-information-science/",
    },
    "CalTech-CS": {
        "url": "https://www.cms.caltech.edu/cms-people/faculty",
    },
    "Harvard-CS": {
        "url": "https://seas.harvard.edu/computer-science/people?role[46]=46",
    },

    "Google-Scholar": {
        "url": "https://scholar.google.com"
    }
}

SCHOOL_MAP = {
    "UCB": "Univ California Berkeley",
    "MIT": "Massachusetts Institute Technology",
    "CMU": "Carnegie Mellon Univ",
    "UIUC": "Univ Illinois Urbana-Champaign",
    "Stanford": "Stanford Univ",
    "Princeton": "Princeton Univ",
    "UWash": "Univ Washington",
    "UPenn": "Univ Pennsylvania",
    "Harvard": "Harvard Univ",
    "CalTech": "California Institute of Technology",
}
DEPT_MAP = {
    "CS": "Computer Science", 
    "AID": "AI & Decision-making", 
    "AI+D": "AI & Decision-making",
    "EE": "Electrical Engineering", 
}

# Top 6 schools
COLUMNS = ['name', 'job_title', 'phd_univ', 'phd_year',
           'research_area', 'research_concentration', 'research_focus', 
           'url', 'img_url', 'phone', 'email', 'cell_phone', 'office_address', 
           'department', 'school']

# other schools, added url_profile column
COLUMNS_v2 = ['name', 'job_title', 'phd_univ', 'phd_year',
           'research_area', 'research_concentration', 'research_focus', 
           'url', 'img_url', 'phone', 'email', 'cell_phone', 'office_address', 
           'department', 'school', 'url_profile', 'url_author']

TITLE_WORDS = ["professor", "scientist", "faculty", "lecturer", "researcher", "adjunct", "fellow", "dean", ]

SCHOLAR_HEADER = [
    'name',             # scholar full name
    'affiliation',      # school
    'interests',        # research interest listed at Google scholar profile
    'num_papers',       # paper count, detailed list is stored in .json file
    'num_coauthors',    # co-author count
    'citedby',          # total citedBy count
    'hindex',           # h-index of lifetime
    'i10index',         # i10-index - at least 10 citations
    'citedby5y',        # citedBy count in past 5 years
    'hindex5y',         # h-index of past 5 years
    'i10index5y',       # i10-index of past 5 years
    'scholar_id',       # unique system ID at Google scholar website
    'url_author',       # scholar profile URL
    'url_picture',      # scholar profile image URL
    'url_homepage',     # scholar personal website
    'file_author'       # json file saved locally for future streamlit app
]

def is_job_title(title):
    res = False
    for x in TITLE_WORDS:
        if x in title:
            res = True
            break
    return res

def map_school_dept(alias):
    x = alias.split("-")
    return SCHOOL_MAP.get(x[0],""), DEPT_MAP.get(x[1],"")

def parser_dummy():
    pass

for k in SCHOOL_DICT.keys():
    SCHOOL_DICT[k]["parser"] = parser_dummy

def uiuc_fix_url(url, base_url="https://cs.illinois.edu/about/people/department-faculty"):
    uid = url.split("/")[-1]
    return f"{base_url}/{uid}"

def uiuc_match_img_url(img, protocol="https"):
    z = re.match(r"^background-image: url\((.*)\)$", img)
    return f"{protocol}:{z.groups()[0]}" if z else ""

def cornell_parse_dept_phd(dept_edu):
    dept_edu = dept_edu.replace(".","").replace(" (Operations Research)", "").strip()
    
    words = re.split(r";|,| ", dept_edu)
    words = [w.strip() for w in words if w.strip()]
    
    ipos_phd = -1
    for n, x in enumerate(words):
        if x.lower() == "phd":
            ipos_phd = n 
            break
            
    try:
        phd_year = str(int(words[-1].strip()))
    except:
        phd_year = ""
    
    if ipos_phd > -1:
        dept = " ".join(words[:ipos_phd]).strip()
        univ_year = " ".join(words[ipos_phd+1:])
        phd_univ = univ_year.replace(phd_year, "").strip() if phd_year else univ_year
        
        # fix univ
        phd_univ = phd_univ[:-1] if phd_univ.endswith(",") else phd_univ
        phd_univ = phd_univ.replace(" of", "").replace(" at ", " ").replace(" - ", " ")
        phd_univ = phd_univ.replace('Massachusetts Institute Technology', "MIT") if 'Massachusetts Institute Technology' in phd_univ else phd_univ
        phd_univ = phd_univ.replace('UC Berkeley', "University California Berkeley") if 'UC Berkeley' in phd_univ else phd_univ
        phd_univ = phd_univ.replace('Pennsylvaniasylvania', "Pennsylvania").replace('UPenn', "University Pennsylvania").replace('Univ Penn', "University Pennsylvania")
        phd_univ = phd_univ.replace("University", "Univ") if "University" in phd_univ else phd_univ
        phd_univ = phd_univ.replace("Ausin", "Austin") if "Ausin" in phd_univ else phd_univ
        phd_univ = phd_univ.replace("Univ Massachusetts Amherst", "Univ Mass Amherst") if "Univ Massachusetts Amherst" in phd_univ else phd_univ

    else:
        dept = dept_edu
        phd_univ = ""
        phd_year = ""
    
    return dept, phd_univ, phd_year

def normalize_str(text, non_alpha_numeric=r'[^a-z0-9]', sep="_"):
    # Replace all non-alphanumeric chars with underscores
    words = re.sub(non_alpha_numeric, sep, text.lower()).split(sep)
    return sep.join([w for w in words if w])
    
def get_scholar_page(scholar_id, base_url=SCHOOL_DICT["Google-Scholar"]["url"], lang=LANG):
    return f"{base_url}/citations?user={scholar_id}&hl={lang}&oi=ao" if scholar_id else ""

def pick_name_from_profile_url(url):
    """
    UPenn profile URL is always present with name
    used it to recover Name when missing
    """
    name = [i.strip() for i in url.split("/") if i.strip()][-1]
    cap_ed = [i.strip().capitalize() for i in name.split("-") if i.strip()]
    return " ".join(cap_ed)