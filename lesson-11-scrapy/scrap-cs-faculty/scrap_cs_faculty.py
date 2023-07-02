
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd 
import xlsxwriter

BROWSER_HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

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
}

SCHOOL_MAP = {
    "UCB": "Univ California Berkeley",
    "MIT": "Massachusetts Institute Technology",
    "CMU": "Carnegie Mellon Univ",
    "UIUC": "Univ Illinois Urbana-Champaign",
    "Stanford": "Stanford Univ",
    "UW": "Univ Washington",
}
DEPT_MAP = {"CS": "Computer Science", 
            "AID": "AI & Decision-making", 
            "AI+D": "AI & Decision-making",
            "EE": "Electrical Engineering", 
            }

COLUMNS = ['name', 'job_title', 'phd_univ', 'phd_year',
           'research_area', 'research_concentration', 'research_focus', 
           'url', 'img_url', 'phone', 'email', 'cell_phone', 'office_address', 
           'department', 'school']

TITLE_WORDS = ["professor", "scientist", "faculty", "lecturer", "researcher", "adjunct", "fellow", "dean", ]

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
