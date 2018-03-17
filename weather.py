import requests
import json


class Wind:
    def __init__(self, speed, degrees):
        self.speed = speed
        self.degrees = degrees

    def __str__(self):
        return "{}km/h, {} degrees".format(self.speed, self.degrees)


class Location:
    def __init__(self, city, country):
        self.city = city
        self.country = country

    def __str__(self):
        return "{}, {}".format(self.city, self.country)


class Weather:
    def __init__(self, city, country, wind_speed, wind_direction, visibility, temperature, pressure, humidity,
                 condition):
        # Put certain information into classes
        prepared_location = Location(city, country)
        prepared_wind = Wind(wind_speed, wind_direction)

        self.location = prepared_location
        self.wind = prepared_wind
        self.visibility = visibility
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.condition = condition

    def __str__(self):
        return "Location: {},\n Windspeed: {},\n Visibility: {},\n Temp: {},\n Pressure: {},\n Humidity: {}," \
               "\n Condition: {}".format(self.location, self.wind, self.visibility, self.temperature, self.pressure,
                                         self.humidity, self.condition)


class WeatherGrabber:
    def __init__(self):
        self.key = "a25b24117bec726b9c93c34d988c9c9a"

    def get_current_weather(self, city):
        if city is not None and type(city) == str:
            # Get the data
            request = requests.get(
                "https://api.openweathermap.org/data/2.5/weather?q={0}&APPID={1}".format(city, self.key))

            # Check the status code
            if request.status_code == 200:
                # Decode the received data
                wheather_data = json.loads(request.content.decode('utf-8'))

                # Return a prepared weather object
                return self.prepare_wheather(wheather_data)

        # Return null
        return None

    def prepare_wheather(self, weather_data):
        if weather_data is not None:
            try:
                # Prepare the weather data to make it convertable into a weather object
                prepared_city = weather_data['name']
                prepared_country = weather_data['sys']['country']
                prepared_wind_speed = weather_data['wind']['speed']
                prepared_wind_degrees = weather_data['wind']['deg']
                prepared_visibility = weather_data['visibility']
                prepared_temperature = weather_data['main']['temp']
                prepared_pressure = weather_data['main']['pressure']
                prepared_humidity = weather_data['main']['humidity']
                prepared_condition = ""
            except:
                return None

            # Loop over the condition in order to create a condition string
            for condition in weather_data['weather']:
                prepared_condition = prepared_condition + condition['main'].lower() + ", "

            # Remove the last two characters
            prepared_condition = prepared_condition[:-2]

            # Return a new weather object containing the prepared data
            return Weather(prepared_city, prepared_country, prepared_wind_speed, prepared_wind_degrees,
                           prepared_visibility, prepared_temperature, prepared_pressure, prepared_humidity,
                           prepared_condition)
