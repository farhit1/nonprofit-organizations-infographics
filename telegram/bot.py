import telebot
from telebot import types

from telegram.api_key import API_KEY

from infographics.companies import *
from infographics.regions import *
from infographics.constants import *

from keynote.draw import *


bot = telebot.TeleBot(API_KEY)
userStorage = dict()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user = message.from_user.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row(types.KeyboardButton('топ компаний'))
    markup.row(types.KeyboardButton('топ регионов'))
    userStorage[user] = dict()
    userStorage[user]['handler'] = splitTop
    bot.send_message(user, "Генерация инфографики распределения госсредств на НКО", reply_markup=markup)


@bot.message_handler(func=lambda x : True)
def handle_everything(message):
    user = message.from_user.id
    userStorage[user]['handler'](message)


def splitTop(message):
    user = message.from_user.id
    if message.text == 'топ компаний':
        userStorage[user]['type'] = 'companies'
        companiesTop(message)
    elif message.text == 'топ регионов':
        userStorage[user]['type'] = 'regions'
        regionsTop(message)


def companiesTop(message):
    user = message.from_user.id

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row(types.KeyboardButton('1'), types.KeyboardButton('2'),
               types.KeyboardButton('3'), types.KeyboardButton('4'),
               types.KeyboardButton('5'))
    userStorage[user]['handler'] = validateK
    bot.send_message(user, "Сколько компаний вам нужно в инфографике?", reply_markup=markup)


def validateK(message):
    user = message.from_user.id
    text = message.text

    if not text.isdigit() or not(int(text) in range(1, 6)):
        bot.send_message(user, "Введите число от 1 до 5")
        return
    userStorage[user]['handler'] = validateRegion
    userStorage[user]['k'] = int(text)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row(types.KeyboardButton('0'))
    bot.send_message(user, "Введите из какого региона должны быть компании или нажмите 0 для общероссийского рейтинга",
                     reply_markup=markup)


def validateRegion(message):
    user = message.from_user.id
    text = message.text

    if text.isdigit():
        text = int(text)
        if text not in range(MAX_REGIONS) or not regionName(text):
            bot.send_message(user, "Неправильный регион")
            return
        userStorage[user]['region'] = text
    else:
        regions = json.load(open('data/regions.json'))
        match = None
        for i in range(len(regions)):
            if regions[i].lower().find(text.lower()) != -1:
                match = i
                break
        if not match:
            bot.send_message(user, "Hеправильный регион")
            return
        userStorage[user]['region'] = match

    addYearButtons(message, 'start')


def addYearButtons(message, type):
    user = message.from_user.id

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row(types.KeyboardButton('2011'), types.KeyboardButton('2012'))
    markup.row(types.KeyboardButton('2013'), types.KeyboardButton('2014'))
    markup.row(types.KeyboardButton('2015'), types.KeyboardButton('2016'))

    userStorage[user]['handler'] = handleEndYear if type == 'start' else getGroup
    bot.send_message(user, "Выберите год %s временного промежутка" %
                     ('начала' if type == 'start' else 'конца'),
                     reply_markup=markup)


def handleEndYear(message):
    user = message.from_user.id
    userStorage[user]['start'] = message.text
    addYearButtons(message, 'end')


def getGroup(message):
    user = message.from_user.id

    if int(userStorage[user]['start']) > int(message.text):
        bot.send_message(user, 'Год окончания должен быть больше года начала')
        return
    userStorage[user]['end'] = message.text

    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton('гранты'))
    markup.row(types.KeyboardButton('контракты'))
    markup.row(types.KeyboardButton('субсидии'))
    markup.row(types.KeyboardButton('окончание выбора'))

    for cat in CATEGORIES:
        userStorage[user][cat] = False

    userStorage[user]['handler'] = handleGroup
    bot.send_message(user, "Выберите нужные типы договоров, после нажмите окончание выбора",
                     reply_markup=markup)


def handleGroup(message):
    user = message.from_user.id
    text = message.text

    if text == 'гранты':
        userStorage[user]['grants'] = True
        return
    elif text == 'контракты':
        userStorage[user]['contracts'] = True
        return
    elif text == 'субсидии':
        userStorage[user]['subsidies'] = True
        return
    elif text == 'окончание выбора':
        if not userStorage[user]['grants'] and not userStorage[user]['contracts'] and not\
               userStorage[user]['subsidies']:
            bot.send_message(user, "Выберите хотя бы один тип договора")
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row(types.KeyboardButton('0'))
            userStorage[user]['handler'] = handleCategory
            with open('images/set.png', 'rb') as photo:
                bot.send_photo(user, photo)
            bot.send_message(user, "Введите номер категории организации или выберите 0 для отображения НКО всех категорий", reply_markup=markup)


def handleCategory(message):
    user = message.from_user.id
    text = message.text

    if not text.isdigit() or not int(text) in range(0, 41):
        bot.send_message(user, 'Неправильная категория')
        return
    userStorage[user]['category'] = int(text)
    drawPic(message)


def drawPic(message):
    user = message.from_user.id

    chosenCategories = []
    for cat in CATEGORIES:
        if userStorage[user][cat]:
            chosenCategories.append(cat)

    if userStorage[user]['type'] == 'companies':
        draw(getFirstInfographics(userStorage[user]['category'],
                                  userStorage[user]['region'],
                                  int(userStorage[user]['start']),
                                  int(userStorage[user]['end']),
                                  chosenCategories,
                                  userStorage[user]['k']), 'keynote/templates/empty.key')
    else:
        draw(getThirdInfographics(userStorage[user]['category'],
                                  int(userStorage[user]['start']),
                                  int(userStorage[user]['end']),
                                  chosenCategories), 'keynote/templates/empty3.key')

    with open('slides/slides.001.jpeg', 'rb') as photo:
        bot.send_photo(user, photo)

    userStorage[user] = dict()
    send_welcome(message)


def regionsTop(message):
    user = message.from_user.id
    userStorage[user]['type'] = 'regions'
    addYearButtons(message, 'start')
