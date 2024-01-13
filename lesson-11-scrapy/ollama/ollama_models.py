import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta

TEST_FLAG = False 

CATEGORY_DICT = {
    # category_name : list of keywords (lower-cased)
    "code": ["sql", "code", "coder", "coding", "programming",],
    "chinese": ["chinese", "bilingual",],
    "medical": ["medical", "medicine",],
    "math": ["math",],
    "logic": ["logic", "reason",],
} 



def relative_date_to_date_string(relative_date):
    """
    Translates a relative date phrase (e.g., "2 months ago") into a date string in YYYY-MM-DD format.

    Args:
        relative_date (str): The relative date phrase to translate.

    Returns:
        str: The corresponding date string in YYYY-MM-DD format, or None if the input is invalid.
    """

    today = datetime.date.today()
    if relative_date == "yesterday":
        result = today - datetime.timedelta(days=1)        
    else:
        number, unit = relative_date.split()[:2]
        number = int(number)

        if unit == "days":
            result = today - datetime.timedelta(days=number)
        elif unit == "weeks":
            result = today - datetime.timedelta(weeks=number)
        elif unit == "months":
            result = today - relativedelta(months=number)  # Requires the 'dateutil' library
        elif unit == "years":
            result = today - relativedelta(years=number)  # Requires the 'dateutil' library
        else:
            return None  # Invalid input

    return result.strftime("%Y-%m-%d")

if TEST_FLAG:
    rel_dates = ["yesterday"]
    for unit in ["days", "weeks", "months", "years"]:
        rel_dates.append(f"2 {unit} ago")
        
    for x in rel_dates:
        print(f"{x}:\t {relative_date_to_date_string(x)}")

def fix_tags(x):
    return x.replace("&nbsp;", "").replace("Tags", "").strip()

def fix_pull_count(x):
    x = x.replace("Pulls", "").replace(",", "").strip()
    if x.endswith("K"):
        x = x.replace("K", "").strip()
        return int(float(x)*1000)
    else:
        return int(x)

if TEST_FLAG:
    test_inputs = [
        """
        1,570.11K
                Pulls
        """,
        """
        1,570
                Pulls
        """,
        """
        570
                Pulls
        """,
        """
        1,570K
                Pulls
        """,
        """
        70K
                Pulls
        """
    ]    
    for x in test_inputs:
        print(f"[In] {x} : \n[Out] {fix_pull_count(x)}")


def categorize_it(desc, cat_dic=CATEGORY_DICT) -> str:
    """fixed categorization based on keyworkds
    Split description into words and check if words startwith keywork found in cat_dic
    
    Returns:
        comma-sep category names
    """
    res = set()
    words = desc.lower().split()
    for w in words:
        for c in cat_dic.keys():
            for kw in cat_dic[c]:
                if w.startswith(kw):
                    res.add(c)
    return " / ".join(sorted(list(res))) if res else ""

if TEST_FLAG:
    test_inputs = [
        "	An advanced language model crafted with 2 trillion bilingual tokens.",
        "Open-source medical large language model adapted from Llama 2 to the medical domain.",
        "SQLCoder is a code completion model fined-tuned on StarCoder for SQL generation tasks",
        "An expansion of Llama 2 that specializes in integrating both general language understanding and domain-specific knowledge, particularly in programming and mathematics."
    ]

    for desc in test_inputs: 
        print(f"[In] {desc}\n[Out] {categorize_it(desc)}")    

# Send a request to the webpage
url = "https://ollama.ai/library"
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find all model elements

models = soup.find_all("li")

# Create a CSV file and write the header
data = []
header = ["model-name", "description", "tags", "pulls-count", "last-updated", "hf-search_url"]

def fmt_hf_url(model_name):
    return f"""<a href="https://huggingface.co/search/full-text?q={model_name}&type=model">hf-search</a>
    """
# Extract data for each model and write to CSV
for model in models:
    model_name = model.find("h2").text.strip()
    desc = model.find("p", class_="mb-4 max-w-md").text.strip()
    [pulls, tags, relative_date] = [x.text.strip() for x in model.find_all("span")]
    # print(model_name, desc, pulls, tags, relative_date)
    pulls = fix_pull_count(pulls)
    # tags = fix_tags(tags)
    category_tags = categorize_it(desc)
    relative_date = relative_date.replace("Updated", "").strip()
    timestamp = relative_date_to_date_string(relative_date)
    search_url = fmt_hf_url(model_name)
    data.append([model_name, desc, category_tags, search_url, pulls, timestamp])

file_html = "ollama_models.html"
file_csv = "ollama_models.csv"
df = pd.DataFrame(data, columns=header)
df.to_html(file_html, index=False)
df.to_csv(file_csv, index=False)
print(f"Ollama LLM model library saved successfully:\n '{file_html}'\n '{file_csv}'")
