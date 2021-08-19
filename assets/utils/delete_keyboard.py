import functools
from typing import Callable

from telebot.types import Message
from telebot import TeleBot

from assets.utils import variables


def delete_keyboard(func: Callable) -> Callable:
    """
    Decorator, checks a previous message's keyboard.
    If it available, removes it.

    :param func: decorating function
    """

    @functools.wraps(func)
    def wrapped(message: Message, bot: TeleBot, command: str):
        if variables.message_with_keyboard_id:
            bot.edit_message_reply_markup(
                message.from_user.id,
                message_id=variables.message_with_keyboard_id,
                reply_markup=None)
            variables.message_with_keyboard_id = None
        func(message=message, bot=bot, command=command)

    return wrapped
