import telebot
from deep_translator import GoogleTranslator
import requests
bot = telebot.TeleBot('1740625861:AAEEiil1vnFxh75qeOUosT-I8JX3lJLfprI')


def weather_data(city):
    """
    This function gets information about weather.
    """
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=5debcdaaac31debd6d746e9e24a4bb25"

    return requests.get(base_url).json()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    lang = message.from_user.language_code
    name = message.from_user.first_name
    reply = f"""Hello, {name}! \nI am bot, who will help you to find the weather forecast.\nTo start just enter city in wich you would like to see the forecast. If you need some help type "/help"."""
    translated = GoogleTranslator(
        source='auto', target=lang).translate(reply)
    bot.reply_to(
        message, translated)


@bot.message_handler(commands=['help'])
def send_help(message):
    lang = message.from_user.language_code
    reply = f"""To start just enter city in wich you would like to see the forecast."""
    translated = GoogleTranslator(
        source='auto', target=lang).translate(reply)
    bot.reply_to(
        message, translated)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    data = weather_data({GoogleTranslator(
        source='auto', target="en").translate(message.text)}.pop())

    lang = message.from_user.language_code
    try:
        if data["message"] == 'city not found':
            answer = "There is no such city("
            translated = GoogleTranslator(
                source='auto', target=lang).translate(answer)
            bot.send_message(message.from_user.id, translated)
    except KeyError:
        weather = GoogleTranslator(
            source='auto', target=lang).translate(data["weather"][0]["description"]).capitalize()
        forecast = f"""{weather}
{GoogleTranslator(
            source='auto', target=lang).translate("Temprature")} {round(int(data["main"]["temp"]) - 273.15)}°C
{GoogleTranslator(
            source='auto', target=lang).translate("Wind")} - {data["wind"]["speed"]}m/s"""
        bot.send_message(message.from_user.id, forecast)


bot.polling(none_stop=True, interval=0)
