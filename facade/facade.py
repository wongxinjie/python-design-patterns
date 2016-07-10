# coding: utf-8
import json
import urllib
import urllib2
from datetime import datetime


class WeatherProvider(object):
    def __init__(self):
        self.api = 'http://api.openweathermap.org/data/2.5/forecast?q={},{}'

    def get_weather_data(self, city, country):
        city = urllib.quote(city)
        url = self.api_url.format(city, country)
        return urllib2.urlopen(url).read()


class Parser(object):

    def parse_weather_data(self, weather_data):
        parsed = json.loads(weather_data)
        start_date = None
        result = []

        for data in parsed['list']:
            date = datetime.strptime(data['dt_txt'], '%Y-%m-%d %H:%M:%S')
            start_date = start_date or date
            if start_date.day != date.day:
                return result
            result.append(data['main']['temp'])


class Converter(object):
    def from_kelvin_to_celcius(self, kelvin):
        return kelvin - 273.15


class Weather(object):
    def __init__(self, data):
        if not data:
            self.temperature = 0.0
        self.temperature = sum(data) / len(data)


class Facade(object):

    def forecast(self, city, country):
        weather_provider = WeatherProvider()
        weather_data = weather_provider.get_weather_data(city, country)

        parser = Parser()
        parsed_data = parser.parse_weather_data(weather_data)
        weather = Weather(parsed_data)
        converter = Converter()
        return converter.from_kelvin_to_celcius(weather.temperature)

if __name__ == "__main__":
    facade = Facade()
    print facade.forecast('London', 'UK')
