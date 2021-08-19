from telebot import types


def create_button(desc: str, command: str) -> types.InlineKeyboardMarkup:
    """
    Function's for creating the inline-keyboard and one button.

    :param desc: str - description of button
    :param command: str - command sent to bot
    :return: InlineKeyboardMarkup
    """

    keyboard = types.InlineKeyboardMarkup()
    button_help = types.InlineKeyboardButton(text=desc, callback_data=command)
    keyboard.add(button_help)

    return keyboard
