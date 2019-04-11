"""Models for the weather."""
from app.initialize import appwrapper as app

db = app.db


class CreateOrUpdateMixin:
    """Mixin that create the behavior of an 'upsert'."""

    @classmethod
    def create_or_update(cls, *args, **kwargs):
        """Create or update an instance of the class.

        Makes a query based on kwargs.
        If we find the instance, we update it with defaults
        otherwise we create it with kwargs and defaults.

        Return a tuple:
            (was_created, instance)
        """
        defaults = kwargs.pop('defaults', {})
        commit = kwargs.pop('commit', True)
        instance = cls.query.filter(*args, **kwargs).first()
        if instance is not None:
            for key, value in defaults.items():
                setattr(instance, key, value)
            was_created = False
        else:
            instance = cls(**defaults)
            was_created = True
        db.session.add(instance)
        if commit:
            db.session.commit()
        return (was_created, instance)


class City(CreateOrUpdateMixin, db.Model):
    """Model that represents a city.

    This model has the attributes:
      id -- Unique identifier for the city
      name -- Name of the city
      state -- State abreviation in which the city belongs.
      country -- Country abreviation the city is in.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    country = db.Column(db.String(3), nullable=False)

    def __repr__(self):
        """Representation of the city."""
        return f'{self.name} - {self.state}'


class WeatherEntry(CreateOrUpdateMixin, db.Model):
    """Model that represents a weather entry.

    This model has the attributes:
      id -- Unique identifier for the city
      city_id -- Identification of the city in which the weather
                 entry was gathered
      date -- Date of the entry
      rain_probability -- percentual probability of rain
      rain_precipitation -- precipitation in milimeters
      max_temperature -- the maximun temperature in degrees celsius 
      min_temperature -- the minimum temperature in degrees celsius
      city -- Direct relation with city
    """

    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    rain_probability = db.Column(db.Integer, nullable=False)
    rain_precipitation = db.Column(db.Integer, nullable=False)
    max_temperature = db.Column(db.Integer, nullable=False)
    min_temperature = db.Column(db.Integer, nullable=False)

    city = db.relationship(
        'City',
        backref=db.backref('weather_entries', lazy=True)
    )

    def __repr__(self):
        """Representation of a weather entry."""
        return f'{self.city} - {self.date:%Y-%m-%d}'
