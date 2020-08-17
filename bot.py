import config
import telebot
from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve

"""Делаем гороскоп-бота, который парсит сегодняшний гороскоп с сайта"""
#Difficult: Low

bot = telebot.TeleBot(config.TOKEN)


zodiac_dict = {'Овен': '?znak=aries',
               'Телец': '?znak=taurus',
               'Близнецы': '?znak=gemini',
               'Рак': '?znak=cancer',
               'Лев':'?znak=leo',
               'Дева':'?znak=virgo',
               'Весы':'?znak=libra',
               'Скорпион': '?znak=scorpio',
               'Стрелец': '?znak=sagittarius',
               'Козерог':'?znak=capricorn',
               'Водолей':'?znak=aquarius',
               'Рыбы':'?znak=pisces'}


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Хочешь узнать гороскоп на сегодня? Напиши мне "Гороскоп"')


@bot.message_handler(content_types=['text'])
def make_choice_zodiac(message):
    if message.text == 'Гороскоп' or message.text == 'гороскоп':
        msg =  bot.send_message(message.chat.id, 'Какой у тебя знак зодиака?')
        bot.register_next_step_handler(msg, show_horoscope)
    else:
        bot.send_message(message.chat.id, 'Упс! Я не знаю, что ты написал, попробуй снова!:)')

@bot.message_handler(content_types=['text'])
def show_horoscope(message):
    if message.text in zodiac_dict:
        resp = urlopen('https://1001goroskop.ru/{}'.format(zodiac_dict[message.text]))
        html = resp.read()
        soup = BeautifulSoup(html, 'html.parser')
        horoscope_text = soup.find('p')
        bot.send_message(message.chat.id, horoscope_text.get_text())
    else:
        bot.send_message(message.chat.id, 'Я не знаю такого знака зодиака. Извини меня :(')


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)
