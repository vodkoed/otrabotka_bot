!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


Корневому админу дни и время не добавлять!


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
сайт хостинга pythonanywhere
убери прокси если тестируешь везде кроме этого сайта

        Если вы заливаете бота на сайт, то:
замените строчку bot = Bot(token=BOT_TOKEN) в файлах user_bot и teach_bot на bot = Bot(token=BOT_TOKEN,proxy="http://proxy.server:3128")
(в user_bot Bot(token=BOT_TOKEN1,proxy="http://proxy.server:3128") а в teach_bot Bot(token=BOT_TOKEN,proxy="http://proxy.server:3128")
,
в  def __init__ в db.file
замените:
    self.conn = mysql.connector.connect(user='root',
                                        post='127.0.0.1',
                                        password='',
                                        database='otrab01')
    self.cursor = self.conn.cursor(buffered=True)
на:
    self.conn = mysql.connector.connect(host='имя_пользователя.mysql.pythonanywhere-services.com',
                                        user='имя_пользователя',
                                        password='пароль_бд',
                                        database='имя_пользователя$название_бд')
    self.cursor = self.conn.cursor()'
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Памятка для корневого админа

Чтобы ввести новый интервал между админами(со страта он = 7) введитие - /new_admins_interval_корневойпароль \\например /new_admins_interval_222

Чтобы добавить нового админа введите - /add_new_admin_корневойпароль \\например  /add_new_admin_222

чтобы разлогиниться из обычного админа корневому введите - /unlog_корневойпароль \\например  /unlog_222 (учтите все дни этого админа удалятся)

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
config - там содержатся токены
db - там всё связанное с бд пояснения для функций там же
keyboards - там клавиатуры
teach_bot - бот тьютора
user_bot - бот для резидента
bot - файл для запуска обоих ботов


@dp.message_handler(commands=['start']) //активируется при написании команды в кавычках после /

message.get_args() // извлекает сообщение после команды

await message.delete() // удаляет сообщение

await callback.message.delete() // удаляет сообщение в коллбек_хэндлерах



await bot.send_message(chat_id=message.from_user.id,       //куда отправлять сообщение
                       text="Если вы хотите выбрать ещё один день выбирайте. "+commands, //текст сообщения
                       parse_mode='HTML',//если хочешь добавить например жирность
                       reply_markup=day_ikb)//клавиатура если стоит ReplyKeyboardRemove() то все кнопки кроме инлайновых убираются


!!!!Создание таблиц(ввести перед началом работы)!!!!
CREATE TABLE `admin` (
  `id` int NOT NULL,
  `days` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `times` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `password` varchar(40) DEFAULT NULL,
  `user_id` varchar(20) DEFAULT NULL,
  `nickname` varchar(33) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `check_update` tinyint(1) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `user` (
  `id` int NOT NULL,
  `day` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `time` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `nickname` varchar(33) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `name` varchar(70) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `group_number` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;



CREATE TABLE `time` (
  `day` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `time1` varchar(10) NOT NULL,
  `time2` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


!!!!добавление данных в таблицы!!!!

INSERT INTO `admin` (`id`, `days`, `times`, `password`, `user_id`, `nickname`, check_update) VALUES
(1, NULL, NULL, 'нужный корневой пароль', 'NULL', 'NULL', 0); //Корневой пароль, с помощью него добавляются новые пароли

INSERT INTO `admin` (`id`, `days`, `times`, `password`, `user_id`, `nickname`, check_update) VALUES
(2, '1', '1', '3342', '2', '3', 0);   // если лень вводить 1 админа

!!!Время нужно вставлять через двоеточие воттак(часы:минуты)(если времени нет, то вставляйте вместо 'xx:xx' - 'NULL')!!!
INSERT INTO `time` (`day`, `time1`, `time2`) VALUES
('Понедельник', 'xx:xx', 'xx:xx'),
('Вторник', 'xx:xx', 'xx:xx'),
('Среда', 'xx:xx', 'xx:xx'),
('Четверг', 'xx:xx', 'xx:xx'),
('Пятница', 'xx:xx', 'xx:xx'),
('Суббота', 'xx:xx', 'xx:xx'),
('Воскресенье', 'xx:xx', 'xx:xx');