from aiogram import types, executor, Dispatcher, Bot
from config import BOT_TOKEN
from aiogram.types import ReplyKeyboardRemove
from keyboards import day_ikb, time_kb1, time_kb2, time_kb3, time_kb4, time_kb5, time_kb6, time_kb7, day_kb, \
    time_kb_for_update
from db import BotDB
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import MessageTextIsEmpty, ChatNotFound
from mysql.connector.errors import IntegrityError

day_for_update = '1'
time_for_update = '1'
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
    day = State()
    time_for_update = State()
    update_time = State()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Добро пожаловать. Введите пароль чтобы войти")
    """ожидает сообщение с паролем от пользователя"""
    await StatesGroup.password.set()


@dp.message_handler(state=StatesGroup.password)
async def tutor_command(message: types.Message, state: FSMContext):
    try:
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
                BotDB.update_root_password(int(message.from_user.id) + 1)
                BotDB.add_admin_nickname('1', password)
            await message.delete()
            await bot.send_message(chat_id=message.from_user.id,
                                   text="Выберите день",
                                   parse_mode='HTML',
                                   reply_markup=day_ikb)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=commands)

            @dp.message_handler(commands=['new_admins_interval_' + str(root_password)])
            async def interval_command(message: types.Message):
                """удаляет лишние дни(если их больше чем новый интервал позволяет), обновляет айди всего"""
                global admins_interval
                last_interval = admins_interval
                admins_interval = message.get_args()
                all_admins = BotDB.select_all_admins('1')
                count_of_admins = BotDB.select_count_of_admins('1')[0]
                update_scroll = 0
                delete_scroll = 0
                all_for_update = BotDB.select_all_admins_and_days_for_update(1)

                BotDB.start_update_check_update(0, 2 + int(last_interval))
                while count_of_admins >= delete_scroll + 1:
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

                        last_admin_not_for_update1 = BotDB.select_last_admin_not_for_update('1', 1)[0]
                        user_id = all_for_update[update_scroll][2]
                        day = all_for_update[update_scroll][0]
                        time = all_for_update[update_scroll][1]
                        if need_interval == 1:
                            need_interval = first_admin_for_update
                        else:
                            need_interval = last_admin_not_for_update + 1
                        if day == '1':
                            BotDB.update_admin_day_id(last_admin_not_for_update1 + int(admins_interval) + 1, 0, day,
                                                      time, user_id)
                        else:
                            BotDB.update_admin_day_id(need_interval + 1, 0, day, time, user_id)
                        update_scroll += 1
                except TypeError:
                    BotDB.update_check_update(1, 2)
                BotDB.update_check_update(1, 2)

            @dp.message_handler(commands=['add_new_admin_' + str(root_password)])
            async def new_admin_command(message: types.Message):
                await message.delete()
                new_password = message.get_args()
                """эта функция добавляет нового админа."""
                try:
                    password_id = int(BotDB.select_last_admin('1')[0]) + admins_interval + 1
                    BotDB.add_new_password(password_id, new_password, password_id, 1)
                except TypeError:
                    password_id = 2
                    BotDB.add_new_password(password_id, new_password, password_id, 0)
                await bot.send_message(message.from_user.id,
                                       text="Админ добавлен.")

            @dp.message_handler(commands=['unlog_' + str(root_password)])
            async def unlog_command(message: types.Message):
                await message.delete()
                try:
                    admin_id = BotDB.select_admin_self_id(message.from_user.id, message.from_user.first_name)[0]
                    """эта функция разлогинивает корневого админа из обычного"""

                    BotDB.update_false_admin(admin_id, '3', admin_id)

                    await bot.send_message(message.from_user.id,
                                           text="Вы вышли.")
                    BotDB.delete_all(message.from_user.id)
                except TypeError:
                    await bot.send_message(message.from_user.id,
                                           text="Вы не заходили")

            @dp.message_handler(commands=['all_admins_' + str(root_password)])
            async def all_admins_command(message: types.Message):
                await message.delete()
                all_admins = BotDB.select_all_admins1('1')
                """эта функция показывает всех админов"""
                await bot.send_message(message.from_user.id,
                                       text="Пароль, никнейм")
                await bot.send_message(message.from_user.id,
                                       text=all_admins)

            @dp.message_handler(commands=['delete_admin_' + str(root_password)])
            async def delete_admin_command(message: types.Message):
                await message.delete()
                password_for_delete = message.get_args()
                admin_for_delete = BotDB.select_user_id(password_for_delete)[0]

                BotDB.delete_all(admin_for_delete)
                BotDB.delete_admin(password_for_delete)
                """эта функция удаляет админа и все его дни"""

                await bot.send_message(message.from_user.id,
                                       text="Админ успешно удалён")

            @dp.message_handler(commands=['update_time_' + str(root_password)])
            async def select_day_command(message: types.Message):
                await message.delete()
                await bot.send_message(message.from_user.id,
                                       text="Введите день, у которого хотите обновить время.",
                                       reply_markup=day_kb)
                await StatesGroup.day.set()

            @dp.message_handler(state=StatesGroup.day)
            async def update_time_command(message: types.Message):
                global day_for_update
                await message.delete()
                await state.finish()
                day_for_update = message.text
                await bot.send_message(message.from_user.id,
                                       text=message.text,
                                       reply_markup=ReplyKeyboardRemove())
                await bot.send_message(message.from_user.id,
                                       text='Введите, что вы хотите обновить',
                                       reply_markup=time_kb_for_update)
                time1 = BotDB.select_time_for_update1(day_for_update)[0]
                await bot.send_message(message.from_user.id,
                                       text='Текущее время для time1 - ' + time1)
                time2 = BotDB.select_time_for_update2(day_for_update)[0]
                await bot.send_message(message.from_user.id,
                                       text='Текущее время для time2 - ' + time2)
                await StatesGroup.time_for_update.set()

            @dp.message_handler(state=StatesGroup.time_for_update)
            async def update_time_command(message: types.Message):
                global time_for_update
                await message.delete()
                await state.finish()
                time_for_update = message.text
                await bot.send_message(message.from_user.id,
                                       text=message.text,
                                       reply_markup=ReplyKeyboardRemove())
                await bot.send_message(message.from_user.id,
                                       text='Введите, на какое время вы хотите поменять текущее. Вводите так'
                                            ' часы:время (xx:xx)')
                await StatesGroup.update_time.set()

            @dp.message_handler(state=StatesGroup.update_time)
            async def update_time_command(message: types.Message):
                global time_for_update
                global day_for_update
                global admins_interval
                await state.finish()
                await message.delete()
                if time_for_update == 'time1':
                    last_time = BotDB.select_time_for_update1(day_for_update)[0]
                    BotDB.update_time1(message.text, day_for_update)

                if time_for_update == 'time2':
                    last_time = BotDB.select_time_for_update2(day_for_update)[0]
                    BotDB.update_time2(message.text, day_for_update)
                j = 0
                users_to_update_time = BotDB.select_users_to_update_time(day_for_update, last_time)
                admins_to_update_time = BotDB.select_admins_to_update_time(day_for_update, last_time)
                while len(users_to_update_time) > j:
                    await bot.send_message(users_to_update_time[0],
                                           text='Ваше время записи теперь недоступно, если вы хотите записаться на'
                                                ' отработку, запишитесь снова на другое время.')
                    j += 1
                j = 0
                print(admins_to_update_time)
                while len(admins_to_update_time) > j:
                    this_admin = admins_to_update_time[j][1]
                    this_admin_id = admins_to_update_time[j][0]
                    BotDB.delete_need_day(this_admin_id)
                    last_day_id = BotDB.select_last_admin_id(this_admin)[0]
                    last_day_and_time = BotDB.select_admin_day_and_time(last_day_id)
                    try:
                        BotDB.update_day_id(this_admin_id, last_day_and_time[0], last_day_and_time[1])
                    except IntegrityError:
                        k = 0
                    try:
                        await bot.send_message(this_admin,
                                               text='Ваше время записи ' + day_for_update + ' ' + last_time + ' теперь недоступно, так что его пришлось удалить, извиняемся за неудобство')
                    except ChatNotFound:
                        k = 0
                    j += 1
                await bot.send_message(message.from_user.id,
                                       text=message.text,
                                       reply_markup=ReplyKeyboardRemove())
                await bot.send_message(message.from_user.id,
                                       text='Время успешно обновлено')

            @dp.message_handler(commands=['help_' + str(root_password)])
            async def help_command(message: types.Message):
                await message.delete()
                """эта функция показывает все команды корневого админа"""
                await bot.send_message(message.from_user.id,
                                       text="Чтобы ввести новый интервал между админами(со старта он = 7) введитие - /new_admins_interval_корневойпароль \\например /new_admins_interval_222"
                                            "\n\nЧтобы добавить нового админа введите - /add_new_admin_корневойпароль \\например  /add_new_admin_222"
                                            "\n\nчтобы разлогиниться из обычного админа корневому введите - /unlog_корневойпароль \\например  /unlog_222 (учтите все дни этого админа удалятся)"
                                            "\n\nчтобы увидеть всех админов введите - /all_admins_корневойпароль \\например  /all_admins_222 (3 в никнейме означает что пароль никем не занят)"
                                            "\n\nчтобы удалить админа введие - /delete_admin_корневойпароль пароль (пароль админа которого хотите удалить) \\например /delete_admin_222 152"
                                            "\n\nчтобы увидеть все команды в телеграмме введите - /help_корневойпароль \\например /help_222")

            @dp.callback_query_handler()
            async def day_command(callback: types.CallbackQuery):
                await callback.message.delete_reply_markup()
                await callback.message.delete()
                try:
                    last_admin_id = int(BotDB.select_last_admin_id(callback.message.chat.id)[0]) + 1
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
                        """если добавленных дней больше интервала то добавлять больше нельзя, если нужно изменить 
                        максимальное количество дней то измените инервал с помощью команды на нужное число"""
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

                            BotDB.add_admin_day(str(last_admin_id), day, callback.message.chat.id, 1)
                            await StatesGroup.time.set()
                except TypeError:
                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Нельзя добавлять дни корневому админу! Если хотите добавить себе дни "
                                                "войдите в аккаунт не корневого админа.")

            @dp.message_handler(state=StatesGroup.time)
            async def time_command(message: types.Message):
                await state.finish()
                try:
                    """проверяет время ли введено"""
                    check_int = int(message.text[0:1])
                    check_int1 = int(message.text[3:4])
                    await message.delete()
                    """добавляет введённое время"""
                    BotDB.add_admin_time2(message.text, message.from_user.id)
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
                                           text=message.text,
                                           reply_markup=ReplyKeyboardRemove())
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
                                       text="Все ваши дни удалены.",
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
                        admin_day = str(BotDB.select_admin_day(message.from_user.id, admin_id + 1)[0])
                        admin_time = str(BotDB.select_admin_time(message.from_user.id, admin_id + 1)[0])
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
    except TypeError:
        await bot.send_message(message.from_user.id,
                               text="Введите пароль заново.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)