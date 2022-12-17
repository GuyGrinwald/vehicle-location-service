import logging
from typing import List

from infra.db import LocationDB

import utils.logging_config  # isort:skip

logger = logging.getLogger(__name__)


class LocationEngine:
    def __init__(self, db: LocationDB) -> None:
        self.db = db

    def report_location(self, id: str, latitude: float, longtitude: float):
        """
        Stores the given vehicle and location information in the DB
        """
        if not self._valid_coordinates(latitude, longtitude):
            raise ValueError(f"Invalide coordinates: {[latitude, longtitude]}")

        self.db.store(id=id, latitude=latitude, longtitude=longtitude)

    def get_vehicles_in_area(
        self, latitude: float, longtitude: float, radius: float
    ) -> List[str]:
        """
        Returns a list of vehicles in the given radius (KM) from the given center (lat/long)
        """
        if not self._valid_coordinates(latitude, longtitude):
            raise ValueError(f"Invalide coordinates: {[latitude, longtitude]}")

        return self.db.get_in_area(
            latitude=latitude, longtitude=longtitude, radius=radius
        )

    def _valid_coordinates(self, latitude: float, longtitude: float) -> bool:
        return (
            latitude <= 90
            and latitude >= -90
            and longtitude <= 180
            and longtitude >= -180
        )
