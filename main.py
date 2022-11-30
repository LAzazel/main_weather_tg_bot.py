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
