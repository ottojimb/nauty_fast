import json
from datetime import timezone, datetime

from fastapi.testclient import TestClient

from main import app
from data import crud
from utils import osm

client = TestClient(app)


def test_auth_main(monkeypatch):
    data = {
        "username": "string",
        "full_name": "string",
        "email": "string@string.com",
        "password": "string"
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    def mockuser(_test):
        return data

    monkeypatch.setattr(crud, "create_user", mockuser)

    response = client.post("/user/", json=data, headers=headers)

    obj = json.loads(response.text)

    assert obj["username"] == data["username"]
    assert obj["full_name"] == data["full_name"]
    assert response.status_code == 200


def test_osm_resolver():
    query = """
    <osm-script output="json">
  <query type="node">
    <has-kv k="name" v="Ibagué"/>
  </query>
  <union>
    <query type="node">
      <around radius="1500"/>
      <has-kv k="amenity" regv="restaurant"/>
    </query>
  </union>
  <print mode="body"/>
  <recurse type="down"/>
  <print mode="skeleton"/>
  </osm-script>
    """.encode("utf-8")

    res = osm.query_osm(query)

    assert len(res["elements"]) == 26


def test_get_user_by_name(monkeypatch):
    data = {
        "username": "string",
        "full_name": "string",
        "email": "string@string.com",
        "password": "string"
    }

    def mockuser(_test):
        return data

    monkeypatch.setattr(crud, "get_user_by_username", mockuser)

    assert crud.get_user_by_username("string") == data


def test_get_user_by_email(monkeypatch):
    data = {
        "username": "string",
        "full_name": "string",
        "email": "string@string.com",
        "password": "string"
    }

    def mockuser(_test):
        return data

    monkeypatch.setattr(crud, "get_user_by_email", mockuser)

    assert crud.get_user_by_email("string@string.com") == data


def test_get_query_log(monkeypatch):
    data = [
        {"query_string": "Bogotá", "created_at": datetime.now(timezone.utc)},
        {"query_string": "Medellín", "created_at": datetime.now(timezone.utc)}
    ]

    def mockuser():
        return data

    monkeypatch.setattr(crud, "get_query_log", mockuser)

    assert len(crud.get_query_log()) == 2
