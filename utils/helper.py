#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import re

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
        if not re.match("\(\-\w+\)", full_name.split(" ")[-1]):
            first_name = " ".join(full_name.split(" ")[:-1])
            last_name = full_name.split(" ")[-1]
        else:
            first_name = " ".join(full_name.split(" ")[:-2])
            last_name = " ".join(full_name.split(" ")[-2:])
            
    last_name = last_name.upper()
    return first_name, last_name
