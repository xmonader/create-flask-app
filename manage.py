import sys
import os
from datetime import datetime
from flask import Flask
from flask_graphql import GraphQLView
from flask_script import Manager
from sqlalchemy_utils import drop_database, create_database, database_exists
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from flask_potion import Api, ModelResource, fields
from resources import TodoResource
from schema import schema
import settings
from models import db, Todo

class EnhancedModelView(ModelView):
    can_view_details = True


app = Flask(__name__)
manager = Manager(app)
app.config.from_pyfile("settings.py")

# Extra configurations to override DB connection.
if os.getenv("EXTRA_CONFIG", False):
    app.config.from_envvar("EXTRA_CONFIG")

app.secret_key = app.config['SECRET_KEY']

db.app = app
db.init_app(app)


api = Api(app, prefix="/api/v1")
resources = [TodoResource]
for resource in resources:
    api.add_resource(TodoResource)



# app.config['BASIC_AUTH_USERNAME'] = 'admin'
# app.config['BASIC_AUTH_PASSWORD'] = 'admin'

# basic_auth = BasicAuth(app)


@manager.command
def dropdb():
    """Drop database and tables."""
    if app.config['BACKEND'] == "sqlite3":
        try:
            os.remove(app.config['DBPATH'])
        except:
            raise
    if database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        drop_database(app.config['SQLALCHEMY_DATABASE_URI'])

    print("Database dropped.")


@manager.command
def createdb():
    """Create database and tables."""
    # ensure database directory
    if app.config['BACKEND'] == 'sqlite3':
        if not os.path.exists(app.config['DBDIR']):
            os.mkdir(app.config['DBDIR'])
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])

    db.create_all(app=app)
    print("DB created.")


@manager.command
def resetdb():
    """Remove database and create it again."""
    dropdb()
    createdb()
    print("DB Resetted")


@manager.command
def loadfixtures():
    """Load test fixtures into database."""
    def generate_fixtures():
        t1 = Todo(title="create init flask app", done=False)
        t2 = Todo(title="Create elm app", done=False)
        t3 = Todo(title="Publish to github", done=False)
        db.session.add(t1)
        db.session.add(t2)
        db.session.add(t3)

    generate_fixtures()
    db.session.commit()
    print("Fixtures loaded.")


def main(host, port, debug=True):
    app.add_url_rule(
        '/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
    admin = Admin(app, name="Todos", template_mode="bootstrap3", url="/admin")
    admin.add_view(EnhancedModelView(Todo, db.session))
    app.run(debug=debug, host=host, port=port)


@manager.option("-h", "--host", help="host", default="0.0.0.0")
@manager.option("-p", "--port", help="port", default=5000)
def startapp(host, port=5000):
    """Starts the Flask-Todo."""
    main(host, int(port))


if __name__ == "__main__":
    manager.run()
