from telebot.types import Message
from telebot import TeleBot

from assets.components.button import create_button
import assets.utils.variables as variables
from assets.utils.delete_keyboard import delete_keyboard

text_content = 'Я помогу подобрать подходящий отель. Жми /help для просмотра всех моих возможностей.'


@delete_keyboard
def get_start(bot: TeleBot, message: Message, command: str) -> None:
    if bool(message.from_user.username):
        name = message.from_user.username
    else:
        name = message.from_user.first_name
    keyboard = create_button(desc='описание команд', command='/help')

    keyboard_message = bot.send_message(
        message.from_user.id,
        f'Привет, {name}!\n' + text_content,
        reply_markup=keyboard
    )
    variables.message_with_keyboard_id = keyboard_message.message_id
