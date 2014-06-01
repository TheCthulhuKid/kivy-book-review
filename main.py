from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton

from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest

from kivy.factory import Factory

import json


class LocationButton(ListItemButton):
    pass


class WeatherRoot(BoxLayout):
    current_weather = ObjectProperty()

    def show_add_location_form(self):
        self.clear_widgets()
        self.add_widget(AddLocationForm())

    def show_current_weather(self, location=None):
        self.clear_widgets()

        if location is None and self.current_weather is None:
            location = "Vienna (AT)"

        if location is not None:
            self.current_weather = Factory.CurrentWeather()
            self.current_weather.location = location

        self.add_widget(self.current_weather)


class AddLocationForm(BoxLayout):
    search_input = ObjectProperty()
    search_results = ObjectProperty()
    location_form = ObjectProperty()

    def search_location(self):
        if len(self.search_input.text) == 0:
            self.search_results.item_strings = ["You did not enter a location"]
            return
        search_template = "http://api.openweathermap.org/data/2.5/find?q={}&type=like"
        search_url = search_template.format(self.search_input.text)
        request = UrlRequest(search_url, self.found_location)

    def found_location(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        self.search_results.item_strings = cities
        self.search_results.adapter.data.clear()
        self.search_results.adapter.data.extend(cities)
        self.search_results._trigger_reset_populate()


class WeatherApp(App):
    pass


if __name__ == '__main__':
    WeatherApp().run()