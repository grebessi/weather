"""Resources for the weather."""
from flask import jsonify
from flask_restful import Resource
from sqlalchemy import func

from app.initialize import appwrapper as app
from .climatempo import ClimaTempoAPI
from .models import City
from .models import WeatherEntry


class RetrieveCityWeather(Resource):
    """Retrieve the city weather from clima tempo saving it in the database."""

    def get(self, city_id):
        """Retrieve city weather data from clima tempo."""
        clima_tempo = ClimaTempoAPI()
        data = clima_tempo.forecast(city_id)
        if data.get('error'):
            return data, 400
        self._create_or_update_city_data(data)
        return jsonify(data)

    def _create_or_update_city_data(self, data):
        """Create or update city/weather entries accordingly to the data."""
        _, city = City.create_or_update(
            City.name == data['city'],
            City.state == data['state'],
            City.country == data['country'],
            defaults={
                'name': data['city'],
                'state': data['state'],
                'country': data['country'],
            }
        )
        for weather_data in data['weather']:
            WeatherEntry.create_or_update(
                WeatherEntry.city_id == city.id,
                WeatherEntry.date == weather_data['date'],
                defaults={
                    'city_id': city.id,
                    'date': weather_data['date'],
                    'rain_probability': weather_data['rain_probability'],
                    'rain_precipitation': weather_data['rain_precipitation'],
                    'max_temperature': weather_data['max_temperature'],
                    'min_temperature': weather_data['min_temperature'],
                },
                commit=False,
            )
        app.db.session.commit()


class WeatherAnalysis(Resource):
    """List a few statistical analysis in a date range.

    List the highest temperature registered in a city in a date range,
    with the average precipitation per city.
    """

    def get(self, initial_date, final_date):
        """Process all the data for the analysis."""
        hotest_city = (
            app.db.session.query(
                City.name,
                WeatherEntry.max_temperature.label('max_temperature'),
            )
            .join(WeatherEntry)
            .filter(
                WeatherEntry.date.between(initial_date, final_date),
            )
            .order_by(WeatherEntry.max_temperature.desc())
        ).first()

        precipitation_average = (
            app.db.session.query(
                func.avg(WeatherEntry.rain_precipitation)
                    .label('average_rain_precipitation'),
                City.name
            )
            .filter(WeatherEntry.date.between(initial_date, final_date))
            .join(City)
            .group_by(WeatherEntry.city_id, City.name)
        )

        return jsonify({
            'hotest_city': hotest_city,
            'precipitation_average': precipitation_average,
        })
