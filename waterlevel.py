import json
import requests


class WaterLevel:
    API_LINK = 'https://waterinfo.rws.nl/api/details/chart?mapType=waterhoogte-t-o-v-nap&values=-48,48&locationCode=3524'

    def __init__(self):
        self.data = None

    def load(self):
        r = requests.get(WaterLevel.API_LINK)
        if r.status_code == 200:
            content = r.content.decode('utf-8')
            self.data = json.loads(content)
            return True, self.data
        else:
            print(r.status_code)
            return False, r.status_code

    def get_level(self, timedelta=0):
        if self.data is not None:
            data = self.data['series'][0]['data'][-1 - timedelta]
            return data['value'], data['dateTime']
        else:
            return 0, False


if __name__ == "__main__":
    l = WaterLevel()
    l.load()
    print(l.get_level())
