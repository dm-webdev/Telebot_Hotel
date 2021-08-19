import functools
from typing import Callable

from telebot.types import Message
from telebot import TeleBot

from assets.constants import publish_constatns


def check_input_as_command(func: Callable) -> Callable:
    """
    Decorator, checks the entered user command.
    If this is one of the service commands, then a new command starts and current breaks.

    :param func: decorating function
    """

    @functools.wraps(func)
    def wrapped(message: Message, bot: TeleBot):
        if message.text in publish_constatns.MENU.keys():
            publish_constatns.MENU[message.text](bot=bot, message=message, command=message.text)
        else:
            func(message=message, bot=bot)

    return wrapped
