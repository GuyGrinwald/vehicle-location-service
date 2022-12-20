class Location:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def __eq__(self, another):
        return (self.latitude, self.longitude) == (another.latitude, another.longitude)

    def __hash__(self):
        return hash((self.latitude, self.longitude))

    @staticmethod
    def valid_coordinates(latitude: float, longitude: float) -> bool:
        return (
            latitude <= 90
            and latitude >= -90
            and longitude <= 180
            and longitude >= -180
        )
