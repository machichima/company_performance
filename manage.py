from flask_script import Manager
from flask.cli import FlaskGroup
from app import app, db
cli = FlaskGroup(app)

manager = Manager(app)


if __name__ == '__main__':
    manager.run()