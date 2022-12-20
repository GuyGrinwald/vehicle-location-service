import logging
from typing import List

from infra.db import LocationDB
from infra.location import Location

import utils.logging_config  # isort:skip

logger = logging.getLogger(__name__)


class LocationEngine:
    def __init__(self, db: LocationDB) -> None:
        self.db = db

    def report_location(self, id: str, latitude: float, longitude: float):
        """
        Stores the given vehicle and location information in the DB
        """
        if not Location.valid_coordinates(latitude, longitude):
            raise ValueError(f"Invalide coordinates: {[latitude, longitude]}")

        self.db.store(id=id, latitude=latitude, longitude=longitude)

    def get_vehicles_in_area(
        self, latitude: float, longitude: float, radius: float
    ) -> List[str]:
        """
        Returns a list of vehicles in the given radius (KM) from the given center (lat/long)
        """
        if not Location.valid_coordinates(latitude, longitude):
            raise ValueError(f"Invalide coordinates: {[latitude, longitude]}")

        return self.db.get_in_area(
            latitude=latitude, longitude=longitude, radius=radius
        )
