from aiogram import types, executor, Dispatcher, Bot
from config import BOT_TOKEN
from aiogram.types import ReplyKeyboardRemove
from keyboards import day_ikb, time_kb1, time_kb2, time_kb3, time_kb4, time_kb5, time_kb6, time_kb7
from db import BotDB
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import MessageTextIsEmpty

admins_interval = 7
last_id = 0
"""память машины состояний"""
storage = MemoryStorage()

"""имя бд"""
BotDB = BotDB('otrab011.db')

"""бот, прокси"""
bot = Bot(token=BOT_TOKEN)

"""диспатчер"""
dp = Dispatcher(bot=bot,
                storage=storage)
"""список дней"""
day_mas = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
"""список клавиату"""
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

commands = "Откройте меню чтобы посмотреть какие команды тут есть."


class StatesGroup(StatesGroup):
    """класс состояний мышины состояний"""
    password = State()
    time = State()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Добро пожаловать. Введите пароль чтобы войти")
    """ожидает сообщение с паролем от пользователя"""
    await StatesGroup.password.set()


@dp.message_handler(state=StatesGroup.password)
async def tutor_command(message: types.Message, state: FSMContext):
    """извелекает пароль"""
    password = message.text
    BotDB.add_admin_id(message.from_user.id, password)
    pasw = str(BotDB.select_password(message.from_user.id)[0])
    """проверяет пароль с введёнными"""
    if pasw == password:
        root_password = BotDB.select_root_password(1)[0]
        """обнуляет состояние"""
        await state.finish()
        if password != root_password:
            BotDB.add_admin_nickname(message.from_user.first_name, password)
        else:
            BotDB.add_admin_nickname('1', password)
        await message.delete()
        await bot.send_message(chat_id=message.from_user.id,
                               text="Выберите день",
                               parse_mode='HTML',
                               reply_markup=day_ikb)
        await bot.send_message(chat_id=message.from_user.id,
                               text=commands)

        @dp.message_handler(commands=['new_admins_interval_'+str(root_password)])
        async def use_command(message: types.Message):
            """удаляет лишние дни(если их больше чем новый интервал позволяет), обновляет айди всего"""
            global admins_interval
            admins_interval = message.get_args()
            all_admins = BotDB.select_all_admins('1')
            count_of_admins = BotDB.select_count_of_admins('1')[0]

            delete_scroll = 0
            all_for_update = BotDB.select_all_admins_and_days_for_update(1)

            BotDB.start_update_check_update(0, int(admins_interval)+2)

            while count_of_admins >= delete_scroll+1:
                user_id = BotDB.select_admin_user_id(all_admins[delete_scroll][0])[0]
                count_records = BotDB.select_admin_count(user_id, '1')[0]
                delete_records = count_records
                while delete_records - int(admins_interval) > 0:
                    BotDB.delete_last_day(BotDB.select_last_admin_id(user_id)[0])
                    delete_records -= 1
                delete_scroll += 1
            try:
                update_scroll = 0
                while len(all_for_update) >= update_scroll:
                    first_admin_for_update = BotDB.select_first_admin_for_update_interval(1)[0]
                    last_admin_not_for_update = BotDB.select_last_admin_not_for_update_interval(1)[0]
                    need_interval = first_admin_for_update - last_admin_not_for_update

                    ddassad = BotDB.select_last_admin_not_for_update('1', 1)[0]

                    user_id = all_for_update[update_scroll][2]
                    day = all_for_update[update_scroll][0]
                    time = all_for_update[update_scroll][1]

                    if need_interval == 1:
                        need_interval = first_admin_for_update
                    else:
                        need_interval = last_admin_not_for_update + 1

                    if day == '1':
                        BotDB.update_admin_day_id(ddassad + int(admins_interval) + 1, 0, day, time, user_id)
                    else:
                        BotDB.update_admin_day_id(need_interval, 0, day, time, user_id)
                    update_scroll += 1
            except TypeError:
                BotDB.update_check_update(1, int(admins_interval) + 2)
            BotDB.update_check_update(1, int(admins_interval) + 2)

        @dp.message_handler(commands=['add_new_admin_'+str(root_password)])
        async def use_command(message: types.Message):
            await message.delete()
            new_password = message.get_args()
            """эта функция добавляет нового админа."""
            if BotDB.select_last_admin('1')[0] != 'None':
                password_id = int(BotDB.select_last_admin('1')[0]) + admins_interval + 1
            else:
                password_id = 2
            BotDB.add_new_password(password_id, new_password)

        @dp.callback_query_handler()
        async def day_command(callback: types.CallbackQuery):
            await callback.message.delete_reply_markup()
            await callback.message.delete()
            """бот проверяет коллбэк и выбирает нужнею клавиатуру с днём"""
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
                count_days = int(BotDB.select_admin_count(callback.message.chat.id, '1')[0])
                """если добавленных дней больше интервала то добавлять больше нельзя, если нужно изменить максимальное
                 количество дней то измените инервал с помощью команды на нужное число"""
                if count_days > admins_interval:
                    await bot.send_message(callback.message.chat.id,
                                           text="место кончилось")
                    BotDB.delete_last_day(BotDB.select_last_admin_id(message.from_user.id))
                    await bot.send_message(chat_id=message.from_user.id,
                                           text=commands)
                """Бот высылыает сообщение с кнопками времени"""
                if count_days <= admins_interval:
                    await bot.send_message(callback.message.chat.id,
                                           text=day,
                                           reply_markup=kla)
                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Выберите время")
                    last_admin_id = int(BotDB.select_last_admin_id(callback.message.chat.id)[0]) + 1
                    BotDB.add_admin_day(str(last_admin_id), day, callback.message.chat.id, 1)
                    await StatesGroup.time.set()

        @dp.message_handler(state=StatesGroup.time)
        async def time_command(message: types.Message):
            await state.finish()
            try:
                """проверяет время ли введено"""
                check_int = int(message.text[0:1])
                check_int1 = int(message.text[3:4])
                await message.delete()
                """добавляет введённое время"""
                await bot.send_message(chat_id=message.from_user.id,
                                       text=message.text,
                                       parse_mode='HTML',
                                       reply_markup=ReplyKeyboardRemove())
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Если вы хотите выбрать ещё один день выбирайте. " + commands,
                                       reply_markup=day_ikb)
                await bot.send_message(chat_id=message.from_user.id,
                                       text=commands)
            except ValueError:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Не балуйтесь со временем! Начинайте выбор дня сначала.',
                                       reply_markup=day_ikb)
                """Удаляет день без времени"""
                BotDB.delete_last_day(BotDB.select_last_admin_id(message.from_user.id)[0])

        @dp.message_handler(commands=['add_day'])
        async def add_command(message: types.Message):
            await bot.send_message(chat_id=message.from_user.id,
                                   text="Выберите день",
                                   parse_mode='HTML',
                                   reply_markup=day_ikb)

        @dp.message_handler(commands=['select_all'])
        async def select_command(message: types.Message):
            """показывает все дни тьютора"""
            await bot.send_message(chat_id=message.from_user.id,
                                   text="/end",
                                   parse_mode='HTML',
                                   reply_markup=ReplyKeyboardRemove())
            days_count = str(BotDB.select_admin_count_for_all_select(message.from_user.id)[0])
            if days_count == '1':
                await bot.send_message(chat_id=message.from_user.id,
                                       text='У вас нет дней',
                                       parse_mode='HTML',
                                       reply_markup=ReplyKeyboardRemove())
                await bot.send_message(chat_id=message.from_user.id,
                                       text=commands,
                                       parse_mode='HTML',
                                       reply_markup=day_ikb)
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text=BotDB.select_all(message.from_user.id, '1'),
                                       parse_mode='HTML',
                                       reply_markup=ReplyKeyboardRemove())
                await bot.send_message(chat_id=message.from_user.id,
                                       text=commands,
                                       parse_mode='HTML')

        @dp.message_handler(commands=['delete_all'])
        async def delete_command(message: types.Message):
            """удаляет все дни тьютора"""
            BotDB.delete_all(message.from_user.id)
            """бот отправляет сообщение"""
            await bot.send_message(chat_id=message.from_user.id,
                                   text="udoleno",
                                   parse_mode='HTML',
                                   reply_markup=ReplyKeyboardRemove())
            await bot.send_message(chat_id=message.from_user.id,
                                   text=commands,
                                   parse_mode='HTML',
                                   reply_markup=day_ikb)

        @dp.message_handler(commands=['look_all'])
        async def look_command(message: types.Message):
            """показывает всех пользователей у которых день и время совпадает с тьютором"""

            admin_id = BotDB.select_admin_self_id(message.from_user.id, message.from_user.first_name)[0]
            number = 0
            count_records = BotDB.select_admin_count(message.from_user.id, '1')[0]
            await bot.send_message(chat_id=message.from_user.id,
                                   text="все пользователи у которых день и время совпадает с вашим: ",
                                   parse_mode='HTML',
                                   reply_markup=ReplyKeyboardRemove())
            try:
                while number <= count_records:
                    admin_day = str(BotDB.select_admin_day(message.from_user.id, admin_id+1)[0])
                    admin_time = str(BotDB.select_admin_time(message.from_user.id, admin_id+1)[0])
                    mes = BotDB.select_users_to_admin(admin_day, admin_time)
                    await bot.send_message(chat_id=message.from_user.id,
                                           text=mes)
                    admin_id += 1
                    number += 1
            except MessageTextIsEmpty:
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Пользователей, записанных на выбранное вами время нет",
                                       parse_mode='HTML',
                                       reply_markup=ReplyKeyboardRemove())
            await bot.send_message(chat_id=message.from_user.id,
                                   text=commands,
                                   parse_mode='HTML',
                                   reply_markup=ReplyKeyboardRemove())



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)