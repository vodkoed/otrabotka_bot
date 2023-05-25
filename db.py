"""import MySQLdb"""
import mysql.connector
'python -m pip install --upgrade pip'


class BotDB:
    """соединение с бд(базой данных)"""
    def __init__(self, db_file):
        """соединение с бд(базой данных)"""
        self.conn = mysql.connector.connect(user='root',
                                            host='127.0.0.1',
                                            password='',
                                            database='otrab01')
        self.cursor = self.conn.cursor(buffered=True)

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        self.cursor.execute("SELECT id FROM user WHERE user_id = %s", (user_id,))
        return bool(len(self.cursor.fetchall()))

    def add_user(self, user_id):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO user (user_id) VALUES (%s)", (user_id,))
        return self.conn.commit()

    def add_username(self, user_id, name):
        """Добавляем имя юзера в базу"""
        self.cursor.execute("UPDATE user SET name = %s WHERE user_id = %s", (name, user_id))
        return self.conn.commit()

    def add_user_nickname(self, user_id, nickname):
        """Добавляем ник юзера в базу"""
        self.cursor.execute("UPDATE user SET nickname = %s WHERE user_id = %s", (nickname, user_id))
        return self.conn.commit()

    def add_day(self, user_id, day):
        """Добавляем день когда юзер придёт на отработку в базу"""
        self.cursor.execute("UPDATE user SET day = %s WHERE user_id = %s", (user_id, day))
        return self.conn.commit()

    def add_admin_day(self, id, days, user_id, check_update):
        """Добавляем день тьютора в базу"""
        self.cursor.execute(
            "INSERT INTO admin (id, times, days, user_id, nickname, check_update) VALUES (%s, 2, %s, %s, 1, %s)",
            (id, days, user_id, check_update))
        return self.conn.commit()

    def add_admin_time2(self, times, user_id):
        """Добавляем время тьютора в базу"""
        self.cursor.execute("UPDATE admin SET times = %s WHERE user_id = %s AND times = '2'", (times, user_id))
        return self.conn.commit()

    def add_new_password(self, id, user_id, password, check_update):
        """Добавляем новый пароль для тьютора в базу"""
        self.cursor.execute(
            "INSERT INTO admin (id, days, times, password, user_id, nickname, check_update) VALUES (%s, 1, 1, %s, %s, 3, %s)",
            (id, user_id, password, check_update))
        return self.conn.commit()

    def add_time(self, user_id, time):
        """Добавляем время когда юзер придёт на отработку в базу"""
        self.cursor.execute("UPDATE user SET time = %s WHERE user_id = %s", (user_id, time))
        return self.conn.commit()

    def add_admin_id(self, user_id, password):
        """Добавляем админа в базу"""
        self.cursor.execute("UPDATE admin SET user_id = %s WHERE password = %s", (user_id, password))
        return self.conn.commit()

    def add_group(self, user_id, group_number):
        """Добавляем группу юзера в базу"""
        self.cursor.execute("UPDATE user SET group_number = %s WHERE user_id = %s", (user_id, group_number))
        return self.conn.commit()

    def select_time1(self, day):
        """достаём из бд время 1"""
        self.cursor.execute("SELECT time1 FROM time WHERE day = %s", (day,))
        output_text = ' '.join([' '.join(row) for row in self.cursor.fetchall()])
        return output_text

    def select_time_for_update1(self, day):
        """достаём из бд время 2"""
        self.cursor.execute("SELECT time1 FROM time WHERE day = %s", (day,))
        return self.cursor.fetchone()

    def select_time_for_update2(self, day):
        """достаём из бд время 2"""
        self.cursor.execute("SELECT time2 FROM time WHERE day = %s", (day,))
        return self.cursor.fetchone()

    def add_admin_nickname(self, nickname, password):
        """добавляем имя тьютора в базу"""
        self.cursor.execute("UPDATE admin SET nickname = %s WHERE password = %s", (nickname, password))
        return self.conn.commit()

    def select_password(self, user_id):
        """достаём пароль тьютора из бд"""
        self.cursor.execute("SELECT password FROM admin WHERE user_id = '%s' LIMIT 1", (user_id,))
        return self.cursor.fetchone()

    def select_user_id(self, password):
        """достаём пароль тьютора из бд"""
        self.cursor.execute("SELECT user_id FROM admin WHERE password = %s LIMIT 1", (password,))
        return self.cursor.fetchone()

    def select_root_password(self, id):
        """достаём корневой пароль из бд"""
        self.cursor.execute("SELECT password FROM admin WHERE id = %s", (id,))
        return self.cursor.fetchone()

    def select_time2(self, day):
        """достаём из бд время 2"""
        self.cursor.execute("SELECT time2 FROM time WHERE day = %s", (day,))
        output_text = ' '.join([' '.join(row) for row in self.cursor.fetchall()])
        return output_text

    def select_number_time(self, time, day):
        """достаём из бд количество юзеров с выбранным временем"""
        self.cursor.execute("SELECT COUNT(id) FROM user WHERE time = %s AND day = %s", (time, day))
        return self.cursor.fetchone()

    def select_need_day(self, times):
        """достаём из бд все дни всех тьюторов"""
        self.cursor.execute("SELECT days FROM admin WHERE times = %s", (times,))
        return self.cursor.fetchall()

    def select_need_day1(self, user_id):
        """достаём из бд всё время всех тьюторов"""
        self.cursor.execute("SELECT day FROM user WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()

    def select_user_day(self, user_id):
        """достаём из бд день юзера"""
        self.cursor.execute("SELECT day FROM user WHERE user_id = %s", (user_id,))
        output_text = ' '.join([' '.join(row) for row in self.cursor.fetchall()])
        return output_text

    def select_users_to_admin(self, day, time):
        """достаём из бд имя юзеров у которых время и день совпадают с тьютором"""
        self.cursor.execute("SELECT name FROM user WHERE day = %s AND time = %s", (day, time))
        output_text = ', '.join([' '.join(row) for row in self.cursor.fetchall()])
        return output_text

    def select_admin_time(self, user_id, id):
        """достаём из бд время тьютора"""
        self.cursor.execute("SELECT times FROM admin WHERE user_id = %s and id = %s", (user_id, id))
        return self.cursor.fetchone()

    def select_all_admins_and_days_for_update(self, check_update):
        """достаём из бд всё, что не относится к 1 админу и к корневому админу"""
        self.cursor.execute("SELECT days, times, user_id FROM admin WHERE check_update = %s", (check_update,))
        return self.cursor.fetchall()

    def select_first_admin_for_update_interval(self, check_update):
        """достаём из бд первый день или админа для обновления его айди"""
        self.cursor.execute("SELECT id FROM admin WHERE check_update = %s ORDER BY id LIMIT 1", (check_update,))
        return self.cursor.fetchone()

    def select_last_admin_not_for_update_interval(self, check_update):
        """достаём из бд последний день или админа чьё время уже обновлено"""
        self.cursor.execute("SELECT id FROM admin WHERE check_update != %s ORDER BY id DESC LIMIT 1", (check_update,))
        return self.cursor.fetchone()

    def select_last_admin_not_for_update(self, days, check_update):
        """достаём из бд последнего админа чьё время уже обновлено"""
        self.cursor.execute("SELECT id FROM admin WHERE days = %s AND check_update != %s ORDER BY id DESC LIMIT 1", (days, check_update))
        return self.cursor.fetchone()

    def select_admin_day(self, user_id, id):
        """достаём из бд дни тьютора"""
        self.cursor.execute("SELECT days FROM admin WHERE user_id = %s and id = %s", (user_id, id))
        return self.cursor.fetchone()

    def select_admin_count(self, user_id, nickname):
        """достаём из бд количество записей тьютора"""
        self.cursor.execute("SELECT count(id) FROM admin WHERE user_id = %s AND nickname = %s", (user_id, nickname))
        return self.cursor.fetchone()

    def select_admin_count_for_all_select(self, user_id):
        """достаём из бд количество айди тьютора где есть его юзер_айди тьютора"""
        self.cursor.execute("SELECT count(id) FROM admin WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()

    def select_admin_self_id(self, user_id, nickname):
        """достаём айди тьютора где есть его пароль"""
        self.cursor.execute("SELECT id FROM admin WHERE user_id = %s and nickname = %s", (user_id, nickname))
        return self.cursor.fetchone()

    def select_last_admin_id(self, user_id):
        """достаём из бд последний день тьютора"""
        self.cursor.execute("SELECT max(id) FROM admin WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()

    def select_admin_day_and_time(self, id):
        """достаём из бд последний день тьютора"""
        self.cursor.execute("SELECT days, times FROM admin WHERE id = %s", (id,))
        return self.cursor.fetchone()

    def select_last_admin(self, nickname):
        """достаём из бд последнего тьютора"""
        self.cursor.execute("SELECT max(id) FROM admin WHERE nickname != %s", (nickname,))
        return self.cursor.fetchone()

    def select_admin_user_id(self, id):
        """достаём из бд юзер_айди по айди"""
        self.cursor.execute("SELECT user_id FROM admin WHERE id = %s", (id,))
        return self.cursor.fetchone()

    def select_all_admins(self, nickname):
        """достаём из бд айди всех админов"""
        self.cursor.execute("SELECT id FROM admin WHERE nickname != %s", (nickname,))
        return self.cursor.fetchall()

    def select_all_admins1(self, nickname):
        """достаём из бд айди всех админов"""
        self.cursor.execute("SELECT password, nickname FROM admin WHERE nickname != %s", (nickname,))
        output_text = '\n'.join([', '.join(row) for row in self.cursor.fetchall()])
        return output_text

    def select_count_of_admins(self, nickname):
        """достаём из бд количество админов"""
        self.cursor.execute("SELECT COUNT(id) FROM admin WHERE nickname != %s", (nickname,))
        return self.cursor.fetchone()

    def select_all(self, user_id, nickname):
        """достаём из бд дни и время тьютора"""
        self.cursor.execute("SELECT days, times FROM admin WHERE user_id = %s and nickname = %s", (user_id, nickname))
        output_text = '\n'.join([' '.join(row) for row in self.cursor.fetchall()])
        return output_text

    def select_users_to_update_time(self, day, time):
        """достаём из бд количество админов"""
        self.cursor.execute("SELECT user_id FROM user WHERE day = %s AND time = %s", (day, time))
        return self.cursor.fetchall()

    def select_admins_to_update_time(self, days, times):
        """достаём из бд количество админов"""
        self.cursor.execute("SELECT id, user_id FROM admin WHERE days = %s AND times = %s", (days, times))
        return self.cursor.fetchall()

    def delete_all(self, user_id):
        """удаляем все дни и время тьютора"""
        self.cursor.execute("DELETE FROM admin WHERE user_id = %s AND nickname = '1'", (user_id,))
        return self.conn.commit()

    def delete_admin(self, password):
        """удаляем все дни и время тьютора"""
        self.cursor.execute("DELETE FROM admin WHERE password = %s", (password,))
        return self.conn.commit()

    def update_time_user(self, user_id):
        """удаляем все дни и время тьютора"""
        self.cursor.execute("UPDATE user SET time = %s WHERE user_id = %s", (user_id,))
        return self.conn.commit()

    def delete_last_day(self, id):
        """удаляем дни и время тьютора"""
        self.cursor.execute("DELETE FROM admin WHERE id = %s", (id,))
        return self.conn.commit()

    def delete_need_day(self, id):
        """удаляем дни и время тьютора"""
        self.cursor.execute("DELETE FROM admin WHERE id = %s", (id,))
        return self.conn.commit()

    def update_check_update(self, check_update, id):
        """обновляем check_update у 1 админа"""
        self.cursor.execute("UPDATE admin SET check_update = %s WHERE id > %s", (check_update, id))
        return self.conn.commit()

    def update_root_password(self, user_id):
        """обновляем check_update у 1 админа"""
        self.cursor.execute("UPDATE admin SET user_id = %s WHERE id = 1", (user_id,))
        return self.conn.commit()

    def start_update_check_update(self, check_update, id):
        """обновляем  check_update у всех админ кроме 1"""
        self.cursor.execute("UPDATE admin SET check_update = %s WHERE id < %s", (check_update, id))
        return self.conn.commit()

    def update_admin_day_id(self, id, check_update, days, times, user_id):
        """обновляем выбранное айди"""
        self.cursor.execute(
            "UPDATE admin SET id = %s, check_update = %s WHERE days = %s AND times = %s AND user_id = %s",
            (id, check_update, days, times, user_id))
        return self.conn.commit()

    def update_false_admin(self, user_id, nickname, id):
        """обновляем выбранное айди"""
        self.cursor.execute("UPDATE admin SET user_id = %s, nickname = %s WHERE id = %s", (user_id, nickname, id))
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
        self.cursor.execute("UPDATE admin SET id = %s WHERE days = %s AND times = %s", (id, days, times))
        return self.conn.commit()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
