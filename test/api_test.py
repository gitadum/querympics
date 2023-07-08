#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi.testclient import TestClient
from app.api import app
import pytest

def test_greetings():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"greetings": "Welcome to QUERYMPICS!"}

@pytest.mark.parametrize(
    ("input_id", "expected"),
    (
        ("S121453", {
                        "id": "S121453",
                        "games": "S2004",
                        "sport": "Swimming",
                        "event": "Swimming Women's 400 metres Freestyle",
                        "athlete": "506160875731",
                        "noc": "FRA",
                        "medal": "G"
                    }),
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
            ({
                "season": "Winter",
                "year": "2014",
                "sport": "Ice Swimming",
                "event": "Ice Swimming Women's 200m Butterfly",
                "athlete": "410421217148",
                "noc": "HUN",
                "medal": "S"
              },
             {
                "id": "W048565",
                "games": "W2014",
                "sport": "Ice Swimming",
                "event": "Ice Swimming Women's 200m Butterfly",
                "athlete": "410421217148",
                "noc": "HUN",
                "medal": "S"
              }),
        )
)
def test_write_a_result(input_post, expected):
    with TestClient(app) as client:
        response = client.post("/result/new", params=input_post)
        assert response.status_code == 200
        assert response.json() == expected
        client.delete(f"/result/{response.json()['id']}")
