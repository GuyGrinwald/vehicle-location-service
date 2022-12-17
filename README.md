Sample Python Project
========================

This is a sample Python project for quick bootstrapping new projects.


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