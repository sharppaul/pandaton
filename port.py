from enum import Enum

import waterlevel
import weather
import datetime


class Status(Enum):
    Free = 1
    Arriving = 2
    Busy = 3
    Departing = 4
    Reserved = 5
    Maintenaince = 6
    Unavailable = 7


class DockingPurpose(Enum):
    Loading = 1
    Unloading = 2


class Ship:
    def __init__(self, ship_name, base_depth, full_depth, base_height, full_height, max_containers, containers,
                 purpose='No purpose given'):
        self.ship_name = ship_name
        self.base_depth = base_depth
        self.full_depth = full_depth
        self.base_height = base_height
        self.full_height = full_height
        self.max_containers = max_containers
        self.containers = containers
        self.purpose = purpose
        self.busy = False

    def __str__(self):
        str_ = "Ship {} with base depth {} and loaded depth {}".format(self.ship_name, self.base_depth, self.full_depth)
        str_ += "\n Unloaded height {}, fully loaded height: {}".format(self.base_height, self.full_height)
        str_ += "\n Loaded {}/{} containers".format(self.containers, self.max_containers)
        str_ += "\n It's purpose is: {}, and it's currently busy: {}".format(self.purpose, self.busy)
        return str_

    def get_status(self):
        return "{} busy: {}, with {}/{} containers. Height: {}, Depth: {}".format(self.ship_name, self.busy,
                                                                                    self.containers,
                                                                                    self.max_containers,
                                                                                    self.get_height(), self.get_depth())

    def get_depth(self):
        if self.max_containers == self.containers:
            return self.full_depth
        elif self.containers == 0:
            return self.base_depth
        else:
            singular_weight = (self.full_depth - self.base_depth) / self.max_containers
            return self.base_depth + (singular_weight * self.containers)

    def get_height(self):
        if self.max_containers >= self.containers:
            return self.base_height
        elif self.containers <= 0:
            return self.full_height
        else:
            singular_height = (self.full_height - self.base_height) / self.max_containers
            return self.base_height + (singular_height * self.containers)

    def process_actions(self):
        if self.busy:
            if self.purpose == DockingPurpose.Unloading:
                self.containers = self.containers - 1

                if self.containers <= 0:
                    self.containers = 0
                    self.busy = False
            else:
                self.containers = self.containers + 1

                if self.containers >= self.max_containers:
                    self.containers = self.max_containers
                    self.busy = False


class Dock:
    def __init__(self, dock_name):
        self.dock_name = dock_name
        self.state = Status.Free
        self.processed_containers = 0
        self.docked_ship = None

    def dock_ship(self, ship: Ship):
        self.docked_ship = ship
        self.state = Status.Arriving

    def process(self):
        if self.docked_ship is not None:
            if self.state == Status.Arriving:
                self.state = Status.Busy
                self.docked_ship.busy = True

            elif self.state == Status.Busy:
                if self.docked_ship.busy:
                    self.processed_containers += 1
                    self.docked_ship.process_actions()
                else:
                    self.state = Status.Departing

            elif self.state == Status.Departing:
                self.state = Status.Free
                self.docked_ship = None
        else:
            print('Dock has no ship!  {}'.format(self.dock_name))

    def __str__(self):
        return "Dock {} status: {}, processed containers: {}".format(self.dock_name, self.state, self.processed_containers)


class Port:
    def __init__(self, name, city, depth, docks):
        # Create an instance of the weather class
        self.weather_functions = weather.WeatherGrabber()
        self.waterlevel_functions = waterlevel.WaterLevel()
        self.waterlevel_functions.load()

        self.name = name
        self.city = city
        self.depth = depth
        self.docks = docks
        self.weather = self.weather_functions.get_current_weather(self.city)
        self.last_weather_update = datetime.datetime.now()

    def check_weather(self):
        if self.last_weather_update < datetime.datetime.today() - datetime.timedelta(hours=1):
            self.weather = self.weather_functions.get_current_weather(self.city)
        warnings = []

        if self.weather.visibility <= 1000:
            warnings.append('Visibility is too bad!')

        elif self.weather.wind.speed > 8.0:
            warnings.append('Wind is too strong!')

        return len(warnings) < 1, warnings

    def check_custom_weather(self, visibility, windspeed):
        if self.last_weather_update < datetime.datetime.today() - datetime.timedelta(hours=1):
            self.weather = self.weather_functions.get_current_weather(self.city)
        warnings = []

        if self.weather.visibility <= visibility:
            warnings.append('Visibility is too bad!')

        elif self.weather.wind.speed > windspeed:
            warnings.append('Wind is too strong!')

        return len(warnings) < 1, warnings

    def check_water(self, ship):
        relative, datetime = self.waterlevel_functions.get_level()
        if datetime:
            return ship.get_depth() < self.depth + relative
        else:
            print('Couldnt retrieve weather data!')
            return False

    def request_place(self, ship):
        soon_available = []

        if self.check_weather():
            if self.check_water(ship):
                for _dock in self.docks:
                    if _dock.state == Status.Free:
                        return True, _dock
                    elif _dock.state == Status.Departing:
                        soon_available.append(_dock)

                if len(soon_available) > 0:
                    return False, 'Soon available'
            else:
                return False, 'Water level is too low to dock!'
        else:
            return False, 'Bad weather! {}'.format(self.weather)
        return False, 'Unavailable'

    def __str__(self):
        return "Port {}, in {}, with {} docks, weather: \n {}".format(self.name, self.city, len(self.docks),
                                                                      self.weather)
