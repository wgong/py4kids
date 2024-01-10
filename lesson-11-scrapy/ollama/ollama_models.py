import requests
from bs4 import BeautifulSoup
import csv
import datetime
from dateutil.relativedelta import relativedelta

TEST_FLAG = False 

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

# Send a request to the webpage
url = "https://ollama.ai/library"
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find all model elements

models = soup.find_all("li")

# Create a CSV file and write the header
with open("ollama_models.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["model-name", "description", "pulls-count", "tags-count", "last-updated"])

    # Extract data for each model and write to CSV
    for model in models:
        name = model.find("h2").text.strip()
        desc = model.find("p", class_="mb-4 max-w-md").text.strip()
        [pulls, tags, relative_date] = [x.text.strip() for x in model.find_all("span")]
        # print(name, desc, pulls, tags, relative_date)
        pulls = fix_pull_count(pulls)
        tags = fix_tags(tags)
        relative_date = relative_date.replace("Updated", "").strip()
        timestamp = relative_date_to_date_string(relative_date)
        writer.writerow([name, desc, pulls, tags, timestamp])

print("CSV file created successfully!")
