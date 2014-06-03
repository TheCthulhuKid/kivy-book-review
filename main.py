from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton

from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
from kivy.network.urlrequest import UrlRequest

from kivy.factory import Factory

import json

api_url = "http://api.openweather.org/data/2.5"


def locations_args_converter(index, data_item):
    city, country = data_item
    return {'location': (city, country)}


class LocationButton(ListItemButton):
    location = ListProperty()


class WeatherRoot(BoxLayout):
    current_weather = ObjectProperty()

    def show_add_location_form(self):
        self.clear_widgets()
        self.add_widget(AddLocationForm())

    def show_current_weather(self, location=None):
        self.clear_widgets()

        if self.current_weather is None:
            self.current_weather = CurrentWeather()

        if location is not None:
            self.current_weather.location = location

        self.current_weather.update_weather()
        self.add_widget(self.current_weather)


class CurrentWeather(BoxLayout):
    location = ListProperty(['Vienna', 'AT'])
    conditions = StringProperty()
    temp = NumericProperty()
    temp_min = NumericProperty()
    temp_max = NumericProperty()

    def update_weather(self):
        weather_template = api_url + "weather?q={},{}&units=metric"
        weather_url = weather_template.format(*self.location)
        request = UrlRequest(weather_url, self.weather_retrieved)

    def weather_retrieved(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        self.conditions = data['weather'][0]['description']
        self.temp = data['main']['temp']
        self.temp_min = data['main']['temp_min']
        self.temp_max = data['main']['temp_max']


class AddLocationForm(BoxLayout):
    search_input = ObjectProperty()
    search_results = ObjectProperty()
    location_form = ObjectProperty()

    def search_location(self):
        if len(self.search_input.text) == 0:
            self.search_results.item_strings = ["You did not enter a location"]
            return
        search_template = api_url + "find?q={}&type=like"
        search_url = search_template.format(self.search_input.text)
        request = UrlRequest(search_url, self.found_location)

    def found_location(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        cities = [(d['name'], d['sys']['country']) for d in data['list']]
        self.search_results.item_strings = cities
        self.search_results.adapter.data.clear()
        self.search_results.adapter.data.extend(cities)
        self.search_results._trigger_reset_populate()


class WeatherApp(App):
    pass


if __name__ == '__main__':
    WeatherApp().run()