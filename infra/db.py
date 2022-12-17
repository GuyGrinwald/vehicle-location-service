import math
from abc import ABC
from typing import List

from infra.location import Location


class LocationDB(ABC):
    def __init__(self) -> None:
        super().__init__()

    def store(self, id: str, latitude: float, longtitude: float):
        """
        Stores a vehicle and location (latitude, longtitude) into the DB. I'ts up for the caller to validate the values
        """
        pass

    def get_in_area(
        self, latitude: float, longtitude: float, radius: float
    ) -> List[str]:
        """
        Returns a list of ids of vehivles that are in the radius of the given location (latitude, longtitude)
        """
        pass

    def _vehicle_in_radius(
        self, vehicle_location: Location, center: Location, radius: float
    ) -> bool:
        return math.pow((vehicle_location.latitude - center.latitude), 2) + math.pow(
            (vehicle_location.longtitude - center.longtitude), 2
        ) < math.pow(radius, 2)


class InMemoryLocationDB(LocationDB):
    """
    An in-memory implementation of the LocationDB abstract class that stores the locations in a dictionary and naively iterates
    them to return data
    """

    def __init__(self) -> None:
        self._vehicle_db = {}

        super().__init__()

    def store(self, id: str, latitude: float, longtitude: float):
        self._vehicle_db[id] = Location(latitude, longtitude)

    def get_in_area(
        self, latitude: float, longtitude: float, radius: float
    ) -> List[str]:
        center = Location(latitude=latitude, longtitude=longtitude)
        return [
            vehicle
            for vehicle, vehicle_location in self._vehicle_db.items()
            if self._vehicle_in_radius(vehicle_location, center, radius)
        ]
