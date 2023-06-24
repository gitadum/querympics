#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import re
import string
from nameparser import HumanName

def parse_name(full_name: str):
    
    parsed_name = {
        "first": "",
        "last": ""
    }

    # Nettoyage des caractères avant le parsing
    stopchars = """!\"#$%&()*+,./:;<=>?@[\\]^_`{|}~"""
    spacechars = """-"""
    full_name = full_name.translate(str.maketrans('', '', stopchars))
    full_name = full_name.translate(str.maketrans(spacechars, " "))
    full_name = full_name.strip()

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
    
    parsed_name["first"] = ' '.join([s.capitalize()
                                     for s in parsed_name["first"].split()])
    parsed_name["last"] = ' '.join([s.capitalize()
                                    for s in parsed_name["last"].split()])

    return parsed_name

def give_short_name(full_name: str) -> str:
    first_name = parse_name(full_name)["first"]
    last_name = parse_name(full_name)["last"]
    short_name = " ".join([first_name.capitalize(),
                           last_name.upper()])
    return short_name

def closest_even(n):
    rn = 0
    try:
        rn = round(n)
    except TypeError:
        return rn
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
    # On supprime les espaces de la chaîne de caractères person_id
    person_id = person_id.replace(" ", "")
    person_id = person_id.upper()
    return person_id

def give_games_id(year: int, season: str):
    season_letter = "S" if season == "Summer" else "W"
    games_id = "".join([season_letter, str(year)])
    return games_id

def get_numeric_id(notanum: str, nc: int = 12):
    id = int(hashlib.sha1(notanum.encode("utf-8")).hexdigest(), 16) % (10 ** nc)
    id = str(id).zfill(12)
    return id
