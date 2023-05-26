from aiogram import types, executor, Dispatcher, Bot
from config import BOT_TOKEN1
from aiogram.types import ReplyKeyboardRemove
from keyboards import day_ikb, time_kb1, time_kb2, time_kb3, time_kb4, time_kb5, time_kb6, time_kb7
from db import BotDB
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from mysql.connector.errors import DataError
import sys
"""память машины состояний"""
storage = MemoryStorage()

"""имя бд"""
BotDB = BotDB('otrab01.db')

"""бот, прокси"""
bot = Bot(token=BOT_TOKEN1)

"""диспатчер"""
dp = Dispatcher(bot=bot,
                storage=storage)

root_password = BotDB.select_root_password(1)[0]
"""создание кнопок времени ко всем дням исключая пустое время"""
day_mas = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
kb_mas = [time_kb1, time_kb2, time_kb3, time_kb4, time_kb5, time_kb6, time_kb7]
i = 0
checking_the_addition = False
while i <= 6:
    try:
        kb_mas[i].add(str(BotDB.select_time1(day_mas[i])), str(BotDB.select_time2(day_mas[i])))
        checking_the_addition = True
    except TypeError:
        kb_mas[i].add(str(BotDB.select_time2(day_mas[i])))
        checking_the_addition = True
    if checking_the_addition == False:
        try:
            kb_mas[i].add(str(BotDB.select_time1(day_mas[i])))
        except TypeError:
            checking_the_addition = False
    checking_the_addition = False
    i += 1


class StatesGroup(StatesGroup):
    """класс состояний мышины состояний"""
    name = State()
    group = State()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)

    await bot.send_message(chat_id=message.from_user.id,
                           text="если вы совершили где то ошибку начинайте заново нажав /start")
    BotDB.add_user_nickname(message.from_user.id, message.from_user.first_name)
    """бот отправляет сообщение с клавиатурой дней"""
    await bot.send_message(chat_id=message.from_user.id,
                           text="В какой день вы хотите пойти на отработку?",
                           parse_mode='HTML',
                           reply_markup=day_ikb)


@dp.callback_query_handler()
async def day_command(callback: types.CallbackQuery):
    await callback.message.delete()
    """бот проверяет коллбэк"""
    if callback.data == "day1":
        day = "Понедельник"
        kla = time_kb1
    if callback.data == "day2":
        day = "Вторник"
        kla = time_kb2
    if callback.data == "day3":
        day = "Среда"
        kla = time_kb3
    if callback.data == "day4":
        day = "Четверг"
        kla = time_kb4
    if callback.data == "day5":
        day = "Пятница"
        kla = time_kb5
    if callback.data == "day6":
        day = "Суббота"
        kla = time_kb6
    if callback.data == "day7":
        day = "Воскресенье"
        kla = time_kb7
    if callback.data == "day1" or "day2" or "day3" or "day4" or "day5" or "day6" or "day7":
        """Бот высылыает сообщение с кнопками времени"""
        await bot.send_message(callback.message.chat.id,
                               text=day,
                               reply_markup=kla)

        BotDB.add_day(day, callback.message.chat.id)
        await bot.send_message(chat_id=callback.message.chat.id,
                               text="Выберите время")


@dp.message_handler(lambda message: ':' in message.text)
async def user_command(message: types.Message):
    """проверка есть ли выбранные пользователем день и время у хоть 1 из тьюторов"""
    time_prov = False
    need_day = BotDB.select_need_day(message.text)
    user_day = BotDB.select_need_day1(message.from_user.id)[0]
    j = 0
    print(need_day)
    while len(need_day) >= j + 1:
        print(user_day)
        print(need_day[j])
        if need_day[j][0] == user_day:
            time_prov = True
        j += 1

    if time_prov == True:
        count_number = str(BotDB.select_number_time(message.text, BotDB.select_user_day(message.from_user.id))[0])
        time_prov = False
        if int(count_number) <= 4:
            BotDB.add_time(message.text, message.from_user.id)
            """бот убирает кнопки и отправляет сообщение"""
            await bot.send_message(chat_id=message.from_user.id,
                                   text="Введите ваши имя, фамилию, отчество.",
                                   parse_mode='HTML',
                                   reply_markup=ReplyKeyboardRemove())
            await StatesGroup.name.set()
        else:
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Выберете другое время или день',
                                   parse_mode='HTML',
                                   reply_markup=day_ikb)
    else:
        time_prov = False
        await bot.send_message(chat_id=message.from_user.id,
                               text=message.text,
                               parse_mode='HTML',
                               reply_markup=ReplyKeyboardRemove())
        await bot.send_message(chat_id=message.from_user.id,
                               text='Выберете другое время или день',
                               parse_mode='HTML',
                               reply_markup=day_ikb)


@dp.message_handler(state=StatesGroup.name)
async def user_command(message: types.Message, state: FSMContext):
    name = message.text
    """проверяет не слишком ли длинное введённое сообщение"""
    await state.finish()
    try:
        BotDB.add_username(message.from_user.id, name)
        """бот отправляет сообщение"""
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите номер вашей группы, если вы его не знаете пишите -",
                               parse_mode='HTML',
                               reply_markup=ReplyKeyboardRemove())
        await StatesGroup.group.set()
    except DataError:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите имя, фамилию, отчество заново, ваше сообщение слишком длинное.",
                               parse_mode='HTML',
                               reply_markup=ReplyKeyboardRemove())
        await StatesGroup.name.set()


@dp.message_handler(state=StatesGroup.group)
async def user_command(message: types.Message, state: FSMContext):
    group = message.text
    """проверяет не слишком ли длинное введённое сообщение"""
    try:
        await state.finish()
        BotDB.add_group(group, message.from_user.id)
        """бот отправляет сообщение"""
        await bot.send_message(chat_id=message.from_user.id,
                               text="Вы закончили всё заполнять, если хотите начать заново нажмите /start")
    except DataError:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите номер вашей группы заново, сообщение слишком длинное.",
                               parse_mode='HTML',
                               reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands=['alert_' + str(root_password)])
async def delete_admin_command(message: types.Message):
    await bot.send_message(message.from_user.id,
                           text="Уведомления отправлены")
    sys.exit()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
