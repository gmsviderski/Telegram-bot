import telebot
import json
from datetime import datetime, timedelta

API_TOKEN = '7220002427:AAFs1V34yYNBGfoUJXfdFtbVkYYNhQhIU5c'

bot = telebot.TeleBot(API_TOKEN)

# Загрузка расписания из JSON файла
with open('schedule.json', 'r',  encoding='utf-8') as schedule_file:
    schedule = json.load(schedule_file)


def get_today_schedule():
    # Получаем полное название текущего дня недели в нижнем регистре.
    today = datetime.today().strftime('%A').lower()
    return schedule.get(today, [])


def get_tomorrow_schedule():
    tomorrow = (datetime.today() + timedelta(days=1)).strftime('%A').lower()
    return schedule.get(tomorrow, [])


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 "Привет! Я бот, который помогает отслеживать расписание занятий. Используйте команду /tomorrow "
                 "чтобы узнать расписание на завтра. Команда /help выведет список всех команд. ")


@bot.message_handler(commands=['today'])
def send_today_schedule(message):
    today_schedule = get_today_schedule()
    if today_schedule:
        response = "Сегодня у вас следующие занятия:\n" + "\n".join(today_schedule)
    else:
        response = "Сегодня у вас нет занятий."
    bot.reply_to(message, response)


@bot.message_handler(commands=['tomorrow'])
def send_tomorrow_schedule(message):
    tomorrow_schedule = get_tomorrow_schedule()
    if tomorrow_schedule:
        response = "Завтра у вас следующие занятия:\n" + "\n".join(tomorrow_schedule)
    else:
        response = "Завтра у вас нет занятий."
    bot.reply_to(message, response)


@bot.message_handler(commands=['schedule'])
def send_full_schedule(message):
    response = "Ваше полное расписание:\n"
    for day, lessons in schedule.items():
        response += f"{day.capitalize()}: {', '.join(lessons)}\n"
    bot.reply_to(message, response)


@bot.message_handler(commands=['help'])
def send_help(message):
    response = (
        "Список доступных команд:\n"
        "/start - Приветственное сообщение\n"
        "/today - Расписание на сегодня\n"
        "/tomorrow - Расписание на завтра\n"
        "/schedule - Расписание на неделю\n"
        "/help - Помощь"
    )
    bot.reply_to(message, response)


# Запуск бота
bot.polling()
