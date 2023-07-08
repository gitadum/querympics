#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi.testclient import TestClient
from app.api import app
import pytest

# EXEMPLES #

# Result
lmanaudou2004_swim = {
                        "id": "S121453",
                        "games": "S2004",
                        "sport": "Swimming",
                        "event": "Swimming Women's 400 metres Freestyle",
                        "athlete": "506160875731",
                        "noc": "FRA",
                        "medal": "G"
                      }

lmanaudou2004_boxing = {
                        "id": "S121453",
                        "games": "S2004",
                        "sport": "Boxing",
                        "event": "Swimming Women's 400 metres Freestyle",
                        "athlete": "506160875731",
                        "noc": "FRA",
                        "medal": "G"
                      }

zjakabos_ice_swimming_input = {
                                "season": "Winter",
                                "year": "2014",
                                "sport": "Ice Swimming",
                                "event": "Ice Swimming Women's 200m Butterfly",
                                "athlete": "410421217148",
                                "noc": "HUN",
                                "medal": "S"
                                }

zjakabos_ice_swimming_output = {
                                "id": "W048565",
                                "games": "W2014",
                                "sport": "Ice Swimming",
                                "event": "Ice Swimming Women's 200m Butterfly",
                                "athlete": "410421217148",
                                "noc": "HUN",
                                "medal": "S"
                                }


def test_greetings():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"greetings": "Welcome to QUERYMPICS!"}

@pytest.mark.parametrize(
    ("input_id", "expected"),
    (
        (lmanaudou2004_swim["id"], lmanaudou2004_swim),
    )
)
def test_get_a_result(input_id, expected):
    with TestClient(app) as client:
        response = client.get(f"/result/{input_id}")
        assert response.status_code == 200
        assert response.json() == expected


@pytest.mark.parametrize(
        ("input_post", "expected"),
        (
            (zjakabos_ice_swimming_input, zjakabos_ice_swimming_output),
        )
)
def test_write_a_result(input_post, expected):
    with TestClient(app) as client:
        response = client.post("/result/new", params=input_post)
        assert response.status_code == 200
        assert response.json() == expected
        # On supprime l'entrée créée pour le test
        client.delete(f"/result/{response.json()['id']}")

@pytest.mark.parametrize(
        ("input_id", "input_update", "expected"),
        (
            (lmanaudou2004_swim["id"],
             {"sport": "Boxing"},
             lmanaudou2004_boxing),
        )
)
def test_update_a_result(input_id, input_update, expected):
    with TestClient(app) as client:
        original_input = client.get(f"/result/{input_id}").json()
        response = client.put(f"/result/{input_id}", params=input_update)
        assert response.status_code == 200
        assert response.json() == expected
        # On rétablit les valeurs modifiées pour le test à leur état d'origine
        client.put(f"/result/{input_id}", params=original_input)
