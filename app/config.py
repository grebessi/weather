"""Custom configuration related to the app settings."""
from flask_environ import get
from flask_environ import collect
from flask_environ import word_for_true
from app.converters import CustomJSONEncoder
from app.converters import DateConverter


def set_configuration(app):
    """Define the configurations for an app."""
    app.config.update(collect(
        get('DEBUG', default=True, convert=word_for_true),
        get('HOST', default='0.0.0.0'),
        get('PORT', default=5000, convert=int),
        get('SQLALCHEMY_DATABASE_URI', default='sqlite:////tmp/app.db'),
        get(
            'CLIMA_TEMPO_URL',
            default='http://apiadvisor.climatempo.com.br/api/v1/'
        ),
        get('CLIMA_TEMPO_TOKEN'),
    ))
    app.json_encoder = CustomJSONEncoder
    app.url_map.converters['date'] = DateConverter
