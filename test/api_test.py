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
