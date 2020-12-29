import json
import requests


def query_osm(query: str) -> any:
    req_headers = {
        "Content-Type": "application/xml",
        "Accept": "application/json",
    }

    req = requests.post(
        "https://lz4.overpass-api.de/api/interpreter",
        data=query,
        headers=req_headers,
    )

    return json.loads(req.text)
