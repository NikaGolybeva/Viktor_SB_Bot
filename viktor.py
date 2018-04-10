
#!/usr/bin/python
# -*- coding: utf-8 -*-
# какая-то шляпа чтобы он не общался юникодом
# настройка импорта , импортируем модули телеграма
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json
updater = Updater(token='555129973:AAEAvx3fCfB1yugb2vTaEP19xl7s26Nq0hk') # Токен API к Telegram
dispatcher = updater.dispatcher

# прописываем callback функции, которые будут вызываться тогда, когда будет получено обновление
# аргументы bot содержит необходимые методы для взаимодействия с API
# update - данные о пришедшем сообщении
def startCommand(bot, update):# обработка команды start для бота
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?') 
   
def textMessage(bot, update): # обработка текстового сообщения
    request = apiai.ApiAI('fc1af16819ad41b6b266fb609dab99c3').text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'Viktor_SB_Bot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text # Посылаем запрос к Dialogflow с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я тебя не понял. Мне нужно подучиться.')
# Хендлеры 
 # Присваиваем уведомлениям обработчики
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
# Поиск обновлений
updater.start_polling(clean=True)
# Остановка Ctrl + C
updater.idle()
"""
Created on Sun Apr  8 18:23:51 2018

@author: Вероника
"""

