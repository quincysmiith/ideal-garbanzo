from dateutil import parser
import urllib.parse


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
        # print(i)
        items = i.split("=", 1)
        # print(items)
        try:
            key = items[0]
            value = urllib.parse.unquote(items[1])
            if key == "t":
                value = parser.parse(value[:-7])
            return_dict.update({key: str(value)})
        except:
            pass
            # print("Failed to add to dict:")
            # print(items)
        # print()

    try:
        my_product_dict = parse_product_list(return_dict["products"])
        return_dict.update({"products": my_product_dict})
    except:
        pass

    return return_dict


def parse_product_list(product_string: str) -> dict:
    """Parses a product string and turns it into a dictionary format.

    Args:
        product_string (str): A product string from an adobe call that
        lists all the products listed on a search results page

    Returns:
        dict: [description]
    """

    main_dict = {}
    for num, i in enumerate(product_string.split(",")):

        item_dict = {}

        if len(i.split(";;")) == 3:
            a_list = i.split(";;")
            item_dict.update({"Product": a_list[0]})
            item_dict.update({"Price": a_list[1]})

            # print(a_list[2])

            evar_list = a_list[2].split("|")

            evar_dict = {}
            for evar in evar_list:
                try:
                    items = evar.split("=", 1)
                    evar_dict.update({items[0]: items[1]})
                except:
                    pass
                    # print("Failed to parse")
                    # print(items)

        if len(i.split(";;")) == 1:
            a_list = i.split("|")
            item_dict.update({"Category": a_list[0]})

            evar_list = a_list[1:]

        evar_dict = {}
        for evar in evar_list:
            try:
                items = evar.split("=", 1)
                evar_dict.update({items[0]: items[1]})
            except:
                print("Failed to parse")
                print(items)

        item_dict.update({"eVars": evar_dict})

        main_dict.update({num: item_dict})

    return main_dict
