import os

from flask_migrate import upgrade
from flaskblog import create_app

app = create_app()

# Automatically apply any pending DB migrations on startup.
# This means `flask db upgrade` runs every time Render (re)starts the service,
# so we never need the paid Shell feature to run migrations manually.
with app.app_context():
    upgrade()


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "").lower() in ("1", "true", "yes")
    app.run(debug=debug)
