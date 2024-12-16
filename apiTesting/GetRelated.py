import re
import requests
import sys
import urllib.parse
import json

def to_related_url(query):
    query=urllib.parse.quote(query)
    query=f"https://sefaria.org/api/related/{query}"
    return query

def to_index_url(query):
    query=urllib.parse.quote(query)
    query=f"https://sefaria.org/api/v2/raw/index/{query}"
    return query
    
def get_related():
    query = sys.stdin.read().strip()
    url=to_related_url(query)
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers).json()
   #response = (f"{response["links"][0]["index_title"]}")
    return response

def get_index(r):
    url=to_index_url(r)
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers).json()
    
def main():
    related = get_related()
    index = get_index(related["links"][0]["index_title"])

    for link in related["links"]:
        print(f"{link["ref"]}")
    
if __name__ == "__main__":
    main()

#What am I doing?

#it takes a verse as input i.e., Genesis 37:2.
#It then finds all of the related texts to the input verse with get_related() and stores them in 
#a variable called related. the variable related["links"[0]["index_title"]] is the title of the 
#related text. related["links"][0]["ref"] is the specific reference i.e., "Rashbam on Genesis 
#37:2:1". 
