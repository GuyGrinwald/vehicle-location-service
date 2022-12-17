import math
from abc import ABC
from collections import defaultdict
from typing import List

from haversine import haversine

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
        Returns a list of ids of vehivles that are in the radius (KM) of the given location (latitude, longtitude)
        """
        pass

    def _points_in_radius(
        self, point: Location, center: Location, radius: float
    ) -> bool:
        """
        Returns True if the given point is within the radius (KM) from the center
        """
        return (
            haversine(
                (center.latitude, center.longtitude), (point.latitude, point.longtitude)
            )
            <= radius
        )


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
            if self._points_in_radius(vehicle_location, center, radius)
        ]


class SpatialInMemoryLocationDB(LocationDB):
    """
    An in-memory implementation of the LocationDB abstract class that stores the locations spatial data structure
    """

    def __init__(self) -> None:
        self._world_grid = defaultdict(lambda: set())
        self._vehicle_db = {}

        super().__init__()

    def store(self, id: str, latitude: float, longtitude: float):
        previous_loc = self._vehicle_db.get(id, None)

        # Remove vehicle from previous location on the world grid
        if previous_loc:
            normlized_location = self._normalize_location(previous_loc)
            self._world_grid[normlized_location].remove(id)

        # Store the new location into the DB and world grid
        new_location = Location(latitude, longtitude)
        self._vehicle_db[id] = new_location
        normlized_location = self._normalize_location(new_location)
        self._world_grid[normlized_location].add(id)

    def get_in_area(
        self, latitude: float, longtitude: float, radius: float
    ) -> List[str]:
        normlized_center = self._normalize_location(Location(latitude, longtitude))

        relevant_locations = [
            location
            for location in self._world_grid.keys()
            if self._points_in_radius(location, normlized_center, radius)
        ]

        vehicles = [self._world_grid[location] for location in relevant_locations]

        return [vehicle for sublist in vehicles for vehicle in sublist]

    def _normalize_location(self, location: Location) -> Location:
        return Location(int(location.latitude), int(location.longtitude))
