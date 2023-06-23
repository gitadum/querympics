#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import string
import re
from nameparser import HumanName

def parse_name(full_name: str):
    
    parsed_name = {
        "first": "",
        "last": ""
    }

    first_names = []
    last_names = []

    uppercase_search = [s for s in re.split("([A-Z]+) ", full_name) if s]
    for name in uppercase_search:
        if name.isupper():
            last_names.append(name)
        else:
            first_names.append(name)
    parsed_name["first"] = " ".join(first_names)
    parsed_name["last"] = " ".join(last_names)

    if parsed_name["last"] == "":
        name = HumanName(full_name)
        if name.first != "":
            parsed_name["first"] = name.first
        else:
            parsed_name["first"] = name.title
        parsed_name["last"] = name.last
    
    for k in parsed_name.keys():
        parsed_name[k] = parsed_name[k].lower()

    return parsed_name

def give_short_name(full_name: str) -> str:
    first_name = parse_name(full_name)["first"]
    last_name = parse_name(full_name)["last"]
    short_name = " ".join([first_name.capitalize(),
                           last_name.upper()])
    return short_name

def closest_even(n):
    rn = round(n)
    if not rn % 2:
        return rn
    elif abs(rn +1 - n) < abs(rn -1 - n):
        return rn + 1
    else:
        return rn - 1

def give_person_id(first_name: str, last_name: str,
                   gender: str, yob: int) -> str:
    first_name = first_name.translate(str.maketrans('', '', string.punctuation))
    last_name = last_name.translate(str.maketrans('', '', string.punctuation))
    gender_code = 0 if gender == "F" else 1
    person_id = "".join([first_name, last_name,
                         str(gender_code), str(yob)])
    person_id = person_id.upper()
    return person_id
