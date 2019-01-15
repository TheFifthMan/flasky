from app import create_app,db
from app.auth.models import Role
from flask_migrate import Migrate
app = create_app('default')
migrate = Migrate(app, db)


@app.cli.command()
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@app.cli.command()
def deploy():
    Role.insert_roles()

