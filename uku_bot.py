import telebot
from telebot import apihelper
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import xml.etree.ElementTree as ET

token = ''
bot = telebot.TeleBot(token)

class Input:
    def __init__(self):
        self.input_1 = None
        self.input_2 = None

user = Input()

@bot.message_handler(commands=['start'])

def send_message(message):
    cid = message.chat.id
    try:
        msg = bot.send_message(cid, "Enter the root note of the chord. Can be set to 'A', 'Bb', 'B' , 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab':")
        bot.register_next_step_handler(msg, first_step)
    except apihelper.ApiException as e:
        print(e)

def first_step(message):
    if message.text == "/start":
        return send_message(message)
    list_1 = ["A", "Bb", "B" , "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab"]
    cid = message.chat.id
    input_1 = message.text
    if not input_1 in list_1:
        try:
            msg = bot.send_message(cid, "Enter a valid note:")
            bot.register_next_step_handler(msg, first_step)
        except apihelper.ApiException as e:
            print(e)
        return
    user.input_1 = input_1
    try:
        msg = bot.send_message(cid, "Enter a type of chord. Can be set to 'major', 'm', 'aug', 'dim', '7', 'm7', 'maj7', 'm7b5', 'sus2', 'sus4', '7sus4', '9', '11', '13', '6', 'm6', 'add9', 'm9', '5', 'dim7', 'm13', '7sus2', 'mMaj7', 'm11', 'maj9':")
        bot.register_next_step_handler(msg, second_step)
    except apihelper.ApiException as e:
        print(e)


def second_step(message):
    if message.text == "/start":
        return send_message(message)
    list_2 = ["major", "m", "aug", "dim", "7", "m7", "maj7", "m7b5", "sus2", "sus4", "7sus4", "9", "11", "13", "6", "m6", "add9", "m9", "5", "dim7", "m13", "7sus2", "mMaj7", "m11", "maj9"]
    cid = message.chat.id
    input_2 = message.text
    if not input_2 in list_2:
        try:
            msg = bot.send_message(cid, "Enter a valid type:")
            bot.register_next_step_handler(msg, second_step)
        except apihelper.ApiException as e:
            print(e)
        return
    user.input_2 = input_2
    req = Request("http://www.ukulele-chords.com/get?ak=YOUR_API_KEY&r="+str(user.input_1)+"&typ="+str(user.input_2), headers={'User-Agent': 'Mozilla/5.0'})
    try:
        data = urlopen(req).read()
        root = ET.fromstring(data)
        chord = root[0][2].text
        bot.send_photo(message.chat.id, photo=chord)
        send_message(message)
    except HTTPError as err:
        if err.code == 404:
            bot.send_message(message.chat.id, "Data not found")


if __name__ == "__main__":
    bot.polling(none_stop=True)




