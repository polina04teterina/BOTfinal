

import telebot  # pyTelegramBotAPI 4.3.1
from telebot import types
import BotGames  # бот-игры, файл botGames.py
import menuBot
from menuBot import Menu  # в этом модуле есть код, создающий экземпляры классов описывающих моё меню
import DZ  # домашнее задание от первого урока
import fun  # развлечения
import speech  # работа с речью


bot = telebot.TeleBot("5246247569:AAG6njKqX8QDcjlkmDUsXqiTgj7v4I0530k")  # Создаем экземпляр бота

#gjkldfjgldfkj
# -----------------------------------------------------------------------
# Функция, обрабатывающая команды
@bot.message_handler(commands="start")
def command(message):
    chat_id = message.chat.id
    bot.send_sticker(chat_id, "5246247569:AAG6njKqX8QDcjlkmDUsXqiTgj7v4I0530k")
    txt_message = f"Привет, {message.from_user.first_name}! Я тестовый бот для курса программирования на языке Python"
    bot.send_message(chat_id, text=txt_message, reply_markup=Menu.getMenu(chat_id, "Главное меню").markup)



# -----------------------------------------------------------------------
# Получение стикеров от юзера
@bot.message_handler(content_types=['sticker'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    sticker = message.sticker
    bot.send_message(message.chat.id, sticker)

    # глубокая инспекция объекта
    # import inspect,pprint
    # i = inspect.getmembers(sticker)
    # pprint.pprint(i)


# -----------------------------------------------------------------------
# Получение аудио от юзера
@bot.message_handler(content_types=['audio'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    audio = message.audio
    bot.send_message(chat_id, audio)


# -----------------------------------------------------------------------
# Получение голосовухи от юзера
@bot.message_handler(content_types=['voice'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    voice = message.voice
    # bot.send_message(message.chat.id, voice)

    import speech
    fileInfo = bot.get_file(voice.file_id)
    audioData = bot.download_file(fileInfo.file_path)
    bot.send_message(chat_id, speech.getTextFromVoice(audioData))

# -----------------------------------------------------------------------
# Получение фото от юзера
@bot.message_handler(content_types=['photo'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    photo = message.photo
    bot.send_message(message.chat.id, photo)


# -----------------------------------------------------------------------
# Получение видео от юзера
@bot.message_handler(content_types=['video'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    video = message.video
    bot.send_message(message.chat.id, video)


# -----------------------------------------------------------------------
# Получение документов от юзера
@bot.message_handler(content_types=['document'])
def get_messages(message):
    chat_id = message.chat.id
    mime_type = message.document.mime_type
    bot.send_message(chat_id, "Это " + message.content_type + " (" + mime_type + ")")

    document = message.document
    bot.send_message(message.chat.id, document)
    if message.document.mime_type == "video/mp4":
        bot.send_message(message.chat.id, "This is a GIF!")


# -----------------------------------------------------------------------
# Получение координат от юзера
@bot.message_handler(content_types=['location'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    location = message.location
    bot.send_message(message.chat.id, location)




# -----------------------------------------------------------------------
# Получение контактов от юзера
@bot.message_handler(content_types=['contact'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    contact = message.contact
    bot.send_message(message.chat.id, contact)


# -----------------------------------------------------------------------
# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    ms_text = message.text

    cur_user = menuBot.Users.getUser(chat_id)
    if cur_user is None:
        cur_user = menuBot.Users(chat_id, message.json["from"])

    # проверка = мы нажали кнопку подменю, или кнопку действия
    subMenu = menuBot.goto_menu(bot, chat_id, ms_text)  # попытаемся использовать текст как команду меню, и войти в него
    if subMenu is not None:
        # Проверим, нет ли обработчика для самого меню. Если есть - выполним нужные команды
        if subMenu.name == "Игра в 21":
            game21 = BotGames.newGame(chat_id, BotGames.Game21(jokers_enabled=True))  # создаём новый экземпляр игры
            text_game = game21.get_cards(2)  # просим 2 карты в начале игры
            bot.send_media_group(chat_id, media=game21.mediaCards)  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

        elif subMenu.name == "Игра КНБ":
            gameRPS = BotGames.newGame(chat_id, BotGames.GameRPS())  # создаём новый экземпляр игры и регистрируем его
            bot.send_photo(chat_id, photo=gameRPS.url_picRules, caption=gameRPS.text_rules, parse_mode='HTML')

        return  # мы вошли в подменю, и дальнейшая обработка не требуется

    # проверим, является ли текст текущий команды кнопкой действия
    cur_menu = Menu.getCurMenu(chat_id)
    if cur_menu is not None and ms_text in cur_menu.buttons:  # проверим, что команда относится к текущему меню
        module = cur_menu.module

        if module != "":  # проверим, есть ли обработчик для этого пункта меню в другом модуле, если да - вызовем его (принцип инкапсуляции)
            exec(module + ".get_text_messages(bot, cur_user, message)")

        if ms_text == "Помощь":
            send_help(bot, chat_id)

    else:  # ======================================= случайный текст
        bot.send_message(chat_id, text="Мне жаль, я не понимаю вашу команду: " + ms_text)
        menuBot.goto_menu(bot, chat_id, "Главное меню")


# -----------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # если требуется передать один или несколько параметров в обработчик кнопки,
    # используйте методы Menu.getExtPar() и Menu.setExtPar()
    # call.data это callback_data, которую мы указали при объявлении InLine-кнопки
    # После обработки каждого запроса вызовете метод answer_callback_query(), чтобы Telegram понял, что запрос обработан
    chat_id = call.message.chat.id
    message_id = call.message.id
    cur_user = menuBot.Users.getUser(chat_id)
    if cur_user is None:
        cur_user = menuBot.Users(chat_id, call.message.json["from"])

    tmp = call.data.split("|")
    menu = tmp[0] if len(tmp) > 0 else ""
    cmd = tmp[1] if len(tmp) > 1 else ""
    par = tmp[2] if len(tmp) > 2 else ""

    if menu == "GameRPSm":
       BotGames.callback_worker(bot, cur_user, cmd, par, call)  # обработчик кнопок игры находится в модули игры


# -----------------------------------------------------------------------
def send_help(bot, chat_id):
    bot.send_message(chat_id, "Автор: Полина ")
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Напишите автору", url="https://t.me/@pixie_po")
    markup.add(btn1)
    img = open('Швец Андрей.png', 'rb')
    bot.send_photo(chat_id, img, reply_markup=markup)

    bot.send_message(chat_id, "Активные пользователи чат-бота:")
    for el in menuBot.Users.activeUsers:
        bot.send_message(chat_id, menuBot.Users.activeUsers[el].getUserHTML(), parse_mode='HTML')



# ---------------------------------------------------------------------


bot.polling(none_stop=True, interval=0)  # Запускаем бота