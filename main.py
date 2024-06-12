import telebot
import json
from datetime import datetime

API_TOKEN = 'Вставьте ваш токен'

bot = telebot.TeleBot(API_TOKEN)

# Загрузка расписания из JSON файла
with open('schedule.json', 'r',  encoding='utf-8') as schedule_file:
    schedule = json.load(schedule_file)


def get_today_schedule():
    # Получаем полное название текущего дня недели в нижнем регистре.
    today = datetime.today().strftime('%A').lower()
    return schedule.get(today, [])


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 "Привет! Я бот, который помогает отслеживать расписание занятий. Используйте команду /today "
                 "чтобы узнать расписание на сегодня. Или команду /schedule чтобы узнать полное расписание. ")


@bot.message_handler(commands=['today'])
def send_today_schedule(message):
    today_schedule = get_today_schedule()
    if today_schedule:
        response = "Сегодня у вас следующие занятия:\n" + "\n".join(today_schedule)
    else:
        response = "Сегодня у вас нет занятий."
    bot.reply_to(message, response)


@bot.message_handler(commands=['schedule'])
def send_full_schedule(message):
    response = "Ваше полное расписание:\n"
    for day, lessons in schedule.items():
        response += f"{day.capitalize()}: {', '.join(lessons)}\n"
    bot.reply_to(message, response)


# Запуск бота
bot.polling()
