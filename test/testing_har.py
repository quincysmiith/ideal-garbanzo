import json
from haralyzer import HarParser, HarPage
import urllib.parse
import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open('www.woolworths.com.au.har', 'r') as f:
    #har_parser = HarParser(json.loads(f.read()))
    har_page = HarPage('page_1', har_data=json.loads(f.read()))

post_requests = har_page.post_requests

# filter for adobe calls
# contains https://woolworthsfoodgroup.sc.omtrdc

adobe_hits = []
for request in post_requests:
    if "https://woolworthsfoodgroup.sc.omtrdc" in request["request"]["url"]:
        adobe_hits.append(request)

# text for call
# post_requests[4]["request"]["postData"]["text"]
'''
print(json.dumps(post_requests[4], indent=4))
print()
print()
'''

# decode url characters
# data_sent = urllib.parse.unquote(post_requests[4]["request"]["postData"]["text"])
for adobe_hit in adobe_hits:
    data_sent = urllib.parse.unquote(adobe_hit["request"]["postData"]["text"])
    for i in data_sent.split("&"):
        print(i)


# one method to parse post requests
# another method to parse get requests