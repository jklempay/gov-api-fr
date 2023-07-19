#!/usr/bin/env python
import requests
import fitz
import os

ENDPOINT_URL = 'https://api.govinfo.gov/published/1936-01-01?offsetMark=*&pageSize=1000&collection=FR&docClass=FR'
CONTENT_URL = 'https://www.govinfo.gov/content/pkg/'
API_KEY = os.environ['GOV_API_KEY']

# Get a list of all issues by looping through all pages of results from API query
print("Getting list of issues...")

url = ENDPOINT_URL + f'&api_key={API_KEY}'
issues = []

while True:
    r = requests.get(url)
    data = r.json()
    issues.extend(package['dateIssued'] for package in data['packages'])
    if data['nextPage']:
        url = data['nextPage'] + f'&api_key={API_KEY}'
    else:
        break
        
# Create data directory
if not os.path.isdir('data'):
  os.mkdir('data')
  
# Get information about the total number of tasks and completed tasks to track progress
total_issues = len(issues)
local_issues = len(os.listdir('data'))

# Extract text from each issue and save to disk
for issue in issues:

    if not os.path.exists(f'data/{issue}.txt'):
    
        url = CONTENT_URL + f'FR-{issue}/pdf/FR-{issue}.pdf'
        r = requests.get(url)
        f = r.content
    
        with fitz.open(stream=f, filetype='pdf') as doc:
            text = ''.join(page.get_text() for page in doc)
            
        with open (f'data/{issue}.txt', 'w', encoding='utf8') as f:
            f.write(text)
      
    local_issues += 1
    print(f"Done with {local_issues} out of {total_issues} issues", end = '\r')
