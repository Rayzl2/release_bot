import telebot
from telebot import types
import sqlite3 as sl
from validate_email import validate_email
import time
from config import *
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import time

e = None
bot = telebot.TeleBot(token)

#registartion function

@bot.message_handler(commands=['start'])
def start(message):
	print(message.chat.id)
	try:
		user_id = message.from_user.id

		conn = sl.connect("database.db")
		cur = conn.cursor()
		cur.execute("SELECT user_id FROM users WHERE user_id=" + str(user_id))
		res = cur.fetchone()
		cur.execute("SELECT id FROM users order by id desc limit 1")
		id_acc = cur.fetchone()[0]
		print(user_id)
		cur.execute("INSERT INTO users (user_id) VALUES ("+ str(user_id) + ")")
		print(cur.fetchall())
		conn.commit()
	except:
		pass

	cur.execute(f"SELECT verify FROM users WHERE user_id={message.from_user.id}""")
	res = cur.fetchone()[0]
	if res == 'YES':
		keyboard = types.InlineKeyboardMarkup()
		btn1 = types.InlineKeyboardButton(text="Разместить объявление", callback_data="post")
		btn2 = types.InlineKeyboardButton(text="Связаться с поддержкой", callback_data="support")
		keyboard.add(btn1, btn2)
		msg = bot.send_message(message.chat.id, 'Добро пожаловать в главное меню!', reply_markup = keyboard)

	else:
		keyboard = types.InlineKeyboardMarkup()
		button_accept = types.InlineKeyboardButton(text="Начать", callback_data="start")
		keyboard.add(button_accept)
		bot.send_message(message.chat.id, 'Для того, чтобы начать размещать объявления, нужно пройти регистрацию, которая займет пару минут!', reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: True)
