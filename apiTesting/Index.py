import re
import requests
import sys
import urllib.parse

def to_related_url(query):
    
    query=urllib.parse.quote(query)
    query=f"https://sefaria.org/api/v2/raw/index/{query}"
    return query
query = sys.stdin.read().strip()
url=to_related_url(query)
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)

print(response.text)
