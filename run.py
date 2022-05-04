#!/usr/bin/env python
from flask_script import Manager, Server

from app import create_app, db
from app.models import User, Role, Review

# Create app instance
app = create_app('testing')
manager = Manager(app)
manager.add_command('server', Server)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, user=User, role=Role, review=Review)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
