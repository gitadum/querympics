#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import utils.helper
import pytest

@pytest.mark.parametrize(
    ("input_name", "expected"),
    (
        ("Michael Phelps", {"first": "michael", "last": "phelps"}),
        ("Zsuzsanna 'Zsu' Jakabos", {"first": "zsuzsanna", "last": "jakabos"}),
        ("JAKABOS Zsuzsanna", {"first": "zsuzsanna", "last": "jakabos"}),
    )
)
def test_parse_name(input_name, expected):
    assert utils.helper.parse_name(input_name) == expected

@pytest.mark.parametrize(
    ("input_name", "expected"),
    (
        ("Michael Phelps", "Michael PHELPS"),
    )
)
def test_give_short_name(input_name, expected):
    assert utils.helper.give_short_name(input_name) == expected
