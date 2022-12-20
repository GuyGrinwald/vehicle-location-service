from flask import abort, request
from flask_restful import Resource

from infra.db import SpatialInMemoryLocationDB
from infra.location import Location
from location.location_engine import LocationEngine


class LocationQuery(Resource):
    def __init__(self) -> None:
        self.location_engine = LocationEngine(SpatialInMemoryLocationDB())
        super().__init__()

    def get(self):
        args = request.args

        if "latitude" not in args or "longitude" not in args or "radius" not in args:
            abort(400, "No location information provided")

        latitude, longitude, radius = (
            args.get("latitude", type=float),
            args.get("longitude", type=float),
            args.get("radius", type=float),
        )

        if not self._valid_location_info(latitude, longitude, radius):
            abort(
                400,
                "Location isn't a valid set of latitude, longitude, and radius coordinates",
            )

        return self.location_engine.get_vehicles_in_area(latitude, longitude, radius)

    def _valid_location_info(self, latitude: float, longitude: float, radius: float):
        return (
            latitude is not None
            and longitude is not None
            and radius is not None
            and Location.valid_coordinates(latitude, longitude)
        )
