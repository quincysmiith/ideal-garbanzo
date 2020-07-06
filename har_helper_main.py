import json
from haralyzer import HarParser, HarPage
import os
from datetime import datetime
import click
import urllib.parse
from har_helper import parse_query_string, parse_product_list


### MAIN WORK ###
@click.command()
@click.argument("file_path_to_har_file", type=click.Path())
def extract_adobe_from_har(file_path_to_har_file):
    list_to_print = []

    with open(file_path_to_har_file, "r") as f:
        har_parser = HarParser(json.loads(f.read()))

    for har_page in har_parser.pages:

        ## POST requests
        post_requests = har_page.post_requests

        # filter for adobe hits
        adobe_post_hits = []
        for request in post_requests:
            if "https://woolworthsfoodgroup.sc.omtrdc" in request["request"]["url"]:
                adobe_post_hits.append(request)
                # print(json.dumps(request, indent=4))

        for adobe_post_hit in adobe_post_hits:
            query = parse_query_string(adobe_post_hit["request"]["postData"]["text"])

            list_to_print.append(query)

        ## GET requests
        get_requests = har_page.get_requests

        # filter adobe requests
        for request in get_requests:
            if "https://woolworthsfoodgroup.sc.omtrdc" in request["request"]["url"]:
                # print(request["request"]["url"])

                my_url = request["request"]["url"]
                parsed = urllib.parse.urlparse(my_url)

                data_sent = urllib.parse.unquote(str(parsed.query))
                query = parse_query_string(parsed.query)

                list_to_print.append(query)

    new_list = sorted(list_to_print, key=lambda k: k["t"])

    click.echo(json.dumps(new_list, indent=4))

    return None


if __name__ == "__main__":
    extract_adobe_from_har()
