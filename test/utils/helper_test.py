#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import utils.helper
import pytest

@pytest.mark.parametrize(
    ("input_name", "expected"),
    (
        ("Michael Phelps", {"first": "Michael", "last": "Phelps"}),
        ("Zsuzsanna 'Zsu' Jakabos", {"first": "Zsuzsanna", "last": "Jakabos"}),
        ("JAKABOS Zsuzsanna", {"first": "Zsuzsanna", "last": "Jakabos"}),
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

@pytest.mark.parametrize(
        ("input_first_name", "input_last_name", "input_gender", "input_yob",
         "expected"),
    (
        ("Alex", "MORGAN", "F", 1989, "ALEXMORGAN01989"),
        ("Adrien", "DUMONT", "M", 1996, "ADRIENDUMONT11996")
    )
)
def test_give_person_id(input_first_name, input_last_name, input_gender,
                        input_yob, expected):
    assert utils.helper.give_person_id(input_first_name,
                                       input_last_name,
                                       input_gender,
                                       input_yob) == expected

@pytest.mark.parametrize(
        ("input_id", "expected"),
    (
        ("ZSUZSANNAJAKABOS01988", "410421217148"),
        ("ADRIENDUMONT11996", "139106765041")
    )
)
def test_get_numeric_id(input_id, expected):
    assert utils.helper.get_numeric_id(input_id) == expected

@pytest.mark.parametrize(
        ("input_n", "expected"),
    (
        (1955, 1954),
        (1963, 1962),
        (1943, 1942),
        (1942, 1942),
    )
)
def test_closest_even(input_n, expected):
    assert utils.helper.closest_even(input_n) == expected
