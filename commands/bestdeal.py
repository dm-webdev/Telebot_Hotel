from typing import Union

from telebot.types import Message, CallbackQuery
from telebot import TeleBot

from assets.constants import publish_constatns
from assets.utils.api_get_location_search import get_location_id
from assets.utils.api_get_properties_list import get_hotels
from assets.utils.check_input_as_command import check_input_as_command
from assets.utils.delete_keyboard import delete_keyboard

current_command = ''
city = ''
min_price = 0
max_price = 1000000
max_distance = 1000000
hotels_count = 0


@delete_keyboard
def get_best_deal(bot: TeleBot, message: Union[Message, CallbackQuery], command: str) -> None:
    global current_command
    current_command = command

    bot.send_message(message.from_user.id, f'Текущая команда {command}.\nВ каком городе ищем?')
    next_message = message if isinstance(message, Message) else message.message
    bot.register_next_step_handler(next_message, get_city, bot=bot)


@check_input_as_command
def get_city(message: Message, bot: TeleBot) -> None:
    global city
    city = message.text

    if len(city) < 2:
        bot.send_message(message.from_user.id, 'Введите верное название города.')
        bot.register_next_step_handler(message, get_city, bot=bot)
    else:
        bot.send_message(message.from_user.id, 'Введите минимальную цену отеля за ночь, руб.')
        bot.register_next_step_handler(message, get_min_price, bot=bot)


@check_input_as_command
def get_min_price(message: Message, bot: TeleBot) -> None:
    global min_price

    try:
        min_price = int(message.text)
        if publish_constatns.MAX_PRICE < min_price or min_price < 1:
            bot.send_message(
                message.from_user.id,
                f'Пожалуйста, введите целое число от 1 до {publish_constatns.MAX_PRICE} руб.'
            )
            bot.register_next_step_handler(message, get_min_price, bot=bot)
        else:
            bot.send_message(message.from_user.id, 'Введите максимальную цену отеля за ночь, руб.')
            bot.register_next_step_handler(message, get_max_price, bot=bot)
    except ValueError:
        bot.send_message(message.from_user.id, 'Пожалуйста, введите целое число.')
        bot.register_next_step_handler(message, get_min_price, bot=bot)


@check_input_as_command
def get_max_price(message: Message, bot: TeleBot) -> None:
    global max_price

    try:
        max_price = int(message.text)
        if publish_constatns.MAX_PRICE < max_price or max_price < 1:
            bot.send_message(
                message.from_user.id,
                f'Пожалуйста, введите целое число от 1 до {publish_constatns.MAX_PRICE} руб.'
            )
            bot.register_next_step_handler(message, get_max_price, bot=bot)
        elif min_price > max_price:
            bot.send_message(
                message.from_user.id,
                f'Максимальная цена {max_price} руб, должна быть больше минимальной {min_price} руб.\n'
                f'Введите заново минимальную цену отеля за ночь, руб.')
            bot.register_next_step_handler(message, get_min_price, bot=bot)
        else:
            bot.send_message(message.from_user.id, 'Введите максимальное расстояние до центра, км.')
            bot.register_next_step_handler(message, get_max_distance, bot=bot)
    except ValueError:
        bot.send_message(message.from_user.id, 'Пожалуйста, введите целое число.')
        bot.register_next_step_handler(message, get_max_price, bot=bot)


@check_input_as_command
def get_max_distance(message: Message, bot: TeleBot) -> None:
    global max_distance

    try:
        max_distance = float(message.text)
        if publish_constatns.MAX_DISTANCE < max_distance or max_distance < 1:
            bot.send_message(
                message.from_user.id,
                'Пожалуйста, введите число от 1 до {:.1f} км.'.format(publish_constatns.MAX_DISTANCE)
            )
            bot.register_next_step_handler(message, get_max_distance, bot=bot)
        else:
            bot.send_message(message.from_user.id, 'Сколько отелей необходимо вывести в результате?')
            bot.register_next_step_handler(message, get_hotels_count, bot=bot)
    except ValueError:
        bot.send_message(message.from_user.id, 'Пожалуйста, введите число в формате 1.1')
        bot.register_next_step_handler(message, get_max_distance, bot=bot)


@check_input_as_command
def get_hotels_count(message: Message, bot: TeleBot) -> None:
    global hotels_count

    try:
        hotels_count = int(message.text)
        if publish_constatns.MAX_HOTEL_COUNT < hotels_count or hotels_count < 1:
            bot.send_message(
                message.from_user.id,
                f'Пожалуйста, введите целое число от 1 до {publish_constatns.MAX_HOTEL_COUNT}.'
            )
            bot.register_next_step_handler(message, get_hotels_count, bot=bot)
        else:
            bot.send_message(
                message.from_user.id,
                f'Веду поиск. Выбран город: {city}, буду выводить {hotels_count} отелей. Подождите немного...'
            )
            get_api_hotels(message, bot)
    except ValueError:
        bot.send_message(message.from_user.id, 'Пожалуйста, введите целое число.')
        bot.register_next_step_handler(message, get_hotels_count, bot=bot)


def get_api_hotels(message: Message, bot: TeleBot) -> None:
    location = get_location_id({'query': city})

    if not location:
        bot.send_message(message.from_user.id, f'К сожалению такой город {city}, не найден. Повторите запрос.')
        return None

    query_data = {
        'destinationId': location[0],
        'pageSize': hotels_count,
        'sortOrder': 'PRICE',
        'landmarkIds': str(max_distance),
        'priceMax': max_price,
        'priceMin': min_price,
    }

    result = get_hotels(query_data)

    bot.send_message(message.from_user.id, f'Результаты поиска отелей в {location[1]}:\n\n{result}')
