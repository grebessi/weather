"""Initialize the app."""
from flask import Flask
from flask_restful import Api
from app.config import set_configuration
from flask_sqlalchemy import SQLAlchemy


class AppWrapper:
    """Proxy for the real app.

    This wrapper is responsible for creating
    and configurating the app.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the app."""
        self.app = Flask(*args, **kwargs)
        self.api = Api(self.app)
        self.presetup()
        self._db = SQLAlchemy(self.app)

    @property
    def config(self):
        """Get app config."""
        return self.app.config

    @property
    def db(self):
        """Get app db."""
        return self._db

    def presetup(self):
        """Make any configurations before calling setup."""
        set_configuration(self.app)

    def setup(self):
        """Make any setup before running the app."""
        # Avoid circular imports
        from app.routes import set_routes
        set_routes(self.api)

    def run(self):
        """Run the app."""
        self.setup()
        self.app.run()


appwrapper = AppWrapper(__name__)
