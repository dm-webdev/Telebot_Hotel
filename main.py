import telebot
from telebot.types import Message, CallbackQuery

from assets.components import button
from assets.constants import constants
from assets.constants import publish_constatns
from assets.utils import variables

bot = telebot.TeleBot(constants.TOKEN)


@bot.message_handler(content_types=['text'])
def get_text_messages(message: Message) -> None:
    if message.text in publish_constatns.MENU.keys():
        publish_constatns.MENU[message.text](bot=bot, message=message, command=message.text)
    else:
        keyboard = button.create_button(desc='помощь', command='/help')
        keyboard_message = bot.send_message(
            message.from_user.id,
            'Такая команда отсутствует. Жми /help.',
            reply_markup=keyboard
        )
        variables.message_with_keyboard_id = keyboard_message.message_id


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call: CallbackQuery) -> None:
    if call.data in publish_constatns.MENU.keys():
        publish_constatns.MENU[call.data](bot=bot, message=call, command=call.data)


bot.polling(none_stop=True, interval=0)
