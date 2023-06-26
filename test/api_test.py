#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)

def test_greetings():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"greetings": "Welcome to QUERYMPICS!"}
