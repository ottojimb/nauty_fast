"""Endpoint definition for authentication."""
from typing import Optional, List

from fastapi import APIRouter, Security

from api import deps
from data import schemas
from services.auth_service import get_current_active_user
from services.restaurant_service import get_query_log, get_nearby_restaurants

db = deps.SessionLocal()

router = APIRouter()


@router.get("/nearby/", response_model=Optional[schemas.Osm])
def get_nearby(location: str,
                        _current_user: schemas.User = Security(get_current_active_user,
                                                               scopes=["user"])):
    """Read the information nearby restaurants from OSM."""
    data = get_nearby_restaurants(location)

    return data


@router.get("/query_log/", response_model=List[schemas.QueryLog])
def get_nearby(_current_user: schemas.User = Security(get_current_active_user,
                                                               scopes=["user"])):
    """Read the information nearby restaurants from OSM."""
    return get_query_log()
