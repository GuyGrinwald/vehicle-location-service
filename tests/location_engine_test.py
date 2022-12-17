import logging
import uuid

import pytest

from infra.db import InMemoryLocationDB
from infra.location import Location
from location.location_engine import LocationEngine

import utils.logging_config  # isort:skip

logger = logging.getLogger(__name__)


class TestlocationEngine:
    @pytest.fixture
    def in_memory_db(self):
        logging.info("Setting up a new InMemoryLocationDB for testing")
        db = InMemoryLocationDB()
        yield db

    def test_report_location(self, in_memory_db):
        assert len(in_memory_db._vehicle_db) == 0

        vehicle_id = uuid.uuid4().hex
        location = Location(1, 1)

        location_engine = LocationEngine(in_memory_db)
        location_engine.report_location(
            vehicle_id, location.latitude, location.longtitude
        )

        assert len(in_memory_db._vehicle_db) == 1
        assert in_memory_db._vehicle_db[vehicle_id].latitude == location.latitude
        assert in_memory_db._vehicle_db[vehicle_id].longtitude == location.longtitude
