import requests

url = "https://sefaria.org/api/calendars"

response = requests.get(url)

data = response.json()

calendar_items = data['calendar_items']

for item in calendar_items:
    if item['title']['en'] == 'Parashat Hashavua':
        parasha_ref = item['ref']
        parasha_name = item['displayValue']['en']

print(parasha_ref)
print(parasha_name)

parasha_ref = parasha_ref.split("-")[0]
print(parasha_ref)

he_vtitle = data['versions'][0]['versionTitle']
he_pasuk = data['versions'][0]['text']

url = f"https://www.sefaria.org/api/related/{parasha_ref}"

response = requests.get(url)

data = response.json

commentaries = []

for linked_text in data["links"]:
    if linked_text['type'] == 'commentary':
        commentaries.append(linked_text['ref'])
