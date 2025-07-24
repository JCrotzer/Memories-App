from flask_app import create_app, db
from flask_migrate import Migrate
from flask.cli import with_appcontext

app = create_app()
migrate = Migrate(app, db)

# This will allow flask CLI to work with the app
if __name__ == '__main__':
    app.run()
