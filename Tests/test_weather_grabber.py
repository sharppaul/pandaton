from unittest import TestCase
import weather
import json
import requests


class test_weather_grabber(TestCase):
    def test_get_current_weather(self):
        weather_functions = weather.WeatherGrabber()

        self.assertIsInstance(weather_functions.get_current_weather("Dordrecht"), weather.Weather)
        self.assertIsNone(weather_functions.get_current_weather(None))
        self.assertFalse(weather_functions.get_current_weather("4585239"))
        self.assertFalse(weather_functions.get_current_weather(False))
        self.assertFalse(weather_functions.get_current_weather(734))

    def test_prepare_wheather(self):
        request = requests.get("https://api.openweathermap.org/data/2.5/weather?q={0}&APPID={1}".format("Dordrecht",
                                                                                                        "a25b24117bec726b9c93c34d988c9c9a"))
        data = json.loads(request.content.decode('utf-8'))
        weather_functions = weather.WeatherGrabber()

        self.assertIsInstance(weather_functions.prepare_wheather(data), weather.Weather)
        self.assertIsNone(weather_functions.prepare_wheather(None), weather.Weather)
        self.assertIsNone(weather_functions.prepare_wheather("4983y834y680"), weather.Weather)
        self.assertIsNone(weather_functions.prepare_wheather(124322532234), weather.Weather)
