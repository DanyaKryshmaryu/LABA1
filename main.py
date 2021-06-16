from unittest.mock import call
import sqlite3
import telebot
import requests
import json
from telebot import types
bot = telebot.TeleBot('1731471550:AAFBXeBnA4xkFmvSfXu8nUPdsLHY6UxP90s')
conn = sqlite3.connect('db.db', check_same_thread=False)
cursor = conn.cursor()
def db_table_val(id_user: int, username: str, usersurname: str, nikname: str):
    conn.row_factory = sqlite3.Row
    user = cursor.execute( f"Select * from user where id_user={id_user}")
    rows = user.fetchall()
    if len(rows) == 1:
        return ('Вы уже зарегестрированы!')
    else:
        cursor.execute('INSERT INTO user (id_user,username, usersurname, nikname) VALUES (?,?, ?, ?)',
                     (id_user, username, usersurname, nikname))
        conn.commit()
        return ('Вы успешно зарегестрированы!')

def db_table_note(id_user: int, body_note: str, date: str):
    cursor.execute('INSERT INTO notes (id_user,body_note, date) VALUES (?, ?, ?)',
                   (id_user,body_note , date ))
    conn.commit()
def send(id,text):
    bot.send_message(id,text)
@bot.message_handler(commands=['start'])
def start_message(message, keyboard=None):
    bot.send_message(message.chat.id, 'Привет, я бот заметок =)')
    id_user = message.from_user.id
    username = message.from_user.first_name
    usersurname = message.from_user.last_name
    nikname = message.from_user.username
    text=db_table_val(id_user=id_user, username=username, usersurname=usersurname, nikname=nikname)
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['notes'])
def notes_message(message, keyboard=None):
    bot.send_message(message.chat.id, ' О чем тебе напомнить?)')
    id_user = message.from_user.id
    body_note = message.text
    date = message.date

    note = db_table_note(id_user=id_user, body_note=body_note,  date= date)





@bot.message_handler(content_types=['text'])
def start_msg(message):
    chat_id = message.chat.id
    msg = message.text
    if msg=='Привет':
        send(chat_id,msg)
    else:
        send(chat_id, 'Я тебя не понял!')
if __name__ == "__main__":
    bot.polling(none_stop=True)
else:
    pass


