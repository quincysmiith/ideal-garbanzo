import json
from haralyzer import HarParser, HarPage
import urllib.parse

with open('www.woolworths.com.au.har', 'r') as f:
    #har_parser = HarParser(json.loads(f.read()))
    har_page = HarPage('page_1', har_data=json.loads(f.read()))

post_requests = har_page.post_requests

# filter for adobe calls
# contains https://woolworthsfoodgroup.sc.omtrdc

# text for call
post_requests[4]["request"]["postData"]["text"]

# decode url characters
data_sent = urllib.parse.unquote(post_requests[4]["request"]["postData"]["text"])

for i in data_sent.split("&"):
    print(i)