def inline(c):
    if c.data=='reg':
        msg = bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text="Укажите ваше Имя и Фамилию",
            parse_mode="markdown")
        
        bot.register_next_step_handler(msg, collect_phone)

    elif c.data=='start':
    	conn = sl.connect("database.db")
    	cur = conn.cursor()
    	keyboard = types.InlineKeyboardMarkup()
    	button_accept = types.InlineKeyboardButton(text="Подписался", callback_data="sub")
    	link = types.InlineKeyboardButton(text="Подписаться", url='https://t.me/+axHLFW28L3U1YjA8')
    	keyboard.add(button_accept, link)
    	bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text="Для работы с ботом вам необходимо быть подписанным на канал tuffstuffxvintage",
            parse_mode="markdown",
            reply_markup=keyboard)


    elif c.data=='sub':
    	conn = sl.connect("database.db")
    	cur = conn.cursor()
    	cur.execute(f"SELECT user_id FROM users WHERE user_id ={c.message.chat.id}""")
    	res = cur.fetchone()[0]
    	print(res)
    	res = bot.get_chat_member(chat_id=channel, user_id=res)
    	print(res)
    	if res.status == 'member':
    		key = types.ReplyKeyboardRemove()
	    	msg = bot.send_message(c.message.chat.id, 'Укажите ваши имя и фамилию', reply_markup=key)
	    	bot.delete_message(c.message.chat.id, c.message.message_id)
	    	bot.register_next_step_handler(msg, get_name)
    	
    	else:
    		keyboard = types.InlineKeyboardMarkup()
    		button_accept = types.InlineKeyboardButton(text="Подписался", callback_data="sub")
    		link = types.InlineKeyboardButton(text="Перейти", url='https://t.me/+axHLFW28L3U1YjA8')
    		keyboard.add(button_accept, link)
    		bot.edit_message_text(chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text="Вы не подписаны. Повторите попытку!",
            parse_mode="markdown", reply_markup= keyboard)

    elif c.data == 'support':

    	keyboard = types.InlineKeyboardMarkup()
    	btn1 = types.InlineKeyboardButton(text="Разместить объявление", callback_data="post")
    	btn2 = types.InlineKeyboardButton(text="Связаться с поддержкой", callback_data="support")
    	keyboard.add(btn1, btn2)
    	msg = bot.send_message(c.message.chat.id, 'Связаться с менеджером: @tuffstuffxvintagetelega\nДобро пожаловать в главное меню!', reply_markup = keyboard)

    elif c.data=='post':
    	keyboard = types.InlineKeyboardMarkup(row_width=4)
    	btn1 = types.InlineKeyboardButton(text='Одежда', callback_data='clothes')
    	btn2 = types.InlineKeyboardButton(text='Сумки', callback_data='bags')
    	btn3 = types.InlineKeyboardButton(text='Обувь', callback_data='shoes')
    	btn5 = types.InlineKeyboardButton(text='Аксессуары', callback_data='acs')
    	keyboard.add(btn1, btn2, btn3, btn5)
    	msg = bot.send_message(c.message.chat.id, 'Давайте узнаем, что за товар вы хотите разместить? Какая категория?', reply_markup = keyboard)

    elif c.data == 'clothes':
    	conn = sl.connect("database.db")
    	cur = conn.cursor()
    	cur.execute(f"INSERT INTO goods (user_id) VALUES ('{c.message.chat.id}')")
    	cur.execute(f"SELECT id FROM goods WHERE user_id = '{c.message.chat.id}' order by id DESC limit 1")
    	res = cur.fetchone()[0]
    	keyboard = types.ReplyKeyboardRemove()
    	cur.execute(f"UPDATE goods SET category = 'Одежда' WHERE id={res}")
    	conn.commit()
    	msg = bot.send_message(c.message.chat.id, 'Спасибо, в каком городе находится вещь?', reply_markup = keyboard)
    	bot.register_next_step_handler(msg, get_city)

    elif c.data == 'bags':
    	conn = sl.connect("database.db")
    	cur = conn.cursor()
    	cur.execute(f"INSERT INTO goods (user_id) VALUES ('{c.message.chat.id}')")
    	cur.execute(f"SELECT id FROM goods WHERE user_id = '{c.message.chat.id}' order by id DESC limit 1")
    	res = cur.fetchone()[0]
    	keyboard = types.ReplyKeyboardRemove()
    	cur.execute(f"UPDATE goods SET category = 'Сумки' WHERE id={res}")
    	conn.commit()
    	msg = bot.send_message(c.message.chat.id, 'Спасибо, в каком городе находится вещь?', reply_markup = keyboard)
    	bot.register_next_step_handler(msg, get_city)

    elif c.data == 'shoes':
    	conn = sl.connect("database.db")
    	cur = conn.cursor()
    	cur.execute(f"INSERT INTO goods (user_id) VALUES ('{c.message.chat.id}')")
    	cur.execute(f"SELECT id FROM goods WHERE user_id = '{c.message.chat.id}' order by id DESC limit 1")
    	res = cur.fetchone()[0]
    	keyboard = types.ReplyKeyboardRemove()
    	cur.execute(f"UPDATE goods SET category = 'Обувь' WHERE id={res}")
    	conn.commit()
    	msg = bot.send_message(c.message.chat.id, 'Спасибо, в каком городе находится вещь?', reply_markup = keyboard)
    	bot.register_next_step_handler(msg, get_city)
    
    elif c.data == 'acs':
    	conn = sl.connect("database.db")
    	cur = conn.cursor()
    	cur.execute(f"INSERT INTO goods (user_id) VALUES ('{c.message.chat.id}')")
    	cur.execute(f"SELECT id FROM goods WHERE user_id = '{c.message.chat.id}' order by id DESC limit 1")
    	res = cur.fetchone()[0]
    	keyboard = types.ReplyKeyboardRemove()
    	cur.execute(f"UPDATE goods SET category = 'Аксессуары' WHERE id={res}")
    	conn.commit()
    	msg = bot.send_message(c.message.chat.id, 'Спасибо, в каком городе находится вещь?', reply_markup = keyboard)
    	bot.register_next_step_handler(msg, get_city)

    elif c.data == 'new':
    	keyboard=types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    	btn1 = types.KeyboardButton(text='ГОТОВО')
    	keyboard.add()
    	conn = sl.connect("database.db")
    	cur = conn.cursor()

    	cur.execute(f"SELECT id FROM goods WHERE user_id = '{c.message.chat.id}' order by id DESC limit 1")
    	res = cur.fetchone()[0]

    	cur.execute(f"UPDATE goods SET status = 'Новое с биркой' WHERE id={res}")
    	conn.commit()
    	msg = bot.send_message(c.message.chat.id, 'Спасибо. Теперь можно загрузить до 10 фотографий. \nВАЖНО! Отправляйте фото по отдельности!\n Нажмите кнопку снизу, когда загрузите нужные фото', reply_markup = keyboard)
    	bot.register_next_step_handler(msg, photo)

    elif c.data == 'also_new':
    	keyboard=types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    	btn1 = types.KeyboardButton(text='ГОТОВО')
    	keyboard.add()
    	conn = sl.connect("database.db")
    	cur = conn.cursor()

    	cur.execute(f"SELECT id FROM goods WHERE user_id = '{c.message.chat.id}' order by id DESC limit 1")
    	res = cur.fetchone()[0]

    	cur.execute(f"UPDATE goods SET status = 'Как новое' WHERE id={res}")
    	conn.commit()
    	msg = bot.send_message(c.message.chat.id, 'Спасибо. Теперь можно загрузить до 10 фотографий. \nВАЖНО! Отправляйте фото по отдельности!\n Нажмите кнопку снизу, когда загрузите нужные фото', reply_markup = keyboard)
    	bot.register_next_step_handler(msg, photo)

    elif c.data == 'good':
    	keyboard=types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    	btn1 = types.KeyboardButton(text='ГОТОВО')
    	keyboard.add()
    	conn = sl.connect("database.db")
    	cur = conn.cursor()

    	cur.execute(f"SELECT id FROM goods WHERE user_id = '{c.message.chat.id}' order by id DESC limit 1")
    	res = cur.fetchone()[0]

    	cur.execute(f"UPDATE goods SET status = 'Хорошее' WHERE id={res}")
    	conn.commit()
    	msg = bot.send_message(c.message.chat.id, 'Спасибо. Теперь можно загрузить до 10 фотографий. \nВАЖНО! Отправляйте фото по отдельности!\n Нажмите кнопку снизу, когда загрузите нужные фото', reply_markup = keyboard)
    	bot.register_next_step_handler(msg, photo)

    elif c.data == 'normal':
    	keyboard=types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    	btn1 = types.KeyboardButton(text='ГОТОВО')
    	keyboard.add()
    	conn = sl.connect("database.db")
    	cur = conn.cursor()

    	cur.execute(f"SELECT id FROM goods WHERE user_id = '{c.message.chat.id}' order by id DESC limit 1")
    	res = cur.fetchone()[0]

    	cur.execute(f"UPDATE goods SET status = 'Удовлетворительное' WHERE id={res}")
    	conn.commit()
    	msg = bot.send_message(c.message.chat.id, 'Спасибо. Теперь можно загрузить до 10 фотографий. \nВАЖНО! Отправляйте фото по отдельности!\n Нажмите кнопку снизу, когда загрузите нужные фото', reply_markup = keyboard)
    	bot.register_next_step_handler(msg, photo)

    elif c.data == 'eur':
    	conn = sl.connect("database.db")
    	cur = conn.cursor()

    	cur.execute(f"SELECT id FROM goods WHERE user_id = '{c.message.chat.id}' order by id DESC limit 1")
    	res = cur.fetchone()[0]

    	cur.execute(f"UPDATE goods SET currency='€' WHERE id={res}")
    	conn.commit()
    	msg = bot.send_message(c.message.chat.id, 'Укажите стоимость без значка валюты', reply_markup = types.ReplyKeyboardRemove())
    	bot.register_next_step_handler(msg, price)
    
    elif c.data == 'rub':
    	conn = sl.connect("database.db")
    	cur = conn.cursor()

    	cur.execute(f"SELECT id FROM goods WHERE user_id = '{c.message.chat.id}' order by id DESC limit 1")
    	res = cur.fetchone()[0]

    	cur.execute(f"UPDATE goods SET currency='₽' WHERE id={res}")
    	conn.commit()
    	msg = bot.send_message(c.message.chat.id, 'Укажите стоимость без значка валюты', reply_markup = types.ReplyKeyboardRemove())
    	bot.register_next_step_handler(msg, price)

    elif c.data == 'done':
    	keyboard = types.InlineKeyboardMarkup()
    	btn1 = types.InlineKeyboardButton(text='₽', callback_data='rub')
    	btn2 = types.InlineKeyboardButton(text='€', callback_data='eur')
    	keyboard.add(btn1, btn2)
    	msg = bot.send_message(c.message.chat.id, 'Спасибо, уже почти все! Осталось указать валюту. Рубли или евро?\nВыберите вариант из предложенных', reply_markup = keyboard)

    elif c.data == 'more':
    	msg = bot.send_message(c.message.chat.id, 'Пришлите новое фото')
    	bot.register_next_step_handler(msg, photo)


