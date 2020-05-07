import sys
import re
import json

# very programmer
CATEGORIES = {
    "A" : "applications",
    "a" : "access software (screen readers, etc)",
    "B" : "BIOS",
    "b" : "vendor-specific BIOS extensions",
    "C" : "CPU-generated",
    "c" : "caches/spoolers",
    "D" : "DOS kernel",
    "d" : "disk I/O enhancements",
    "E" : "DOS extenders",
    "e" : "electronic mail",
    "F" : "FAX",
    "f" : "file manipulation",
    "G" : "debuggers/debugging tools",
    "g" : "games",
    "H" : "hardware",
    "h" : "vendor-specific hardware",
    "I" : "IBM workstation/terminal emulators",
    "i" : "system info/monitoring",
    "J" : "Japanese",
    "j" : "joke programs",
    "K" : "keyboard enhancers",
    "k" : "file/disk compression",
    "l" : "shells/command interpreters",
    "M" : "mouse/pointing device",
    "m" : "memory management",
    "N" : "network",
    "n" : "non-traditional input devices",
    "O" : "other operating systems",
    "P" : "printer enhancements",
    "p" : "power management",
    "Q" : "DESQview/TopView and Quarterdeck programs",
    "R" : "remote control/file access",
    "r" : "runtime support",
    "S" : "serial I/O",
    "s" : "sound/speech",
    "T" : "DOS-based task switchers/multitaskers",
    "t" : "TSR libraries",
    "U" : "resident utilities",
    "u" : "emulators",
    "V" : "video",
    "v" : "virus/antivirus",
    "W" : "MS Windows",
    "X" : "expansion bus BIOSes",
    "x" : "non-volatile config storage",
    "y" : "security",
    "*" : "reserved (and not otherwise classified)"
}

def is_interrupt_block(block):
    if len(block) < 2:
        return False

    return block[1].startswith("INT ")

def divi_camel_case(string):
    return " ".join(
        list(
            re.findall("((?:^[a-z]|[A-Z])[a-z]*)", string, re.MULTILINE)
        )
    )

def parse_subsections(block):
    subsections = []
    subsection_names = []

    current_subsection = None
    current_subsection_content = []

    for line in block:
        section_name = re.match("^([A-Za-z ]*)\:[ \t](.*)", line, re.MULTILINE)

        if not section_name:
            current_subsection_content.append(line)
            continue
        
        if not current_subsection:
            current_subsection = section_name.groups()[0]
            current_subsection_content = [section_name.groups()[1]]
            continue
        
        subsections.append({
            "name" : divi_camel_case(current_subsection),
            "content": current_subsection_content
        })
        subsection_names.append(current_subsection)

        current_subsection = section_name.groups()[0]
        current_subsection_content = [section_name.groups()[1]]
    
    if current_subsection:
        subsections.append({
            "name" : divi_camel_case(current_subsection),
            "content": current_subsection_content
        })
        subsection_names.append(current_subsection)

    return (subsection_names, subsections)

def parse_registers(register_list):

    register_info = {}

    current_reg = None
    current_reg_content = []

    ax = "???"
    ah = "???"

    def parse_reg_data(reg_match, content):
        reg_name = current_reg.groups()[0]
        reg_data_type = "value" if current_reg.groups()[1] == "=" else "pointer"
        reg_value = current_reg.groups()[2]

        return (reg_name, {
            "data_type": reg_data_type,
            "set_symbol": current_reg.groups()[1],
            "value": reg_value,
            "notes": content
        })

    for reg in register_list:
        reg = reg.strip()
        reg_match = re.match("([A-Za-z]{2,}(?:(?::|,)[A-Za-z]{2,})?)\s(=|->)\s(.*)", reg)

        if not reg_match:
            current_reg_content.append(reg)
            continue

        if not current_reg:
            current_reg = reg_match
            continue

        reg_name, procd_register = parse_reg_data(current_reg, current_reg_content)
        register_info[reg_name] = procd_register

        current_reg = reg_match
        current_reg_content = []

    if current_reg:
        reg_name, procd_register = parse_reg_data(current_reg, current_reg_content)
        register_info[reg_name] = procd_register

    return register_info

def parse_interrupt(block):
    interrupt_info = []

    for line in block[1:]:
        if re.match("([A-Za-z ]*)\:(.*)", line):
            break
            
        interrupt_info.append(line)

    registers = parse_registers(interrupt_info)

    return {
        "number": interrupt_info[0].split("-")[0].split(" ")[1],
        "tagline" : "-".join(interrupt_info[0].split("-")[1:]).strip(),
        "registers": registers
    }


def parse_interrupt_block(block):
    if not is_interrupt_block(block):
        return False

    section_tag_tokens = block[0].strip("-")
    subsection_names, subsections = parse_subsections(block)

    if section_tag_tokens[0] in CATEGORIES:
        category = CATEGORIES[section_tag_tokens[0]]
    else:
        category = "uncategorized"

    return {
        "number": section_tag_tokens[1] if len(section_tag_tokens) > 1 else section_tag_tokens[0],
        "categories": category,
        "subsection_names": subsection_names,
        "subsections" : subsections,
        "interrupt": parse_interrupt(block)
    }

def parse_blocks(lines):
    BLOCK_DELIM = "--------"

    blocks = []

    temp_block = []

    for line in lines:
        if line.startswith(BLOCK_DELIM):
            blocks.append(temp_block)
            temp_block = []
        
        temp_block.append(
            line.strip()
        )

    return blocks

def main(argc, argv):
    if argc < 2:
        print("usage: %s [interrupt files]" % argv[0])
        return

    interrupt_files = argv[1:]

    parsed_blocks = []

    current_id = 0

    for int_file in interrupt_files:
        with open(int_file, 'r', errors="ignore") as int_file:
            lines = int_file.readlines()

        blocks = parse_blocks(lines)

        for block in blocks:
            if is_interrupt_block(block):
                p_block = parse_interrupt_block(block)

                p_block["id"] = current_id

                parsed_blocks.append(p_block)

                current_id += 1

    with open("dump.json", 'w') as json_output:
        json_output.writelines(json.dumps({"objects":parsed_blocks}))

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)