"""Clima Tempo Request Factory."""
import requests
from app.initialize import appwrapper as app
from urllib.parse import urlunparse
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.parse import urlencode
from datetime import datetime


class ClimaTempoAPI:
    """Request factory for Clima Tempo API."""

    def __init__(self, default_url=None):
        """Initialize ClimaTempoAPI."""
        self.default_url = app.config['CLIMA_TEMPO_URL']
        if default_url:
            self.default_url = default_url

    def _get_token(self):
        """Retrieve Clima Tempo Token."""
        return app.config['CLIMA_TEMPO_TOKEN']

    def _build_url(self, path, query_dict={}):
        """Build an url with urllib."""
        # join the base url with the path
        url = urljoin(self.default_url, path)

        # parse all the url components
        url_parts = list(urlparse(url))
        # update the query parameters with the authentication token
        query_dict.update({'token': self._get_token()})
        # set the parameters in the url
        url_parts[4] = urlencode(query_dict)
        # return all the pieces of the url together
        return urlunparse(url_parts)

    def forecast(self, city_id):
        """Call the forecast api filtered by city_id.

        Call the API
        http://apiadvisor.climatempo.com.br/doc/index.html#api-Forecast-Forecast15DaysByCity
        If the request is made successfully it will return:
            {
                'city': 'city_name',
                'state': 'state',
                'country': 'country',
                'weather': [
                    {
                        'date': datetime object,
                        'rain_probability': rain probability percentage,
                        'rain_precipitation': precipitation in milimiters,
                        'max_temperature': maximum temperature in celsius,
                        'min_temperature': minimum temperature in celsius,
                    }
                ]
            }
        If the requests fails, an dictionary with the key 'error' will be
        set, the key detail will have the reason for the request failure.
        """
        try:
            response = requests.get(
                self._build_url(f'forecast/locale/{city_id}/days/15'))
            if response.status_code == 400:
                return response.json()
            elif response.status_code != 200:
                raise requests.RequestException(
                    f'Server responded with {response.status_code}')
            api_response = response.json()
            return {
                'city': api_response['name'],
                'state': api_response['state'],
                'country': api_response['country'],
                'weather': [
                    {
                        'date': datetime.strptime(
                            weather_data['date'],
                            '%Y-%m-%d'
                        ).date(),
                        'rain_probability':
                            weather_data['rain']['probability'],
                        'rain_precipitation':
                            weather_data['rain']['precipitation'],
                        'max_temperature': weather_data['temperature']['max'],
                        'min_temperature': weather_data['temperature']['min'],
                    }
                    for weather_data in api_response['data']
                ],
            }

        except requests.RequestException as e:
            # Catch any requests lib exceptions
            # http://docs.python-requests.org/en/master/api/#exceptions

            return {
                'error': True,
                'detail': f'the following error occurred '
                          f'while making the request: {e}'
            }

        except Exception as e:
            if app.config['DEBUG']:
                return {
                    'error': True,
                    'detail': f'{e}',
                }
            # Do not return the error in production
            # since it can have sensitive data
            return {
                'error': True,
                'detail': f'An unknown error ocurred',
            }
