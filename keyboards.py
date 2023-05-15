from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton,\
    InlineKeyboardMarkup
from db import BotDB

day_kb = ReplyKeyboardMarkup(resize_keyboard=True)

day_kb.add(KeyboardButton('Понедельник'), KeyboardButton('Вторник'),  KeyboardButton('Среда'), KeyboardButton('Четверг')
           , KeyboardButton('Пятница'), KeyboardButton('Суббота'), KeyboardButton('Воскресенье'))
"""клавитуры для каждого дня"""
time_kb = ReplyKeyboardMarkup(resize_keyboard=True)
time_kb1 = ReplyKeyboardMarkup(resize_keyboard=True)
time_kb2 = ReplyKeyboardMarkup(resize_keyboard=True)
time_kb3 = ReplyKeyboardMarkup(resize_keyboard=True)
time_kb4 = ReplyKeyboardMarkup(resize_keyboard=True)
time_kb5 = ReplyKeyboardMarkup(resize_keyboard=True)
time_kb6 = ReplyKeyboardMarkup(resize_keyboard=True)
time_kb7 = ReplyKeyboardMarkup(resize_keyboard=True)

"""инлайн клавиатура дней"""
day_ikb = InlineKeyboardMarkup(row_width=2)

day_ikb.add(InlineKeyboardButton('Понедельник', callback_data="day1"), InlineKeyboardButton('Вторник', callback_data="day2"),
            InlineKeyboardButton('Среда', callback_data="day3"), InlineKeyboardButton('Четверг', callback_data="day4"),
            InlineKeyboardButton('Пятница', callback_data="day5"), InlineKeyboardButton('Суббота', callback_data="day6"),
            InlineKeyboardButton('Воскресенье', callback_data="day7"))
