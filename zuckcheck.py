# original script credit: mental#7690
import pytest
import time
import csv
import requests
import pandas
import json

def synonym(customlist, searchterm):
    """Finds synonyms for words from an API."""
    customlist = []
    resp = requests.get('https://api.datamuse.com/words?ml=' + searchterm)
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /' + searchterm + '/ {}'.format(resp.status_code))
    for item in resp.json():
        customlist.append('{}'.format(item['word']))
        customlist.append('{}'.format(item['word']).title())
    return customlist

new_list = []
search_list = []

print("Input words to use as a base list; pass an empty string to begin.")

while "" not in search_list:
    search_list.append(input("Term: ")) # Waits for user to pass an empty string to signal the end of the list
search_list.remove("") # Removes said empty string from the term list prior to generating synonyms

for term in search_list: # Generate list of synonyms from base words
    for item in synonym(new_list, term):
        new_list.append(item)

new_list = list(dict.fromkeys(new_list))
print("Current List Length: "+str(len(new_list))+" word(s)", end="\r")

print("Checking wordlist...") # Performs API call on the zuckwatch password aws bucket to check passwords
for password in new_list:
    response = requests.post('https://k1ozwahixa.execute-api.us-east-1.amazonaws.com/dev/password',json={'password': password})
    if response.status_code != 400:
        print("The password is: " + password, end="\r")
        break

print("No password produced at current settings.", end="\r")
