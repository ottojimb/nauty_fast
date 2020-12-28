import json
import config
import requests


def query_osm(query: str) -> any:
    req_headers = {
        "Content-Type": "application/xml",
        "Accept": "application/json",
    }

    req = requests.post(
        config.OSM_PROVIDER,
        data=query,
        headers=req_headers,
    )

    return json.loads(req.text)
