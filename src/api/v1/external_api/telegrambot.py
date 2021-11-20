import telepot
from telegram import ParseMode

from WellbeApi import settings

token = settings.TELEGRAM_BOT_TOKEN
telegramBot = telepot.Bot(token)

orders_token = settings.TELEGRAM_ORDERS_BOT_TOKEN
telegramOrdersBot = telepot.Bot(orders_token)

id_list = [
    # 386501754, # Тонкошкуров
    346178844, # Даниил
    436640485, # Никита Кузьмин
    420415601, # Виталик
    73634880,  # Ксюша
    # 388818234, # Славич
    234283090, # Димас
    72346292,  # Паша Семенов
    421306123, # Паша Компанеец
    143309296, # Инна
]

def send_message_html_to_orders_bot(text):
    for pk in id_list:
        try:
            telegramOrdersBot.sendMessage(pk, text, parse_mode=ParseMode.HTML)
        except Exception as inst:
            print(type(inst))  # the exception instance
            print(inst.args)  # arguments stored in .args
            print(inst)
            print(f"Tg User {pk} deprecated")

def send_message(text):
    text = ''.join(e for e in text if e.isalnum())
    for pk in id_list:
        try:
            telegramBot.sendMessage(pk, text, parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as inst:
            print(type(inst))  # the exception instance
            print(inst.args)  # arguments stored in .args
            print(inst)
            print(f"Tg User {pk} deprecated")

def send_message_html(text):
    for pk in id_list:
        try:
            telegramBot.sendMessage(pk, text, parse_mode=ParseMode.HTML)
        except Exception as inst:
            print(type(inst))  # the exception instance
            print(inst.args)  # arguments stored in .args
            print(inst)
            print(f"Tg User {pk} deprecated")