def get_contact(message):
	a = types.ReplyKeyboardRemove()
	if message.contact is not None:
	 	msg = bot.send_message(message.chat.id, 'Спасибо, теперь введите адрес электронной почты', reply_markup=a)
	 	print(message.contact)
	 	conn = sl.connect("database.db")
	 	cur = conn.cursor()
	 	cur.execute(f"""UPDATE users SET phone='{message.contact.phone_number}' WHERE user_id={message.from_user.id}""")
	 	print(cur.fetchall())
	 	conn.commit()
	 	bot.register_next_step_handler(msg, get_email)
	else:
		keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
		button_phone = types.KeyboardButton(text="Отправить телефон", request_contact=True)
		keyboard.add(button_phone)
		msg = bot.send_message(message.chat.id, "Не похоже на номер телефона :/ \nВоспользуйтесь кнопкой снизу", reply_markup=keyboard)
		bot.register_next_step_handler(msg, get_contact)



def get_name(message):
	if " " not in message.text:
		msg = bot.send_message(message.chat.id, 'Неверный формат. Напишите имя и фамилию в формате: Иван Иванов')
		bot.register_next_step_handler(msg, get_name)
	elif message.text == '/start':
		bot.send_message(message.chat.id, 'Вы уже регистрируетесь!\nУкажите ваше имя и фамилию')

	else:
		fname, lname = message.text.split(' ')
		conn = sl.connect("database.db")
		cur = conn.cursor()
		cur.execute(f"""UPDATE users SET fname='{fname}', lname='{lname}' WHERE user_id={message.from_user.id}""")
		print(cur.fetchall())
		conn.commit()

		keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
		button_phone = types.KeyboardButton(text="Отправить телефон", request_contact=True)
		keyboard.add(button_phone)
		msg = bot.send_message(message.chat.id, "Теперь оставьте, пожалуйста, ваш номер телефона.", reply_markup=keyboard)
		bot.register_next_step_handler(msg, get_contact)

def get_email(message):
	if validate_email(message.text):
		keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
		btn1 = types.KeyboardButton(text='Разместить объявление')
		keyboard.add(btn1)
		conn = sl.connect("database.db")
		cur = conn.cursor()
		cur.execute(f"""SELECT fname FROM users WHERE user_id={message.from_user.id}""")
		fname = cur.fetchone()
		cur.execute(f"UPDATE users SET verify='YES' WHERE user_id={message.from_user.id}")
		conn.commit()
		cur.execute(f"UPDATE users SET email='{message.text}' WHERE user_id={message.from_user.id}")
		conn.commit()


		print("___________________________________________")
		gscope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
		gcredentials = 'db-api.json'
		gdocument = 'DataBase Taff'
		cur.execute(f"""SELECT phone, fname, lname, email, verify FROM users WHERE user_id={message.from_user.id}""")
		data = cur.fetchone()
		credentials = ServiceAccountCredentials.from_json_keyfile_name(gcredentials, gscope)
		gc = gspread.authorize(credentials)
		wks = gc.open(gdocument).sheet1
		print(data)
		wks.append_row(
	        [data[0], data[1], data[2], data[3], data[4], message.from_user.id])

		keyboard = types.InlineKeyboardMarkup()
		btn1 = types.InlineKeyboardButton(text="Разместить объявление", callback_data="post")
		keyboard.add(btn1)
		msg = bot.send_message(message.chat.id, f'{fname[0]}, спасибо за регистрацию!\nПоздравляем, ваш аккаунт подтвержден!\nДобро пожаловать в главное меню!', reply_markup = keyboard)

	elif message.text == '/start':
		msg = bot.send_message(message.chat.id, 'Вы уже регистрируетесь!\nУкажите ваш email')
		bot.register_next_step_handler(msg, get_email)

	else:
		msg = bot.send_message(message.chat.id, "Не похоже на email :/\nПопробуйте снова!")
		bot.register_next_step_handler(msg, get_email)


