"""Routes for views."""
from app.weather.resources import RetrieveCityWeather
from app.weather.resources import WeatherAnalysis


def set_routes(api):
    """Create weather routes."""
    api.add_resource(RetrieveCityWeather, '/city/<int:city_id>/')
    api.add_resource(
        WeatherAnalysis,
        '/city/analysis/<date:initial_date>/<date:final_date>'
    )
