from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import Interrupt

import json

from .search import process_query

# unsure of what to make the title of the page so this was just done
# to make it a bit easier to change later if I so desire
DEFAULT_CONTENT = {
    "title": "SEARCHABLE INTERRUPT LIST"
}

def index(request):
    return render(request, "ralf_explorer/index.html", DEFAULT_CONTENT)

def view_info(request):
    return render(request, "ralf_explorer/info.html", DEFAULT_CONTENT)

def view_filtered_json(request):
    get_params = request.GET

    def convert_registers(register_str):
        registers = json.loads(register_str)

        reg_list = []

        for reg in registers:
            registers[reg]["name"] = reg
            reg_list.append(registers[reg])

        return reg_list

    def convert_query_object(obj):
        return {
            "id": obj.id,
            "vector" : obj.number,
            "number" : obj.call_number,
            "categories" : obj.categories,
            "tagline" : obj.tagline,
            "registers_json" : convert_registers(obj.registers_json),
            "sections_json" : json.loads(obj.sections_json),
        }

    matches, _ = process_query(get_params)

    converted_query_objects = []
    for match in matches:
        converted_query_objects.append(
            convert_query_object(match)
        )

    return JsonResponse({
        "objects" : converted_query_objects
    })


def view_filtered_interrupts(request):
    get_params = request.GET

    matches, query_request = process_query(get_params)
    
    # used on the template for showing full information of interrupts, such
    # as register lists and subsections
    full_context = False

    if "full_context" in get_params:
        if get_params["full_context"] == "1":
            full_context = True

    return render(request, "ralf_explorer/get.html", {
        "interrupt_list" : matches,
        "full_context": full_context,
        "search": query_request,
        "multisearch": get_params["multisearch"] if "multisearch" in get_params else "",
        **DEFAULT_CONTENT
    })