def verify(message):

	cur.execute(f"""SELECT fname FROM users WHERE user_id={message.from_user.id}""")
	fname = cur.fetchone()
	cur.execute(f"UPDATE users SET verify='YES' WHERE user_id={message.from_user.id}")
	conn.commit()

	keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	btn1 = types.KeyboardButton(text='Разместить объявление')
	btn2 =  types.KeyboardButton(text='Связь с поддержкой')
	keyboard.add(btn1, btn2)
	msg = bot.send_message(message.chat.id, f'{fname[0]}, спасибо за регистрацию!\nПоздравляем, ваш аккаунт подтвержден!\nДобро пожаловать в главное меню!', reply_markup = keyboard)


	bot.register_next_step_handler(msg, menu)

#menu function
'''
def menu(message):
	if message.text == 'Разместить объявление':
		keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
		btn1 = types.KeyboardButton(text='Одежда')
		btn2 = types.KeyboardButton(text='Сумки')
		btn3 = types.KeyboardButton(text='Обувь')
		btn4 = types.KeyboardButton(text='Косметика')
		btn5 = types.KeyboardButton(text='Аксессуары')
		keyboard.add(btn1, btn2, btn3, btn4, btn5)
		msg = bot.send_message(message.chat.id, 'Давайте узнаем, что за товар вы хотите разместить? Какая категория?', reply_markup = keyboard)
		bot.register_next_step_handler(msg, categories)
	
	elif message.text == '/start':
		keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
		keyboard = types.InlineKeyboardMarkup()
		btn1 = types.InlineKeyboardButton(text="Разместить объявление", callback_data="post")
		keyboard.add(btn1)
		msg = bot.send_message(message.chat.id, '\nДобро пожаловать в главное меню!', reply_markup = keyboard)
	
	elif message.text == 'Связь с поддержкой':
		keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
		btn1 = types.KeyboardButton(text='Разместить объявление')
		btn2 =  types.KeyboardButton(text='Связь с поддержкой')
		keyboard.add(btn1, btn2)
		msg = bot.send_message(message.chat.id, 'Связаться с менеджером: @tuffstuffxvintagetelega', reply_markup=keyboard)
		bot.register_next_step_handler(msg, menu)

	else:
		msg = bot.send_message(message.chat.id, 'Не удалось обработать запрос, попробуйте снова!')
		bot.register_next_step_handler(msg, menu)
'''
#post
def categories(message):
	conn = sl.connect("database.db")
	cur = conn.cursor()
	cur.execute(f"INSERT INTO goods (user_id) VALUES ('{message.from_user.id}')")
	cur.execute(f"SELECT id FROM goods WHERE user_id = '{message.from_user.id}' order by id DESC limit 1")
	res = cur.fetchone()[0]
	file1 = open("log.txt", "w")
	file1.write(f"{res}:{message.from_user.id}")
	
	keyboard = types.ReplyKeyboardRemove()

	if message.text == 'Одежда' or message.text == 'Аксессуары' or message.text == 'Сумки' or message.text == 'Обувь' or message.text == 'Косметика':
		cur.execute(f"UPDATE goods SET category = '{message.text}' WHERE id={res}")

		conn.commit()
		msg = bot.send_message(message.chat.id, 'Спасибо, в каком городе находится вещь?', reply_markup = keyboard)
		bot.register_next_step_handler(msg, get_city)

	elif message.text == '/start':
		keyboard = types.InlineKeyboardMarkup()
		btn1 = types.InlineKeyboardButton(text="Разместить объявление", callback_data="post")
		keyboard.add(btn1)
		msg = bot.send_message(message.chat.id, '\nДобро пожаловать в главное меню!', reply_markup=keyboard)
		bot.register_next_step_handler(msg, menu)

	else:
		msg = bot.send_message(message.chat.id, 'Не удалось получить категорию. Повторите снова, используя кнопки снизу')
		bot.register_next_step_handler(msg, categories)

def get_city(message):
	keyboard = types.ReplyKeyboardRemove()
	#database
	conn = sl.connect("database.db")
	cur = conn.cursor()
	file1 = open("log.txt", "r")
	res = file1.read().split(":")[0]
	

	cur.execute(f"UPDATE goods SET city = '{message.text}' WHERE id='{res}'")
	conn.commit()
	msg = bot.send_message(message.chat.id, 'Хорошо, укажите бренд вещи', reply_markup = keyboard)
	bot.register_next_step_handler(msg, brand)

def brand(message):
	keyboard = types.ReplyKeyboardRemove()
	#database
	conn = sl.connect("database.db")
	cur = conn.cursor()
	cur.execute(f"SELECT id FROM goods WHERE user_id = '{message.chat.id}' order by id DESC limit 1")
	res = cur.fetchone()[0]

	cur.execute(f"UPDATE goods SET brand = '{message.text}' WHERE id={res}")
	conn.commit()
	msg = bot.send_message(message.chat.id, 'Какой размер указан на бирке или подошве? (если размера нет, поставьте NA)', reply_markup = keyboard)
	bot.register_next_step_handler(msg, size)


