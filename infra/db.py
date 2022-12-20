import math
from abc import ABC
from collections import defaultdict
from functools import cache
from typing import List

from haversine import haversine

from infra.location import Location


class LocationDB(ABC):
    def __init__(self) -> None:
        super().__init__()

    def store(self, id: str, latitude: float, longitude: float):
        """
        Stores a vehicle and location (latitude, longitude) into the DB. I'ts up for the caller to validate the values
        """
        pass

    def get_in_area(
        self, latitude: float, longitude: float, radius: float
    ) -> List[str]:
        """
        Returns a list of ids of vehivles that are in the radius (KM) of the given location (latitude, longitude)
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
                (center.latitude, center.longitude), (point.latitude, point.longitude)
            )
            <= radius
        )


@cache  # marks this as a Singleton
class InMemoryLocationDB(LocationDB):
    """
    An in-memory implementation of the LocationDB abstract class that stores the locations in a dictionary and naively iterates
    them to return data
    """

    def __init__(self) -> None:
        self._vehicle_db = {}

        super().__init__()

    def store(self, id: str, latitude: float, longitude: float):
        self._vehicle_db[id] = Location(latitude, longitude)

    def get_in_area(
        self, latitude: float, longitude: float, radius: float
    ) -> List[str]:
        center = Location(latitude=latitude, longitude=longitude)
        return [
            vehicle
            for vehicle, vehicle_location in self._vehicle_db.items()
            if self._points_in_radius(vehicle_location, center, radius)
        ]


@cache  # marks this as a Singleton
class SpatialInMemoryLocationDB(LocationDB):
    """
    An in-memory implementation of the LocationDB abstract class that stores the locations spatial data structure
    """

    def __init__(self) -> None:
        self._world_grid = defaultdict(lambda: set())
        self._vehicle_db = {}

        super().__init__()

    def store(self, id: str, latitude: float, longitude: float):
        previous_loc = self._vehicle_db.get(id, None)

        # Remove vehicle from previous location on the world grid
        if previous_loc:
            normlized_location = self._normalize_location(previous_loc)
            self._world_grid[normlized_location].remove(id)

        # Store the new location into the DB and world grid
        new_location = Location(latitude, longitude)
        self._vehicle_db[id] = new_location
        normlized_location = self._normalize_location(new_location)
        self._world_grid[normlized_location].add(id)

    def get_in_area(
        self, latitude: float, longitude: float, radius: float
    ) -> List[str]:
        center = Location(latitude, longitude)

        # Find all locations on world grid that are within the radius from the center
        relevant_locations = [
            location
            for location in self._world_grid.keys()
            if self._points_in_radius(location, center, radius)
        ]

        # Finds all vehicles in relevant locations that are within the radius from the center
        # Note: this is based on 2D Euclidean formula. This is an approximation as in reality we should
        # address Earth's curvitude
        vehicles = [self._world_grid[location] for location in relevant_locations]
        return [
            vehicle
            for sublist in vehicles
            for vehicle in sublist
            if self._intersection(self._vehicle_db[vehicle], center, radius)
        ]

    def _normalize_location(self, location: Location) -> Location:
        return Location(int(location.latitude), int(location.longitude))

    def _intersection(self, cell: Location, center: Location, radius: int) -> bool:
        """
        Returns True if any point overlaps the given Circle and Rectangle - https://www.geeksforgeeks.org/check-if-any-point-overlaps-the-given-circle-and-rectangle/
        """

        # Find the nearest point on the
        # rectangle to the center of
        # the circle
        Xn = max(cell.latitude, min(center.latitude, cell.latitude + 1))
        Yn = max(cell.longitude, min(center.longitude, cell.longitude + 1))

        # Find the distance between the
        # nearest point and the center
        # of the circle
        # Distance between 2 points,
        # (x1, y1) & (x2, y2) in
        # 2D Euclidean space is
        # ((x1-x2)**2 + (y1-y2)**2)**0.5
        Dx = Xn - center.latitude
        Dy = Yn - center.longitude
        return (Dx**2 + Dy**2) <= radius**2
