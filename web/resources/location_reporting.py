from typing import Dict

from flask import abort, request
from flask_restful import Resource

from infra.db import SpatialInMemoryLocationDB
from infra.location import Location
from location.location_engine import LocationEngine


class LocationReporting(Resource):
    def __init__(self) -> None:
        self.location_engine = LocationEngine(SpatialInMemoryLocationDB())
        super().__init__()

    def post(self, vehicle_id):
        if "location" not in request.json:
            abort(400, "No location information provided")

        location_info = request.json["location"]

        if not self._valid_location_info(location_info):
            abort(
                400, "Location isn't a valid pair of latitude and longitude coordinates"
            )

        self.location_engine.report_location(
            vehicle_id, location_info["latitude"], location_info["longitude"]
        )

    def _valid_location_info(self, location_info: Dict):
        return (
            "latitude" in location_info
            and "longitude" in location_info
            and isinstance(location_info["latitude"], (int, float))
            and isinstance(location_info["longitude"], (int, float))
            and Location.valid_coordinates(
                location_info["latitude"], location_info["longitude"]
            )
        )
