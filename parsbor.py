
from decouple import config
import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types

page = 'https://kaktus.media/?lable=8&date=2023-05-30&order=time'
url = 'https://kaktus.media/?lable=8&date=2023-05-30&order=time'
count = 0
list_all = []
response = requests.get(url)
htmltext = response.text
soup = BeautifulSoup(htmltext, 'lxml')

values = soup.find_all('div', class_="ArticleItem--data ArticleItem--data--withImage")
ss = soup.find_all('a', 'ArticleItem--name')

for i in range(len(values[:20])):
    news = values[i].find('a', class_="ArticleItem--name").text.replace('\n','')
    new = BeautifulSoup(requests.get(ss[i].get('href')).text, 'lxml')
    p = new.find_all('p')
    img = values[i].find('img').get('src') if values[i].find('img') is not None else 'None'

    list_all.append([news, img, ' '.join([i.text.strip() if i is not None else 'None' for i in p])])

for i in range(len(list_all)):
    list_all[i].insert(0, str(i + 1))

print(list_all)



token = config('TOKEN')
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    knopka1 = types.KeyboardButton('Все новости')
    knopka2 = types.KeyboardButton('Quit')
    markup.add(knopka1, knopka2)
    bot.send_message(message.from_user.id, "Выберите узнать новости или выйти", reply_markup=markup)
    
    for i in range(len(list_all)):
        bot.send_message(message.from_user.id, list_all[i][0] +') '+  list_all[i][1] )

@bot.message_handler(func=lambda message: message.text in ['Все новости', 'Quit'])
def handle_currency(message):
    if message.text == 'Все новости':
        bot.send_message(message.from_user.id, 'Вы выбрали раздел "Все новости"')
        keyboard = types.ReplyKeyboardMarkup(row_width=5)
        knopki = [types.KeyboardButton(str(i + 1)) for i in range(20)]
        keyboard.add(*knopki)
        bot.send_message(message.from_user.id, 'Выберите номер новости:', reply_markup=keyboard)
    elif message.text == 'Quit':
        bot.send_message(message.from_user.id, 'До свидания')

    

@bot.message_handler(func=lambda message: message.text.isdigit())
def push(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    knopka1DIS = types.KeyboardButton('Description')
    knopka2PH = types.KeyboardButton('Photo')
    markup.add(knopka1DIS, knopka2PH)
    global nomer
    nomer = int(message.text)
    if 1 <= nomer <= len(list_all):
        tek = list_all[nomer- 1][1]
        bot.send_message(message.from_user.id, f'вы выбрали новость {nomer}:\n{tek}', reply_markup = markup)
        bot.send_message(message.from_user.id, 'some title news you can see Description of this new sand Photo',reply_markup = markup)
    else:
        bot.send_message(message.from_user.id, 'Что-то пошло не так')


@bot.message_handler(func=lambda message: message.text in ['Description', 'Photo'])
def func_(message):
    if message.text == 'Photo':
        bot.send_message(message.from_user.id,list_all[nomer- 1][2], reply_markup=types.ReplyKeyboardRemove())

    if message.text == 'Description':
        bot.send_message(message.from_user.id,list_all[nomer- 1][3], reply_markup=types.ReplyKeyboardRemove())
    

bot.polling()









