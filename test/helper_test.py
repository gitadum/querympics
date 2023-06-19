#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import utils.helper
import pytest

@pytest.mark.parametrize(
    ("input_name", "expected"),
    (
        ("Michael Phelps", ("Michael", "PHELPS")),
        ("Zsuzsanna 'Zsu' Jakabos", ("Zsuzsanna", "JAKABOS")),
        ("JAKABOS Zsuzsanna", ("Zsuzsanna", "JAKABOS")),
    )
)
def test_parse_name(input_name, expected):
    assert utils.helper.parse_name(input_name) == expected