def size(message):
	keyboard = types.InlineKeyboardMarkup(row_width=4)
	btn1 = types.InlineKeyboardButton(text='Новое с биркой', callback_data='new')
	btn2 = types.InlineKeyboardButton(text='Как новое', callback_data='also_new')
	btn3 = types.InlineKeyboardButton(text='Хорошее', callback_data='good')
	btn4 = types.InlineKeyboardButton(text='Удовлетворительное', callback_data='normal')
	keyboard.add(btn1, btn2, btn3, btn4)
	#database
	conn = sl.connect("database.db")
	cur = conn.cursor()
	cur.execute(f"SELECT id FROM goods WHERE user_id = '{message.chat.id}' order by id DESC limit 1")
	res = cur.fetchone()[0]

	cur.execute(f"UPDATE goods SET size = '{message.text}' WHERE id={res}")
	conn.commit()
	msg = bot.send_message(message.chat.id, 'Как вы оцениваете состояние вещи?', reply_markup = keyboard)


def status(message):
	keyboard=types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	btn1 = types.KeyboardButton(text='ГОТОВО')
	keyboard.add(btn1)
	conn = sl.connect("database.db")
	cur = conn.cursor()
	file1 = open("log.txt", "r")
	res = file1.read().split(":")[0]


	if message.text == 'Новое с биркой' or message.text == 'Как новое' or message.text == 'Хорошее' or message.text == 'Удовлетворительное':
		cur.execute(f"UPDATE goods SET status = '{message.text}' WHERE id={res}")
		conn.commit()
		msg = bot.send_message(message.chat.id, 'Спасибо. Теперь можно загрузить до 10 фотографий. \nВАЖНО! Отправляйте фото по отдельности!\n Нажмите кнопку снизу, когда загрузите нужные фото', reply_markup = keyboard)
		bot.register_next_step_handler(msg, photo)

	else:
		msg = bot.send_message(message.chat.id, 'Выберите состояние из данного списка')
		bot.register_next_step_handler(msg, status)

def currency(message):
	file1 = open("log.txt", "r")
	res = file1.read().split(":")[0]

	conn = sl.connect("database.db")
	cur = conn.cursor()
	cur.execute(f"UPDATE goods SET currency='{message.text}' WHERE id={res}")
	conn.commit()
	msg = bot.send_message(message.chat.id, 'Укажите стоимость без значка валюты', reply_markup = types.ReplyKeyboardRemove())
	bot.register_next_step_handler(msg, price)

def price(message):
	keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	btn1 = types.KeyboardButton(text='Опубликовать')
	keyboard.add(btn1)
	conn = sl.connect("database.db")
	cur = conn.cursor()

	cur.execute(f"SELECT id FROM goods WHERE user_id={message.from_user.id} order by id DESC limit 1")
	res = cur.fetchone()[0]

	cur.execute(f"SELECT * FROM goods WHERE id={res}")
	all_data = cur.fetchone()
	cur.execute(f"SELECT fname, lname, phone FROM users WHERE user_id='{message.from_user.id}'")
	contact_data = cur.fetchone()
	cur.execute(f"UPDATE goods SET price='{message.text}' WHERE id={res}")
	conn.commit()
	cur.execute(f"UPDATE goods SET moderation='' WHERE id={res}")
	print(res)
	conn.commit()
	photos_pathes = all_data[6]
	if photos_pathes is not None:
		path_list = photos_pathes.split(":")
		count = 0
		medias = []

		for el in path_list:
			count += 1
			photo = open(el, 'rb')
			medias.append(types.InputMedia(type='photo', media=photo))

		bot.send_media_group(message.chat.id, media=medias)

	msg = bot.send_message(message.chat.id, text=f'Предварительный просмотр:\nКатегория: {all_data[1]}\nБренд: {all_data[3]}\nРазмер: {all_data[4]}\nСостояние: {all_data[5]}\nЦена: {message.text}{all_data[7]}\nОпубликовать?\n', reply_markup = keyboard)
	bot.send_message(admin, 'Новая заявка ожидает модерации!\nЧтобы посмотреть, напишите /moderate')
	bot.register_next_step_handler(msg, moderation)


def moderation(message):
	file1 = open("log.txt", "w")
	bot.send_message(message.chat.id, 'Спасибо, объявление отправлено на модерацию и будет опубликовано после проверки.')
	time.sleep(0.2)
	keyboard = types.InlineKeyboardMarkup()
	btn1 = types.InlineKeyboardButton(text="Разместить объявление", callback_data="post")
	btn2 = types.InlineKeyboardButton(text="Связаться с поддержкой", callback_data="support")
	keyboard.add(btn1, btn2)
	msg =  bot.send_message(message.chat.id, 'Добро пожаловать в главное меню!', reply_markup = keyboard)


