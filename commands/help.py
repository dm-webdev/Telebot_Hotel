from telebot import types
from telebot.types import Message
from telebot import TeleBot

import assets.utils.variables as variables
from assets.utils.delete_keyboard import delete_keyboard

text_description = 'Я помогу тебе подобрать подходящий отель в городе. \n' \
                   '1. Узнать топ самых доступных отелей в городе (команда /lowprice).\n' \
                   '2. Узнать топ самых дорогих отелей в городе (команда /highprice).\n' \
                   '3. Узнать топ отелей, наиболее подходящих по цене и расположению от центра (команда /bestdeal).'


@delete_keyboard
def get_help(bot: TeleBot, message: Message, command: str):
    markup = types.InlineKeyboardMarkup()
    button_lower_price = types.InlineKeyboardButton(text='топ доступных отелей', callback_data='/lowprice')
    button_high_price = types.InlineKeyboardButton(text='топ дорогих отелей', callback_data='/highprice')
    button_best_deal = types.InlineKeyboardButton(text='топ отелей по цене и расположению', callback_data='/bestdeal')
    markup.row(button_lower_price, button_high_price)
    markup.row(button_best_deal)

    keyboard_message = bot.send_message(
        message.from_user.id,
        f'Текущая команда {command}.\n' + text_description,
        reply_markup=markup
    )
    variables.message_with_keyboard_id = keyboard_message.message_id
