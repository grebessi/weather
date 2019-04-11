"""Custom url converters."""
from datetime import datetime
from datetime import date
from flask.json import JSONEncoder
from werkzeug.routing import BaseConverter
from werkzeug.routing import ValidationError


class DateConverter(BaseConverter):
    """Parse date from path."""

    regex = r'\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        """Parse date from string to date object."""
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValidationError()

    def to_url(self, value):
        """Convert date object to string."""
        return value.strftime('%Y-%m-%d')


class CustomJSONEncoder(JSONEncoder):
    """Define custom JSON encoding for apis."""

    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