@bot.message_handler(commands=['moderate'])
def moderate(message):
	if message.chat.id == admin:
		file1 = open("log.txt", "r")
		res = file1.read().split(":")[0]
		print(res)
		conn = sl.connect("database.db")
		cur = conn.cursor()
		cur.execute(f"SELECT * FROM goods WHERE moderation='' order by id DESC limit 1")
		all_data = cur.fetchone()
		print(all_data)
		if all_data is not None:
			cur.execute(f"SELECT fname, lname, phone FROM users WHERE user_id='{all_data[10]}'")
			contact_data = cur.fetchone()
			print(all_data)
			if all_data[9] != 'YES':
				photos_pathes = all_data[6]
				if photos_pathes is not None:
					path_list = photos_pathes.split(":")
					count = 0
					medias = []

					for el in path_list:
						count += 1
						photo = open(el, 'rb')
						medias.append(types.InputMedia(type='photo', media=photo))

					bot.send_media_group(message.chat.id, media=medias)
						
					keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
					btn1 = types.KeyboardButton(text='Изменить состояние')
					btn2 = types.KeyboardButton(text='Изменить бренд')
					btn3 = types.KeyboardButton(text='Изменить размер')
					btn4 = types.KeyboardButton(text='Изменить цену')
					btn5 = types.KeyboardButton(text='Отклонить')
					btn6 = types.KeyboardButton(text='Опубликовать')
					keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6)

					msg = bot.send_message(message.chat.id, text=f'Новая заявка!\nДанные о клиенте:\nНомер телефона:{contact_data[2]}\nИмя:{contact_data[0]}\n--\nКатегория: {all_data[1]}\nБренд: {all_data[3]}\nРазмер: {all_data[4]}\nСостояние: {all_data[5]}\nЦена: {all_data[8]}{all_data[7]}\nОпубликовать?\n', reply_markup = keyboard)
			
					bot.register_next_step_handler(msg, editor)
			else:
				cur.execute(f"DELETE FROM goods WHERE id='{all_data[0]}'")
				conn.commit()

				cur.execute(f"SELECT COUNT(*) FROM `goods` WHERE moderation='' and price is not null and photo_path is not null and status is not null and currency is not null and category is not null")
				count = cur.fetchone()[0]
				bot.send_message(message.chat.id, f'Объявление оказалось пустым, осталось {count} объявлений. Чтобы перейти к следущему\nНапишите /moderate')

		else:
			bot.send_message(message.chat.id, 'Заявок не найдено!', reply_markup=types.ReplyKeyboardRemove())


def editor(message):
	if message.text == 'Изменить состояние':
		keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
		btn1 = types.KeyboardButton(text='Новое с биркой')
		btn2 = types.KeyboardButton(text='Как новое')
		btn3 = types.KeyboardButton(text='Хорошее')
		btn4 = types.KeyboardButton(text='Удовлетворительное')
		keyboard.add(btn1, btn2, btn3, btn4)
		msg = bot.send_message(message.chat.id, 'Выберите вариант из предложенных', reply_markup = keyboard)
		bot.register_next_step_handler(msg, edit_status)

	elif message.text == 'Изменить размер':
		msg = bot.send_message(message.chat.id, 'Введите новое значение', reply_markup=types.ReplyKeyboardRemove())
		bot.register_next_step_handler(msg, edit_size)

	elif message.text == 'Изменить бренд':
		msg = bot.send_message(message.chat.id, 'Введите новое значение', reply_markup=types.ReplyKeyboardRemove())
		bot.register_next_step_handler(msg, edit_brand)

	elif message.text == 'Изменить цену':
		msg = bot.send_message(message.chat.id, 'Введите новую цену', reply_markup=types.ReplyKeyboardRemove())
		bot.register_next_step_handler(msg, edit_price)

	elif message.text == 'Опубликовать':
		conn = sl.connect("database.db")
		cur = conn.cursor()
		cur.execute(f"SELECT user_id FROM goods order by id DESC limit 1")
		user_id = cur.fetchone()[0]
		cur.execute(f"SELECT id FROM goods WHERE moderation='' order by id DESC limit 1")
		res = cur.fetchone()[0]
		print(res)
		cur.execute(f"UPDATE goods SET moderation='YES' WHERE id='{res}' and moderation=''")
		conn.commit()

		cur.execute(f"SELECT COUNT(*) FROM `goods` WHERE moderation='' and price is not null and photo_path is not null and status is not null and currency is not null and category is not null")
		count = cur.fetchone()[0]

		cur.execute(f"SELECT * FROM goods WHERE id='{res}'")
		all_data = cur.fetchone()
		cur.execute(f"SELECT fname, lname, phone FROM users WHERE user_id='{message.from_user.id}'")
		contact_data = cur.fetchone()
		print(all_data)
		print(contact_data)
		photos_pathes = all_data[6]
		path_list = photos_pathes.split(":")
		count = 0
		medias = []

		for el in path_list:
			count += 1
			photo = open(el, 'rb')
			medias.append(types.InputMedia(type='photo', media=photo))

		bot.send_media_group(channel, media=medias)
		bot.send_message(channel, f"Категория: {all_data[1]}\nБренд: {all_data[3]}\nРазмер: {all_data[4]}\nСостояние: {all_data[5]}\nЦена: {all_data[8]}{all_data[7]}\n")
		bot.send_message(message.chat.id, 'Объявление успешно опубликовано!')
		bot.send_message(user_id, 'Ваше объявление опубликовано!')
		bot.send_message(message.chat.id, f'Осталось еще {count} нерасмотренных объявлений')

		keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
		btn1 = types.KeyboardButton(text='Изменить состояние')
		btn2 = types.KeyboardButton(text='Изменить бренд')
		btn3 = types.KeyboardButton(text='Изменить размер')
		btn4 = types.KeyboardButton(text='Изменить цену')
		btn5 = types.KeyboardButton(text='Отклонить')
		btn6 = types.KeyboardButton(text='Опубликовать')
		keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6)

		time.sleep(0.5)
		if all_data is not None:
			msg = bot.send_message(message.chat.id, text=f'Новая заявка!\nДанные о клиенте:\nНомер телефона:{contact_data[2]}\nИмя:{contact_data[0]}\n--\nКатегория: {all_data[1]}\nБренд: {all_data[3]}\nРазмер: {all_data[4]}\nСостояние: {all_data[5]}\nЦена: {all_data[8]}{all_data[7]}\nОпубликовать?\n', reply_markup = keyboard)
			bot.register_next_step_handler(msg, editor)	
		else:
			msg = bot.send_message(message.chat.id, 'При следущих заявках будет отправено уведомление')

	elif message.text == 'Отклонить':
		try:
			file1 = open("log.txt", "r")
			res = file1.read().split(":")[0]

			conn = sl.connect("database.db")
			cur = conn.cursor()
			cur.execute(f"SELECT user_id FROM goods order by id DESC limit 1")
			user_id = cur.fetchone()[0]
			cur.execute(f"SELECT id FROM goods WHERE moderation='' order by id DESC limit 1")
			res = cur.fetchone()[0]
			cur.execute(f"DELETE FROM goods WHERE id='{res}'")
			conn.commit()
			bot.send_message(message.chat.id, 'Объявление успешно отклонено!')
			bot.send_message(user_id, 'К сожалению, мы не можем опубликовать ваше объявление, так как оно не отвечает нашим требованиям.\nСвязаться с менеджером: @tuffstuffxvintagetelega')

			file1 = open("log.txt", "r")
			res = file1.read().split(":")[0]

			cur.execute(f"SELECT * FROM goods WHERE moderation='' order by id DESC limit 1")
			all_data = cur.fetchone()
			cur.execute(f"SELECT fname, lname, phone FROM users WHERE user_id='{message.from_user.id}'")
			contact_data = cur.fetchone()
			print(all_data)

			photos_pathes = all_data[6]
			path_list = photos_pathes.split(":")
			count = 0
			medias = []

			if all_data[9] == '' and all_data[0] is not None and all_data[1] is not None and all_data[2] is not None and all_data[3] is not None and all_data[4] is not None and all_data[5] and all_data[6] is not None and all_data[7] is not None and all_data[8] is not None and all_data[10] is not None:
				print('PASSED')
				
				if photos_pathes is not None:
					path_list = photos_pathes.split(":")
					count = 0
					medias = []

					for el in path_list:
						count += 1
						photo = open(el, 'rb')
						medias.append(types.InputMedia(type='photo', media=photo))

					bot.send_media_group(message.chat.id, media=medias)
						
					keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
					btn1 = types.KeyboardButton(text='Изменить состояние')
					btn2 = types.KeyboardButton(text='Изменить бренд')
					btn3 = types.KeyboardButton(text='Изменить размер')
					btn4 = types.KeyboardButton(text='Изменить цену')
					btn5 = types.KeyboardButton(text='Отклонить')
					btn6 = types.KeyboardButton(text='Опубликовать')
					keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6)

					bot.send_message(message.chat.id, f'Осталось еще {count} нерасмотренных объявлений')
					time.sleep(0.5)

					msg = bot.send_message(message.chat.id, text=f'Новая заявка!\nДанные о клиенте:\nНомер телефона:{contact_data[2]}\nИмя:{contact_data[0]}\n--\nКатегория: {all_data[1]}\nБренд: {all_data[3]}\nРазмер: {all_data[4]}\nСостояние: {all_data[5]}\nЦена: {all_data[8]}{all_data[7]}\nОпубликовать?\n', reply_markup = keyboard)
					bot.register_next_step_handler(msg, editor)
		except:
			pass

