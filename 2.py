# Телеграм-бот v.004 - бот создаёт меню, присылает собачку, и анекдот
import json
from gettext import find
from io import BytesIO

import telebot  # pyTelegramBotAPI 4.3.1
from telebot import types
import requests
import bs4
import BotGames
from menuBot import Menu
import DZ

bot = telebot.TeleBot('5246247569:AAG6njKqX8QDcjlkmDUsXqiTgj7v4I0530k')  # Создаем экземпляр бота
game21 = None


# Функция, обрабатывающая команду /start
@bot.message_handler(commands="start")
def command(massage, res=False):
    txt_massage = f"Привет, {massage.from_user.first_name}! Я тестовый бот для курса программирования на языке Pyton"
    bot.send_message(massage.chat.id, text=txt_massage, reply_markup=Menu.getMenu("Главное меню").markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global game21
    chat_id = message.chat.id
    ms_text = message.text
    result = goto_menu(chat_id, ms_text)
    if result == True:
        return
    if Menu.cur_menu != None and ms_text in Menu.cur_menu.buttons:
        if ms_text == "Помощь":
            send_help(chat_id)
        elif ms_text == "Прислать собаку":
            bot.send_photo(chat_id, photo=get_dogURL(), caption="Вот тебе собачка!")
        elif ms_text == "Прислать анекдот":
            bot.send_message(chat_id, text=get_anekdot())
        elif ms_text == "Прислать фильм":
            send_film(chat_id)
        elif ms_text == "Угадай кто?":
            get_ManOrNot(chat_id)
        elif ms_text == "Карту!":
            if game21 == None:
                goto_menu(chat_id, "Выход")
                return

            text_game = game21.get_cards(1)
            bot.send_media_group(chat_id, media=getMediaCards(game21))

            bot.send_message(chat_id, text=text_game)

            if game21.status != None:
                goto_menu(chat_id, "Выход")
                return
        elif ms_text == "Стоп!":
            game21 = None
            goto_menu(chat_id, "Выход")
            return
        elif ms_text == "Задание-1":
            DZ.dz1(bot, chat_id)
        elif ms_text == "Задание-2":
            DZ.dz2(bot, chat_id)
        elif ms_text == "Задание-3":
            DZ.dz3(bot, chat_id)
        elif ms_text == "Задание-4":
            DZ.dz4(bot, chat_id)
        elif ms_text == "Задание-5":
            DZ.dz5(bot, chat_id)
        elif ms_text == "Задание-6":
            DZ.dz6(bot, chat_id)
        elif ms_text == "Курс доллара":
            data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
            rate_message = "1 Доллар США равен "+str(data['Valute']['USD']['Value'])+" руб."
            bot.send_message(chat_id, text=rate_message)
    else:
        bot.send_message(chat_id, text="Мне жаль, я не понимаю вашу команду: " + ms_text)
        goto_menu(chat_id, "Главное меню")

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    pass

def goto_menu(chat_id, name_menu):
    if name_menu == "Выход" and Menu.cur_menu !=None and Menu.cur_menu.parent != None:
        target_menu = Menu.getMenu(Menu.cur_menu.parent.name)
    else:
        target_menu = Menu.getMenu(name_menu)

    if target_menu != None:
        bot.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)
        if target_menu.name == "Игра в 21":
            global game21
            game21 = BotGames.Game21()
            text_game = game21.get_cards(2)
            bot.send_media_group(chat_id, media=getMediaCards(game21))
            bot.send_message(chat_id, text=text_game)
        return True
    else:
        return False

def getMediaCards(game21):
    medias = []
    for url in game21.arr_cards_URL:
        medias.append(types.InputMediaPhoto(url))
    return medias

def send_help(chat_id):
    global bot
    bot.send_message(chat_id, "Автор: Швец Андрей")
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Напишите автору", url="https://t.me/user59387")
    markup.ad

def send_help(chat_id):
    global bot
    bot.send_message(chat_id, "Автор: Швец Андрей")
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Напишите автору", url="https://t.me/user59387")
    markup.add(btn1)
    img = open('Швец Андрей.png', 'rb')
    bot.send_photo(chat_id, img, reply_markup=markup)

def send_film(chat_id):
    film = get_randomFilm()
    info_str = f"<b>{film['Наименование']}</b>\n" \
               f"Год: {film['Год']}\n" \
               f"Страна: {film['Страна']}\n" \
               f"Жанр: {film['Жанр']}\n" \
               f"Продолжительность: {film['Продолжительность']}"
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Трейлер", url=film["Трейлер_url"])
    btn2 = types.InlineKeyboardButton(text="СМОТРЕТЬ онлайн", url=film["фильм_url"])
    markup.add(btn1, btn2)
    bot.send_photo(chat_id, photo=film['Обложка_url'], caption=info_str, parse_mode='HTML', reply_markup=markup)

def get_anekdot():
    array_anekdots = []
    req_anek = requests.get('http://anekdotme.ru/random')
    if req_anek.status_code == 200:
        soup = bs4.BeautifulSoup(req_anek.text, "html5lib")
        result_find = soup.select('.anekdot_text')
        for result in result_find:
            array_anekdots.append(result.getText().strip())
    if len(array_anekdots) > 0:
        return array_anekdots[0]
    else:
        return ""

def get_dogURL():
    url = ""
    req = requests.get('https://random.dog/woof.json')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['url']
    return url

def get_ManOrNot(chat_id):
    global bot

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Проверить",
                                      url="https://vc.ru/dev/58543-thispersondoesnotexist-sayt-generator-realistichnyh-lic")
    markup.add(btn1)

    req = requests.get("https://thispersondoesnotexist.com/image", allow_redirects=True)
    if req.status_code == 200:
        img = BytesIO(req.content)
        bot.send_photo(chat_id, photo=img, reply_markup=markup, caption="Этот человек реален?")

def get_randomFilm():
    url = 'https://randomfilm.ru/'
    infoFilm = {}
    req_film = requests.get(url)
    soup = bs4.BeautifulSoup(req_film.text, "html5lib")
    result_find = soup.find('div', align="center", style="width: 100%")
    infoFilm["Наименование"] = result_find.find("h2").getText()
    names = infoFilm["Наименование"].split(" / ")
    infoFilm["Наименование_rus"] = names[0].strip()
    if len(names) > 1:
        infoFilm["Наименование_eng"] = names[1].strip()

    images = []
    for img in result_find.findAll('img'):
        images.append(url + img.get('src'))
    infoFilm["Обложка_url"] = images[0]
    detalis = result_find.findAll('td')
    infoFilm["Год"] = detalis[0].contents[1].strip()
    infoFilm["Страна"] = detalis[1].contents[1].strip()
    infoFilm["Жанр"] = detalis[2].contents[1].strip()
    infoFilm["Продолжительность"] = detalis[3].contents[1].strip()
    infoFilm["Режиссер"] = detalis[4].contents[1].strip()
    infoFilm["Актеры"] = detalis[5].contents[1].strip()
    infoFilm["Трейлер_url"] = url + detalis[6].contents[0]["href"]
    infoFilm["фильм_url"] = url + detalis[7].contents[0]["href"]

    return infoFilm

bot.polling(none_stop=True, interval=0)

print()
