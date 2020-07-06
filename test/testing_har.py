import json
from haralyzer import HarParser, HarPage
import urllib.parse
import os
import re
from datetime import datetime
from dateutil import parser

#os.chdir(os.path.dirname(os.path.realpath(__file__)))


def parse_query_string(query_parameters: str) -> dict:
    """Converts a string that contains query parameters to a dictionary.
    Key value pairs must be seperated by "&"
    Keys and values must be seperated by "="

    Args:
        query_parameters (str): [description]

    Returns:
        dict: dictionary object representing the key value pairs from the original input
        string.
    """

    return_dict = {}

    for i in query_parameters.split("&"):
        #print(i)
        items = i.split("=", 1)
        #print(items)
        try:
            key = items[0]
            value = urllib.parse.unquote(items[1])
            if key == "t":
                value = parser.parse(value[:-7])
            return_dict.update({key: str(value)})
        except:
            pass
            #print("Failed to add to dict:")
            #print(items)
        #print()

    try:
        my_product_dict = parse_product_list(return_dict["products"])
        return_dict.update({"products" : my_product_dict})
    except:
        pass

    return return_dict


def parse_product_list(product_string: str) -> dict:
    """[summary]

    Args:
        product_string (str): [description]

    Returns:
        dict: [description]
    """

    main_dict = {}
    for num, i in enumerate(product_string.split(",")): 
        
        item_dict = {}
        
        if len(i.split(";;")) == 3:
            a_list = i.split(";;")
            item_dict.update({"Product":a_list[0]})
            item_dict.update({"Price":a_list[1]})

            #print(a_list[2])

            evar_list = a_list[2].split("|")

            evar_dict = {}
            for evar in evar_list:
                try:
                    items = evar.split("=", 1)
                    evar_dict.update({items[0] : items[1]})
                except:
                    pass
                    #print("Failed to parse")
                    #print(items)
            
            

        if len(i.split(";;")) == 1:
            a_list = i.split("|")
            item_dict.update({"Category" : a_list[0]})

            evar_list = a_list[1:]

        evar_dict = {}
        for evar in evar_list:
            try:
                items = evar.split("=", 1)
                evar_dict.update({items[0] : items[1]})
            except:
                print("Failed to parse")
                print(items)

        item_dict.update({"eVars" : evar_dict})

        main_dict.update({num : item_dict})


    return main_dict

### MAIN WORK ###

list_to_print = []

with open('woolworths_20200706_chicken_search.har', 'r') as f:
    har_parser = HarParser(json.loads(f.read()))
    #har_page = HarPage('page_1', har_data=json.loads(f.read()))
    #har_page = HarPage(page, har_data=json.loads(f.read()))

for har_page in har_parser.pages:

    ## POST requests
    post_requests = har_page.post_requests

    # filter for adobe calls
    # contains https://woolworthsfoodgroup.sc.omtrdc

    adobe_post_hits = []
    for request in post_requests:
        if "https://woolworthsfoodgroup.sc.omtrdc" in request["request"]["url"]:
            adobe_post_hits.append(request)
            #print(json.dumps(request, indent=4))


    # decode url characters
    for adobe_post_hit in adobe_post_hits:
        #data_sent = urllib.parse.unquote(adobe_post_hit["request"]["postData"]["text"])

        #print(data_sent)
        #print()
        #for i in data_sent.split("&"):
        #for i in re.split('\S+&\S', data_sent):
        #for i in adobe_post_hit["request"]["postData"]["text"].split("&"):
            #print(i)
            #print()
        #query = parse_query_string(data_sent)
        query = parse_query_string(adobe_post_hit["request"]["postData"]["text"])
        #print(json.dumps(query, indent=4))
        #print()
        #print()
        list_to_print.append(query)


    ## GET requests
    get_requests = har_page.get_requests

    for request in get_requests:
        if "https://woolworthsfoodgroup.sc.omtrdc" in request["request"]["url"]:
            #print(request["request"]["url"])

            my_url = request["request"]["url"]
            parsed = urllib.parse.urlparse(my_url)
            #print(parsed.query)

            data_sent = urllib.parse.unquote(str(parsed.query))
            query = parse_query_string(parsed.query)
            #print(json.dumps(query, indent=4))
            #print()
            #print()
            list_to_print.append(query)
            #for i in data_sent.split("&"):
                #print(i)
            #print()
            #print()


new_list = sorted(list_to_print, key=lambda k: k['t'])

for i in new_list:
    print(json.dumps(i, indent=4))