def edit_brand(message):
	keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	btn1 = types.KeyboardButton(text='Изменить состояние')
	btn2 = types.KeyboardButton(text='Изменить бренд')
	btn3 = types.KeyboardButton(text='Изменить размер')
	btn4 = types.KeyboardButton(text='Изменить цену')
	btn5 = types.KeyboardButton(text='Отклонить')
	btn6 = types.KeyboardButton(text='Опубликовать')
	keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6)

	conn = sl.connect("database.db")
	cur = conn.cursor()

	cur.execute(f"SELECT id FROM goods where moderation='' order by id DESC limit 1")
	res = cur.fetchone()[0]
	print(res)
	cur.execute(f"UPDATE goods SET brand ='{message.text}' WHERE id={res} and moderation=''")
	conn.commit()
	cur.execute(f"SELECT * FROM goods WHERE moderation='' order by id DESC limit 1")
	data = cur.fetchone()
	cur.execute(f"SELECT fname, lname, phone FROM users WHERE user_id='{message.from_user.id}'")
	contact= cur.fetchone()
	msg = bot.send_message(message.chat.id, text=f'Проверьте данные!\nДанные о клиенте:\nНомер телефона:{contact[2]}\nИмя:{contact[0]}\n--\nКатегория: {data[1]}\nБренд: {data[3]}\nРазмер: {data[4]}\nСостояние: {data[5]}\nЦена: {data[8]}{data[7]}\nОпубликовать?\n', reply_markup = keyboard)
	bot.register_next_step_handler(msg, editor)

def edit_size(message):
	keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	btn1 = types.KeyboardButton(text='Изменить состояние')
	btn2 = types.KeyboardButton(text='Изменить бренд')
	btn3 = types.KeyboardButton(text='Изменить размер')
	btn4 = types.KeyboardButton(text='Изменить цену')
	btn5 = types.KeyboardButton(text='Отклонить')
	btn6 = types.KeyboardButton(text='Опубликовать')
	keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6)

	conn = sl.connect("database.db")
	cur = conn.cursor()

	cur.execute(f"SELECT id FROM goods where moderation='' order by id DESC limit 1")
	res = cur.fetchone()[0]
	print(res)
	cur.execute(f"UPDATE goods SET size ='{message.text}' WHERE id={res} and moderation=''")
	conn.commit()
	cur.execute(f"SELECT * FROM goods WHERE moderation='' order by id DESC limit 1")
	data = cur.fetchone()
	cur.execute(f"SELECT fname, lname, phone FROM users WHERE user_id='{message.from_user.id}'")
	contact= cur.fetchone()
	msg = bot.send_message(message.chat.id, text=f'Проверьте данные!\nДанные о клиенте:\nНомер телефона:{contact[2]}\nИмя:{contact[0]}\n--\nКатегория: {data[1]}\nБренд: {data[3]}\nРазмер: {data[4]}\nСостояние: {data[5]}\nЦена: {data[8]}{data[7]}\nОпубликовать?\n', reply_markup = keyboard)
	bot.register_next_step_handler(msg, editor)


