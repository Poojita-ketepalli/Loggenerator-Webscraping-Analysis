import requests
from bs4 import BeautifulSoup
import time
import json
import re

#Retry mechanism and data scraping function
def fetch_data_with_retries(url,retries=3,delay=2):
    """
    Fetches data from a URL with retries in case of failure
    """
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt+1} failed: {e}")
            if attempt<retries-1:
                time.sleep(delay*(attempt+1)) #Exponential backoff
            else:
                raise

# Function to extract data using BeautifulSoup4 and regular Expressions
def extract_data_from_html(html_content):
    """
    Extracting the relevant data (Eg:links containing 'python' from the html content)
    """
    if not html_content:
        raise ValueError("HTML content is invalid or empty!!")
    soup = BeautifulSoup(html_content,'html.parser')
    titles = []

    # RegularExpression to find all the links with specific text (python)
    for link in soup.find_all('a',href=True):
        title = link.get_text()
        if(re.match(r'.*python.*',title,re.IGNORECASE)): # Looking for link containing python
            titles.append(title)

    return titles

# Function to ave the data into json file
def save_data_to_json(data,filename="scrapped_data.json"):
    """
    Saves the extracted data to a JSON file
    """
    try:
        with open(filename,'w') as file:
            json.dump(data,file,indent=2)
        print(f"data have been saved to {filename}")
    except Exception as e:
        print(f"Error in saving data to the file: {e}")

# URL to scrape
url = "https://docs.python.org/3/"

# Fetch, extract and save data
html_content = fetch_data_with_retries(url)
extracted_data = extract_data_from_html(html_content)
save_data_to_json(extracted_data) 