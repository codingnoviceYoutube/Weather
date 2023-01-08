import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.graphics import Color
from kivy.graphics.vertex_instructions import Rectangle

import requests
import json

class WeatherApp(App):
    def build(self):
        self.location_input = TextInput(hint_text='Enter location')
        fetch_button = Button(text='Fetch Weather')
        fetch_button.bind(on_press=lambda instance: self.fetch_weather(fetch_button))
        self.weather_display = Label(text='', font_size=24)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.location_input)
        layout.add_widget(fetch_button)
        layout.add_widget(self.weather_display)
        self.root = layout
        return self.root

    def clear_input(self):
        self.location_input.text = ''
        self.weather_display.text = ''

    def fetch_weather(self, instance):
        # Fetch weather data from API
        location = self.location_input.text
        api_key = '35639f72dfa531720f5e6edcfd0eac23'
        api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(location, api_key)
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            temperature = data['main']['temp']
            # Convert temperature from Kelvin to Fahrenheit
            temperature_f = (temperature - 273.15) * 9 / 5 + 32
            # Update weather display
            self.weather_display.text = 'Temperature: {}°F'.format(temperature_f)
            # Change background color based on temperature
            self.root.canvas.clear()
            with self.root.canvas:
                if temperature_f > 80:
                    Color(1, 0.5, 0)
                elif temperature_f < 40:
                    Color(0.75, 0.75, 1)
                else:
                    Color(1, 1, 1)
                Rectangle(size=(self.root.size[0], self.root.size[1] / 3), pos=(self.root.pos[0], self.root.pos[1]))
            # Clear input fields
            self.clear_input()
        else:
            self.weather_display.text = 'Error fetching weather data'

if __name__ == '__main__':
    WeatherApp().run()
