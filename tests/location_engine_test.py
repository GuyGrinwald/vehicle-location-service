import logging
import uuid

import pytest

from infra.db import InMemoryLocationDB, SpatialInMemoryLocationDB
from infra.location import Location
from location.location_engine import LocationEngine

import utils.logging_config  # isort:skip

logger = logging.getLogger(__name__)


class TestlocationEngine:
    @pytest.fixture
    def vehicles(self):
        vehicle_id_1 = "0927b073e5b44f48a8dfe7d6e4bd32d8"
        vehicle_id_2 = "a2f37f1c6c43416ebbc0960e2bdda05e"
        vehicle_id_3 = "a2f37f1c6c43416ea8dfe7d6e4bd32d8"
        yield vehicle_id_1, vehicle_id_2, vehicle_id_3

    @pytest.fixture
    def in_memory_db(self, vehicles):
        logging.info("Setting up a new InMemoryLocationDB for testing")

        vehicle_id_1, vehicle_id_2, vehicle_id_3 = vehicles

        db = InMemoryLocationDB()
        db._vehicle_db = {
            vehicle_id_1: Location(1, 1),
            vehicle_id_2: Location(-2, -2),
            vehicle_id_3: Location(2, 2),
        }

        yield db

    @pytest.fixture
    def spatial_in_memory_db(self, vehicles):
        logging.info("Setting up a new SpatialInMemoryLocationDB for testing")

        vehicle_id_1, vehicle_id_2, vehicle_id_3 = vehicles

        db = SpatialInMemoryLocationDB()
        db._vehicle_db = {
            vehicle_id_1: Location(1, 1),
            vehicle_id_2: Location(-2, -2),
            vehicle_id_3: Location(2, 2),
        }

        db._world_grid[Location(1, 1)] = {vehicle_id_1}
        db._world_grid[Location(-2, -2)] = {vehicle_id_2}
        db._world_grid[Location(2, 2)] = {vehicle_id_3}
        
        yield db

    def test_report_location(self, in_memory_db):
        assert len(in_memory_db._vehicle_db) == 3

        vehicle_id = uuid.uuid4().hex
        location = Location(1, 1)

        location_engine = LocationEngine(in_memory_db)
        location_engine.report_location(
            vehicle_id, location.latitude, location.longtitude
        )

        assert len(in_memory_db._vehicle_db) == 4
        assert in_memory_db._vehicle_db[vehicle_id].latitude == location.latitude
        assert in_memory_db._vehicle_db[vehicle_id].longtitude == location.longtitude

    def test_get_vehicles_in_area(self, in_memory_db, vehicles):
        location_engine = LocationEngine(in_memory_db)
        vehicle_id_1, vehicle_id_2, vehicle_id_3 = vehicles

        vehicles = location_engine.get_vehicles_in_area(0, 0, 158)  # distance in KM
        assert len(vehicles) == 1
        assert vehicles[0] == vehicle_id_1

        vehicles = location_engine.get_vehicles_in_area(1, 1, 316)  # distance in KM
        assert len(vehicles) == 2
        assert vehicle_id_1 in vehicles and vehicle_id_3 in vehicles

        vehicles = location_engine.get_vehicles_in_area(-2.5, -2.5, 158)
        assert len(vehicles) == 1
        assert vehicles[0] == vehicle_id_2

    def test_spatial_report_location(self, spatial_in_memory_db):
        assert len(spatial_in_memory_db._vehicle_db) == 3

        vehicle_id = uuid.uuid4().hex
        location = Location(1, 1)

        location_engine = LocationEngine(spatial_in_memory_db)
        location_engine.report_location(
            vehicle_id, location.latitude, location.longtitude
        )

        assert len(spatial_in_memory_db._vehicle_db) == 4
        assert (
            spatial_in_memory_db._vehicle_db[vehicle_id].latitude == location.latitude
        )
        assert (
            spatial_in_memory_db._vehicle_db[vehicle_id].longtitude
            == location.longtitude
        )

    def test_spatial_get_vehicles_in_area(self, spatial_in_memory_db, vehicles):
        location_engine = LocationEngine(spatial_in_memory_db)
        vehicle_id_1, vehicle_id_2, vehicle_id_3 = vehicles

        vehicles = location_engine.get_vehicles_in_area(0, 0, 158)  # distance in KM
        assert len(vehicles) == 1
        assert vehicles[0] == vehicle_id_1

        vehicles = location_engine.get_vehicles_in_area(1, 1, 316)  # distance in KM
        assert len(vehicles) == 2
        assert vehicle_id_1 in vehicles and vehicle_id_3 in vehicles

        vehicles = location_engine.get_vehicles_in_area(-2.5, -2.5, 158)
        assert len(vehicles) == 1
        assert vehicles[0] == vehicle_id_2
