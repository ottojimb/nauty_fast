from utils import osm
from data import crud
from datetime import datetime
from datetime import timezone

def build_osm_query(amenity: str, radius: int, location: str) -> bytes:  # noqa: D103
    return f"""<osm-script output="json">
  <query type="node">
    <has-kv k="name" v="{location}"/>
  </query>
  <union>
    <query type="node">
      <around radius="{radius}"/>
      <has-kv k="amenity" regv="{amenity}"/>
    </query>
  </union>
  <print mode="body"/>
  <recurse type="down"/>
  <print mode="skeleton"/>
  </osm-script>""".encode("utf-8")


def get_nearby_restaurants(
        location: str,
):
    """Get the nearby restaurants information."""
    query_log = {
        "query_string": location,
        "created_at": datetime.now(timezone.utc)
    }
    crud.create_query_log(query_log)

    query = build_osm_query("restaurant", 1500, location)
    return osm.query_osm(query)


def get_query_log():
    """Get the query log."""
    return crud.get_query_log()
