#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi.testclient import TestClient
from app.api import app
import pytest

# EXEMPLES #

# Result
lmanaudou2004_400m = {
    "id": "S121453",
    "games": "S2004",
    "sport": "Swimming",
    "event": "Swimming Women's 400 metres Freestyle",
    "athlete": "506160875731",
    "noc": "FRA",
    "medal": "G"
                      }

lmanaudou2012_400m_input = {
    "season": "Summer",
    "year": "2012",
    "sport": "Swimming",
    "event": "Swimming Women's 400 metres Freestyle",
    "athlete": "506160875731",
    "noc": "FRA",
    "medal": "G"
                            }

lmanaudou2012_400m_output = {
    "id": "S237674",
    "games": "S2012",
    "sport": "Swimming",
    "event": "Swimming Women's 400 metres Freestyle",
    "athlete": "506160875731",
    "noc": "FRA",
    "medal": "G"
                             }

lmanaudou2012_boxing = {
    "id": "S237674",
    "games": "S2012",
    "sport": "Boxing",
    "event": "Swimming Women's 400 metres Freestyle",
    "athlete": "506160875731",
    "noc": "FRA",
    "medal": "G"
                        }

tparker = {
    "id": "715210719562",
    "first_name": "William",
    "last_name": "PARKER",
    "gender": "M",
    "birth_year": 1982,
    "lattest_noc": "FRA"
}

vwembanyama_input = {
    "first_name": "Victor",
    "last_name": "Wembanyama",
    "gender": "M",
    "birth_year": 2004,
    "lattest_noc": "FRA",
}

vwembanyama_output = {
    "id": "076466741491",
    "first_name": "Victor",
    "last_name": "WEMBANYAMA",
    "gender": "M",
    "birth_year": 2004,
    "lattest_noc": "FRA"
}

def test_greetings():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"greetings": "Welcome to QUERYMPICS!"}

@pytest.mark.parametrize(
    ("input_id", "expected"),
    (
        (lmanaudou2004_400m["id"], lmanaudou2004_400m),
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
            (lmanaudou2012_400m_input, lmanaudou2012_400m_output),
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
        ("test_input", "update_params", "expected"),
        (
            (lmanaudou2012_400m_input,
             {"sport": "Boxing"},
             lmanaudou2012_boxing),
        )
)
def test_update_a_result(test_input, update_params, expected):
    with TestClient(app) as client:
        create_test_item = client.post("/result/new/", params=test_input)
        assert create_test_item.status_code == 200
        test_item = create_test_item.json()
        response = client.put(f"/result/{test_item['id']}",
                              params=update_params)
        assert response.status_code == 200
        assert response.json() == expected
        # On supprime l'entrée créée pour le test
        client.delete(f"/result/{test_item['id']}")


def test_delete_a_result():
    test_item_input = lmanaudou2012_400m_input
    with TestClient(app) as client:
        create_test_item = client.post("/result/new", params=test_item_input)
        assert create_test_item.status_code == 200
        test_item = create_test_item.json()
        response = client.delete(f"/result/{test_item['id']}")
        assert response.status_code == 200
        assert response.json() == {"message": f"Deleted {test_item['id']}."}
        assert client.get(f"/result/{test_item['id']}").status_code == 404

@pytest.mark.parametrize(
        ("input_id", "expected"),
        (
            (tparker["id"], tparker),
        )
)
def test_get_an_athlete(input_id, expected):
    with TestClient(app) as client:
        response = client.get(f"/athlete/{input_id}")
        assert response.status_code == 200
        assert response.json() == expected

@pytest.mark.parametrize(
        ("input_post", "expected"),
        (
            (vwembanyama_input, vwembanyama_output),
        )
)
def test_write_an_athlete(input_post, expected):
    with TestClient(app) as client:
        response = client.post("/athlete/new", params=input_post)
        assert response.status_code == 200
        assert response.json() == expected
        # On supprime l'entrée créée pour le test
        client.delete(f"/athlete/{response.json()['id']}")
