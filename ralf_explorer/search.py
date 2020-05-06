import re
from django.db.models import Q
from .models import Interrupt

_QUERY_CONVERSIONS = {
    "id": "id__exact",
    "category": "categories__icontains",
    "call_number": "call_number__icontains",
    "number": "number__iexact",
    "tagline": "tagline__icontains",
    "sections": "sections_json__icontains",

    # the rest are short cut names
    "i": "id__exact",
    "c": "categories__icontains",
    "cn": "call_number__icontains",
    "n": "number__iexact",
    "t": "tagline__icontains",
    "s": "sections_json__icontains",
}

def _convert_query(get_params):
    query_request = {}

    # iterate GET params, only process ones that are a recognized name
    # and non-empty
    for param in get_params:
        param = param.lower()

        if param not in _QUERY_CONVERSIONS:
            continue

        if get_params[param] == "":
            continue

        conversion = _QUERY_CONVERSIONS[param]

        query_request[conversion] = get_params[param] 

    return query_request

def _get_search_pairs(search_string):
    # matches 
    # field_name:value 
    # or 
    # field_name:"value va''''lue value"
    # or 
    # field_name:'value value """""value'
    matches = re.findall(r'(\w+):(?:(\w+)|([\'"])(.*?)\3)', search_string)

    parsed_matches = []

    # because I suck at regex and could only find a way to do this with two
    # capture groups, we have to iterate through them and find which one isn't
    # empty and then use that as the value
    for match in matches:
        name = match[0]
        value = match[1] if match[1] != '' else match[3]

        parsed_matches.append((name, value))

    return parsed_matches

def _convert_multisearch_query(get_params):
    pairs = _get_search_pairs(get_params["multisearch"])

    search_dict = {}

    for pair in pairs:
        # not a valid param, ignore
        if pair[0].lower() not in _QUERY_CONVERSIONS:
            continue

        field_name = _QUERY_CONVERSIONS[pair[0].lower()]

        # not already in search, create new entry and go to next
        if field_name not in search_dict:
            search_dict[field_name] = [pair[1]]
            continue

        search_dict[field_name].append(pair[1])
    
    return search_dict

def _multisearch_query(search_dict):
    
    search_fields = []

    for param in search_dict:
        field_values = search_dict[param]

        accumulated_Q = Q(**{
            param:field_values[0]
        })

        # if there is more than one search term for the current field,
        # iterate through them and or them all together then append
        for value in field_values[1:]:
            accumulated_Q = accumulated_Q | Q(**{
                param:value
            })
        
        search_fields.append(accumulated_Q)

    return Interrupt.objects.filter(*search_fields)

def process_query(get_params):
    if "multisearch" in get_params:
        query_request = _convert_multisearch_query(get_params)
        matches = _multisearch_query(query_request)
    else:
        query_request = _convert_query(get_params)
        # process query request
        matches = Interrupt.objects.filter(**query_request)

    return (matches, query_request)