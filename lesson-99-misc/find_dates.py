"""
pip install dateparser dateutils
"""
from datetime import datetime
import re
from dateutil import parser
from dateparser.search import search_dates

_DATE_FORMAT = re.compile("((\d{4}[-/]\d{1,2}[-/]\d{1,2})|(\d{1,2}/\d{1,2}/\d{4})|((?:JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)(?:[\.]?|[A-Z]+)\s*[\d]{1,2}\s*,\s*[\d]{4}))")

def find_dates(s):
    """find dates in a string and return a list of date-string like "YYYYMMDD" 
    
    >>> d = "September 9, 1999  08/09/2000  8/8/2021 - 10/27/2021  2022-07-04  2022-7-5  2022/07/01  2022/7/7  Jul 4, 1980 july 14, 2011, August 18, 2021"
    >>> find_dates(d)
    ['19800704', '19990909', '20000809', '20110714', '20210808', '20210818', '20211027', '20220701', '20220704', '20220705', '20220707']
        
    """
    s_new = s.upper().replace(",", " , ") # dateutil.parser.parse() fail to handle 'may13,2021'

    # exact match
    dates = []
    for dt in _DATE_FORMAT.findall(s_new):
        dates.extend([d for d in dt if d])

    # fuzzy match
    for d in dates:
        s_new = s_new.replace(d, "")   # remove exact-matched date-string        
    dt_extra = search_dates(s_new.strip())
    dates_extra = [dt[1] for dt in dt_extra] if dt_extra else []
        
    return [datetime.strftime(dt, '%Y%m%d') for dt in sorted(list(set([parser.parse(d) for d in dates] + dates_extra)))]

if __name__ == "__main__":
    d = "September 9, 1999  08/09/2000  8/8/2021 - 10/27/2021  2022-07-04  2022-7-5  2022/07/01  2022/7/7  Jul 4, 1980 july 14, 2011, August 18, 2021"
    print(find_dates(d))