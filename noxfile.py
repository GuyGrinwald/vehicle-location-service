import nox

@nox.session
def lint(session):
    session.install("black")
    session.install("isort")
    session.run("isort", "sample/hello_world.py")
    session.run("black", "sample/hello_world.py")

@nox.session
def unit_test(session):
    session.install("-r", "requirements.txt")
    session.run("coverage", "run", "-m", "pytest")
