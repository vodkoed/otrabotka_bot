"""!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Teach_bot!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""


@dp.message_handler(commands=['update_time' + str(root_password)])
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
    day_for_update = message.text
    await bot.send_message(message.from_user.id,
                           text=message.text,
                           reply_markup=ReplyKeyboardRemove())
    await bot.send_message(message.from_user.id,
                           text='Введите, что вы хотите обновить',
                           reply_markup=time_kb_for_update)
    await StatesGroup.time_for_update.set()


@dp.message_handler(state=StatesGroup.time_for_update)
async def update_time_command(message: types.Message):
    global time_for_update
    await message.delete()
    time_for_update = message.text
    await bot.send_message(message.from_user.id,
                           text=message.text,
                           reply_markup=ReplyKeyboardRemove())
    await bot.send_message(message.from_user.id,
                           text='Введите, на какое время вы хотите поменять текущее. Вводите так'
                                ' часы:время (xx:xx)')
    await StatesGroup.time_for_update.set()


@dp.message_handler(state=StatesGroup.update_time)
async def update_time_command(message: types.Message):
    global time_for_update
    global day_for_update
    global admins_interval
    await message.delete()
    if message.text == 'time1':
        last_time = BotDB.select_time_for_update1(day_for_update)
        BotDB.update_time1(message.text, day_for_update)

    if message.text == 'time2':
        last_time = BotDB.select_time_for_update2(day_for_update)
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
    k = 0
    while len(admins_to_update_time) > j:
        this_admin = admins_to_update_time[j][1]
        this_admin_id = admins_to_update_time[j][0]
        await bot.send_message(this_admin,
                               text='Ваше время записи ' + day_for_update + ' ' + last_time + ' теперь недоступно, так что его пришлось удалить, извиняемся за неудобство')
        BotDB.delete_need_day(this_admin_id)
        last_day_id = BotDB.select_last_admin_id(this_admin)[0]
        last_day_and_time = BotDB.select_admin_day_and_time(last_day_id)
        BotDB.update_day_id(this_admin_id, last_day_and_time[0], last_day_and_time[1])
    await bot.send_message(message.from_user.id,
                           text=message.text,
                           reply_markup=ReplyKeyboardRemove())
    await bot.send_message(message.from_user.id,
                           text='Время успешно обновлено')


"""!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!keyboards!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""


def select_time_for_update1(self, day):
    """достаём из бд время 2"""
    self.cursor.execute("SELECT time1 FROM time WHERE day = %s", (day,))
    return self.cursor.fetchone()


def select_time_for_update2(self, day):
    """достаём из бд время 2"""
    self.cursor.execute("SELECT time2 FROM time WHERE day = %s", (day,))
    return self.cursor.fetchone()


def select_admin_day_and_time(self, id):
    """достаём из бд последний день тьютора"""
    self.cursor.execute("SELECT days, times FROM admin WHERE id = %s", (id,))
    return self.cursor.fetchone()


def select_users_to_update_time(self, day, time):
    """достаём из бд количество админов"""
    self.cursor.execute("SELECT user_id FROM user WHERE day = %s AND time = %s", (day, time))
    return self.cursor.fetchall()


def select_admins_to_update_time(self, days, times):
    """достаём из бд количество админов"""
    self.cursor.execute("SELECT id, user_id FROM admin WHERE days = %s AND times = %s", (days, times))
    return self.cursor.fetchall()


def update_time_user(self, user_id):
    """удаляем все дни и время тьютора"""
    self.cursor.execute("UPDATE user SET time = %s WHERE user_id = %s", (user_id,))
    return self.conn.commit()


def delete_need_day(self, id):
    """удаляем дни и время тьютора"""
    self.cursor.execute("DELETE FROM admin WHERE id = %s", (id,))
    return self.conn.commit()


def update_time1(self, time1, day):
    """обновляем выбранное айди"""
    self.cursor.execute("UPDATE time SET time1 = %s WHERE day = %s", (time1, day))
    return self.conn.commit()


def update_time2(self, time2, day):
    """обновляем выбранное айди"""
    self.cursor.execute("UPDATE time SET time2 = %s WHERE day = %s", (time2, day))
    return self.conn.commit()


def update_day_id(self, id, days, times):
    """обновляем выбранное айди"""
    self.cursor.execute("UPDATE admin SET id = %s WHERE days = %s, times = %s", (id, days, times))
    return self.conn.commit()
