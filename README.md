Vehicle Location Service
========================

A vehicle location service. Vehicles can update the server on their location, and a user
can query the server for a list of vehicles in a specified area. The assumption is while a vehicle is in motion it
updates it's location every few seconds.

## Setup

1. If not already present, install Python 3.11 and [virtualenvwrapper](https://pypi.org/project/virtualenvwrapper/)
2. Create a local virtualenv
```
$ mkvirtualenv {your-env-name}
```
3. Install project dependencies using
```bash
$ pip install -r requirements.txt
```

## Running Tests

We use [nox](https://nox.thea.codes/en/stable/tutorial.html#running-nox-for-the-first-time) as our testing framework. To run the tests do the following:
1. Install `nox`
```bash
$ pip install nox
```
2. Run `nox` tests
```bash
$ nox --session unit_test -f noxfile.py
```

## Running Localy
1. Configure your environment's interpreter into your IDE
2. Make sure your `PATH` and `PYTHONPATH` env variables are configured properly
3. Open `web/app.py` and run the file via the IDE

## Running in Docker
1. Make sure you have `Docker` installed
2. `cd` to project root folder and build the image
```bash
$ docker build . -t vehicle-location-service
```
3. Run the image with exposed ports (make sure you're binded to the correct localhost - could also be `0.0.0.0`)
```bash
$ docker run -d -p 127.0.0.1:5000:5000 vehicle-location-service
```