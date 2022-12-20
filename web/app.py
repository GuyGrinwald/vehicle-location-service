from flask import Flask
from flask_restful import Api

from web.resources.health import Health
from web.resources.location_query import LocationQuery
from web.resources.location_reporting import LocationReporting

app = Flask(__name__)
api = Api(app)

api.add_resource(Health, "/health")
api.add_resource(LocationReporting, "/report/<string:vehicle_id>")
api.add_resource(LocationQuery, "/query")

if __name__ == "__main__":
    # Use this in non-prod envs only
    app.run(debug=False)
