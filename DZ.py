# ======================================= модуль ДЗ
# ======================================= модуль ДЗ

name = 'Полина'
age = 20
# -----------------------------------------------------------------------
def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Задание-1":
        dz1(bot, chat_id)

    elif ms_text == "Задание-2":
        dz2(bot, chat_id)

    elif ms_text == "Задание-3":
        dz3(bot, chat_id)

    elif ms_text == "Задание-4":
        dz4(bot, chat_id)

    elif ms_text == "Задание-5":
        dz5(bot, chat_id)

    elif ms_text == "Задание-6":
        dz6(bot, chat_id)


# -----------------------------------------------------------------------
def dz1(bot, chat_id):
    bot.send_message(chat_id, text=name)


# -----------------------------------------------------------------------
def dz2(bot, chat_id):
    message = 'Привет, меня зовут ' + name + '. Мне ' + str(age) + ' лет.'
    bot.send_message(chat_id, text=message)


# -----------------------------------------------------------------------
def dz3(bot, chat_id):
    name5 = name * 5
    bot.send_message(chat_id, text=name5)


# -----------------------------------------------------------------------
def dz4(bot, chat_id):
    proc_answer_name = lambda message: bot.send_message(chat_id, f"Привет, {message.text}!")
    my_input(bot, chat_id, "Как тебя зовут?", proc_answer_name)


# -----------------------------------------------------------------------
def dz5(bot, chat_id):
    my_inputInt(bot, chat_id, "Сколько вам лет?", dz5_ResponseHandler)


def dz5_ResponseHandler(bot, chat_id, age_int):
    bot.send_message(chat_id, text=f"О! тебе уже {age_int}! \nА через год будет уже {age_int + 1}!!!")


# -----------------------------------------------------------------------
def dz6(bot, chat_id):
    dz6_ResponseHandler = lambda message: bot.send_message(chat_id,
                                                           f"Добро пожаловать {message.text}! У тебя красивое имя, в нём {len(message.text)} букв!")
    my_input(bot, chat_id, "Как тебя зовут?", dz6_ResponseHandler)


# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
def my_input(bot, chat_id, txt, ResponseHandler):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, ResponseHandler)


# -----------------------------------------------------------------------
def my_inputInt(bot, chat_id, txt, ResponseHandler):
    # bot.send_message(chat_id, text=botGames.GameRPS_Multiplayer.name, reply_markup=types.ReplyKeyboardRemove())

    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, my_inputInt_SecondPart, botQuestion=bot, txtQuestion=txt,
                                   ResponseHandler=ResponseHandler)
    # bot.register_next_step_handler(message, my_inputInt_return, bot, txt, ResponseHandler)  # то-же самое, но короче


def my_inputInt_SecondPart(message, botQuestion, txtQuestion, ResponseHandler):
    chat_id = message.chat.id
    try:
        if message.content_type != "text":
            raise ValueError
        var_int = int(message.text)
        # данные корректно преобразовались в int, можно вызвать обработчик ответа, и передать туда наше число
        ResponseHandler(botQuestion, chat_id, var_int)
    except ValueError:
        botQuestion.send_message(chat_id,
                                 text="Можно вводить ТОЛЬКО целое число в десятичной системе исчисления (символами от 0 до 9)!\nПопробуйте еще раз...")
        my_inputInt(botQuestion, chat_id, txtQuestion, ResponseHandler)  # это не рекурсия, но очень похоже
        # у нас пара процедур, которые вызывают друг-друга, пока пользователь не введёт корректные данные,
        # и тогда этот цикл прервётся, и управление перейдёт "наружу", в ResponseHandler

# -----------------------------------------------------------------------
# -----------------------------------------------------------------------