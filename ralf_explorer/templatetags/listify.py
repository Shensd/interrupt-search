from django import template
import json

register = template.Library()

@register.filter('listify')
def listify(obj):
    obj = json.loads(obj)

    converted = []

    for key in obj:
        listing_copy = obj[key]
        listing_copy["name"] = key

        converted.append(listing_copy)

    return converted

@register.filter("jsonloads")
def jsonloads(obj):
    return json.loads(obj)