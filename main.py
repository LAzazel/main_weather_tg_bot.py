import requests
import datetime
import telebot
import os
from flask import Flask, request
from config import open_weather_token
from aiogram import types


TOKEN = str(os.environ.get('TOKEN'))
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


@bot.message_handler(commands=['start'])
def start_command(message: types.Message):
    bot.send_message(message.chat.id, "Hi! Write a city name and get a weather forecast!")
    

@bot.message_handler()
def get_weather(message: types.Message):
    code_to_smile = {
        'Clear': 'Clear \U00002600',
        'Clouds': 'Cloudy \U00002601',
        'Rain': 'Rainy \U00002614',
        'Drizzle': 'Drizzly \U00002614',
        'Thunderstorm': 'Thunder \U000026A1',
        'Snow': 'Snowy \U0001F328',
        'Fog': 'Foggy \U0001F32B',
    }

    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric'
        )
        data = r.json()

        city = data['name']
        current_weather = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Can't describe the weather today."

        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(
            data['sys']['sunrise'])

        bot.send_message(message.chat.id, f'***{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}***\n'
              f'Current weather in: {city}\nTemperature: {current_weather}°C {wd}\n'
              f'Humidity: {humidity}%\nPressure: {pressure} mm Hg\nWind: {wind} mps\n'
              f'Sunrise: {sunrise_timestamp}\nSunset: {sunset_timestamp}\nLength of the day: {length_of_the_day}\n'
              f'***Have a nice day!***'
              )
    except:
        bot.send_message(message.chat.id, '\U0000274C Wrong city name \U0000274C')
        

@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return '!', 200


@app.route('/')
def web_hook():
    bot.remove_webhook()
    bot.set_webhook(url='https://weather-bot.herokuapp.com/' + TOKEN)
    return '!', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
