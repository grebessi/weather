"""Create the database."""
from app.initialize import appwrapper as app

# Import weather models
from app.weather.models import * # noqa

app.db.create_all()
