import logging
from typing import List

from infra.db import LocationDB

import utils.logging_config  # isort:skip

logger = logging.getLogger(__name__)


class LocationEngine:
    def __init__(self, db: LocationDB) -> None:
        self.db = db

    def report_location(self, id: str, latitude: float, longtitude: float):
        self.db.store(id=id, latitude=latitude, longtitude=longtitude)

    def get_vehicles_in_area(
        self, latitude: float, longtitude: float, radius: float
    ) -> List[str]:
        return self.db.get_in_area(
            latitude=latitude, longtitude=longtitude, radius=radius
        )
