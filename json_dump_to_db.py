from ralf_explorer.models import Interrupt
import json

# This is the method used to convert the raw json into a useable database for django,
# simply open the django shell, import this file, and run add_entries

def add_entries():
    with open("ralf_explorer/data/dump.json") as dump_file:
        lines = dump_file.readlines()

    interrupts = json.loads("".join(lines))
    for inter in interrupts["objects"]:
        call_number = ""
        if "AX" in inter["interrupt"]["registers"]:
                call_number = "AX {}".format(inter["interrupt"]["registers"]["AX"]["value"])
        elif "AH" in inter["interrupt"]["registers"]:
                call_number = "AH {}".format(inter["interrupt"]["registers"]["AH"]["value"])
        else:
                call_number = "N/A"
        new_inter = Interrupt(number=inter["interrupt"]["number"],
        call_number=call_number,
        categories=inter["categories"],
        tagline=inter["interrupt"]["tagline"],
        registers_json=json.dumps(inter["interrupt"]["registers"]),
        sections_json=json.dumps({
            "subsection_names": inter["subsection_names"],
            "subsections": inter["subsections"]
        }))

        new_inter.save()