def edit_price(message):
	keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	btn1 = types.KeyboardButton(text='Изменить состояние')
	btn2 = types.KeyboardButton(text='Изменить бренд')
	btn3 = types.KeyboardButton(text='Изменить размер')
	btn4 = types.KeyboardButton(text='Изменить цену')
	btn5 = types.KeyboardButton(text='Отклонить')
	btn6 = types.KeyboardButton(text='Опубликовать')
	keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6)

	conn = sl.connect("database.db")
	cur = conn.cursor()

	cur.execute(f"SELECT id FROM goods where moderation='' order by id DESC limit 1")
	res = cur.fetchone()[0]
	print(res)
	cur.execute(f"UPDATE goods SET price ='{message.text}' WHERE id={res} and moderation=''")
	conn.commit()
	cur.execute(f"SELECT * FROM goods WHERE moderation='' order by id DESC limit 1")
	data = cur.fetchone()
	cur.execute(f"SELECT fname, lname, phone FROM users WHERE user_id='{message.from_user.id}'")
	contact= cur.fetchone()
	msg = bot.send_message(message.chat.id, text=f'Проверьте данные!\nДанные о клиенте:\nНомер телефона:{contact[2]}\nИмя:{contact[0]}\n--\nКатегория: {data[1]}\nБренд: {data[3]}\nРазмер: {data[4]}\nСостояние: {data[5]}\nЦена: {data[8]}{data[7]}\nОпубликовать?\n', reply_markup = keyboard)
	bot.register_next_step_handler(msg, editor)


def edit_status(message):
	keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	btn1 = types.KeyboardButton(text='Изменить состояние')
	btn2 = types.KeyboardButton(text='Изменить бренд')
	btn3 = types.KeyboardButton(text='Изменить размер')
	btn4 = types.KeyboardButton(text='Изменить цену')
	btn5 = types.KeyboardButton(text='Отклонить')
	btn6 = types.KeyboardButton(text='Опубликовать')
	keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6)

	file1 = open("log.txt", "r")
	res = file1.read().split(":")[0]
	conn = sl.connect("database.db")
	cur = conn.cursor()

	cur.execute(f"SELECT id FROM goods where moderation='' order by id DESC limit 1")
	res = cur.fetchone()[0]
	print(res)
	cur.execute(f"UPDATE goods SET status ='{message.text}' WHERE id={res} and moderation=''")
	conn.commit()
	cur.execute(f"SELECT * FROM goods WHERE moderation='' order by id DESC limit 1")
	data = cur.fetchone()
	cur.execute(f"SELECT fname, lname, phone FROM users WHERE user_id='{message.from_user.id}'")
	contact= cur.fetchone()
	msg = bot.send_message(message.chat.id, text=f'Проверьте данные!\nДанные о клиенте:\nНомер телефона:{contact[2]}\nИмя:{contact[0]}\n--\nКатегория: {data[1]}\nБренд: {data[3]}\nРазмер: {data[4]}\nСостояние: {data[5]}\nЦена: {data[8]}{data[7]}\nОпубликовать?\n', reply_markup = keyboard)
	bot.register_next_step_handler(msg, editor)


def photo(message):
	conn = sl.connect("database.db")
	cur = conn.cursor()

	if message.text == 'ГОТОВО':

		keyboard = types.InlineKeyboardMarkup()
		btn1 = types.InlineKeyboardButton(text='₽', callback_data='rub')
		btn2 = types.InlineKeyboardButton(text='€', callback_data='eur')
		keyboard.add(btn1, btn2)
		msg = bot.send_message(message.chat.id, 'Спасибо, уже почти все! Осталось указать валюту. Рубли или евро?\nВыберите вариант из предложенных', reply_markup = keyboard)
	
	elif message.photo is not None:
		keyboard=types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
		btn1 = types.KeyboardButton(text='ГОТОВО')
		keyboard.add(btn1)
		file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
		downloaded_file = bot.download_file(file_info.file_path)
		src = '/Users/anna/desktop/bot_new_release/img/' + message.photo[1].file_id
		with open(src, 'wb') as new_file:
			new_file.write(downloaded_file)

		cur.execute(f"SELECT id FROM goods WHERE user_id = '{message.chat.id}' order by id DESC limit 1")
		res = cur.fetchone()[0]

		conn = sl.connect("database.db")
		cur = conn.cursor()
		cur.execute(f"SELECT photo_path FROM goods WHERE id={res}")
		path = cur.fetchone()
		print(path[0])
		if path[0] == None:
			path = src
		else:
			path = str(src) + ':' + str(path[0])
		print(path)
		cur.execute(f"UPDATE goods SET photo_path = '{path}' WHERE id={res}")
		conn.commit()

		keyboard = types.InlineKeyboardMarkup(row_width=2)
		btn1 =  types.InlineKeyboardButton(text='Готово', callback_data='done')
		btn2 = types.InlineKeyboardButton(text='Еще фото', callback_data='more')
		keyboard.add(btn1, btn2)
		msg = bot.send_message(message.chat.id, 'Фото успешно загружено!',  reply_markup = keyboard)


bot.polling(none_stop=True, timeout=100)