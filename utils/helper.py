#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from nameparser import HumanName

def parse_name(full_name: str):
    first_name = ""
    last_name = ""
    first_names = []
    last_names = []

    uppercase_search = [s for s in re.split("([A-Z]+) ", full_name) if s]
    for name in uppercase_search:
        if name.isupper():
            last_names.append(name)
        else:
            first_names.append(name)
    first_name = " ".join(first_names)
    last_name = " ".join(last_names)

    if last_name == "":
        name = HumanName(full_name)
        if name.first != "":
            first_name = name.first
        else:
            first_name = name.title
        last_name = name.last
    
    return first_name.capitalize(), last_name.upper()

def give_short_name(full_name: str) -> str:
    first_name, last_name = parse_name(full_name)
    short_name = " ".join([first_name, last_name])
    return short_name
