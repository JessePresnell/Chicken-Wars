from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib import urlencode
from urllib import urlencode
import json
import csv
from pprint import pprint
import requests

api_key = 'YOUR KEY HERE'

def geocode(address, api_key):
    results =[]
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'sensor': 'false', 'address': address, 'key': api_key}
    r = requests.get(url, params=params)
    google_payload = r.json()['results']
    # print json.dumps(google_payload, indent=4, sort_keys=True), len(google_payload)
    if len(google_payload) != 0:
        location = google_payload[0]['geometry']['location']
        latitude=location['lat']
        longitude=location['lng']
        accuracy=google_payload[0]['geometry']['location_type']
        print address," @ ", latitude," @ ", longitude," @ ", accuracy
        results.append({'latitude': latitude, 'longitude': longitude, 'accuracy': accuracy})
    else:
        results.append({'latitude': '', 'longitude': '', 'accuracy': 'no match'})
    return results[0]

def get_chickfila_locations():
    url = "https://www.chick-fil-a.com/Locations/Browse/NC"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    address_divs = driver.find_elements_by_css_selector(".location")
    locations = []
    for address in address_divs:
        location = dict()
        location['name'] = address.find_element_by_css_selector("h2 > a").text
        location_details = address.find_element_by_css_selector("p").text
        location['street'] = location_details.split("\n")[0]
        location['csz'] = location_details.split("\n")[1]
        location['address'] = location['street']+" "+location['csz']
        results = geocode(location['address'])
        location['latitude'] = results['latitude']
        location['longitude'] = results['longitude']
        location['accuracy'] = results['accuracy']
        locations.append(location)
        keys = locations[0].keys()
        with open('chickfila.csv', 'wb') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(locations)

def get_bojangles_locations():
    with open('Bojangles.json') as f:
        data = json.load(f)
    pprint(data)
    locations = []
    for store in data['locs']:
        locations.append(store)
    keys = locations[0].keys()
    with open('bojangles.csv', 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(locations)

def get_kfc_locations():
    with open('kfc.json') as f:
        data = json.load(f)
    pprint(data)
    locations = []
    for store in data['results']:
        locations.append(store)
    keys = locations[0].keys()
    with open('kfc.csv', 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(locations)



