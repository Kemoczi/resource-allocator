import nox


@nox.session
def tests(session):
    session.install("-r", "requirements.txt")
    session.run("pytest", "-v")


@nox.session
def lint_app(session):
    session.install('flake8')
    session.run("flake8", "app/")


@nox.session
def lint_tests(session):
    session.install('flake8')
    session.run("flake8", "tests/")


@nox.session
def lint_project_root(session):
    session.install('flake8')
    session.run("flake8", "conftest.py", "noxfile.py")


@nox.session
def lint_behave(session):
    session.install('flake8')
    session.run("flake8", "features/")
