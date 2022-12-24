#!/bin/sh
# This runs a gunicorn with a simple setup of a single worker. In other environments we should use multiple workers
gunicorn -w 1 -b 0.0.0.0:5000 --chdir web app:app