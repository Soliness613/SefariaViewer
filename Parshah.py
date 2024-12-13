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
