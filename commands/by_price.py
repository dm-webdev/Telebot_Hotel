from typing import Union

from telebot.types import Message, CallbackQuery
from telebot import TeleBot

from assets.constants import publish_constatns
from assets.utils.api_get_location_search import get_location_id
from assets.utils.api_get_properties_list import get_hotels
from assets.utils.check_input_as_command import check_input_as_command
from assets.utils.delete_keyboard import delete_keyboard

city = ''
hotels_count = 0
current_command = ''


@delete_keyboard
def get_by_price(message: Union[Message, CallbackQuery], bot: TeleBot, command: str) -> None:
    global current_command
    current_command = command
    command_desc = 'Топ отелей с низкой ценой' if current_command == '/lowprice' else 'Топ отелей с высокой ценой'

    bot.send_message(message.from_user.id, f'Текущая команда {command} \n{command_desc}.\nВ каком городе ищем?')
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
        bot.send_message(message.from_user.id, 'Сколько отелей необходимо вывести в результате?')
        bot.register_next_step_handler(message, get_hotels_count, bot=bot)


@check_input_as_command
def get_hotels_count(message: Message, bot: TeleBot) -> None:
    global hotels_count

    try:
        hotels_count = int(message.text)
        if publish_constatns.MAX_HOTEL_COUNT < hotels_count or hotels_count < 1:
            bot.send_message(
                message.from_user.id,
                f'Пожалуйста, введите число от 1 до {publish_constatns.MAX_HOTEL_COUNT}.'
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
    result = None

    if not location:
        bot.send_message(message.from_user.id, f'К сожалению такой город {city}, не найден. Повторите запрос.')
        return None

    query_data = {
        'destinationId': location[0],
        'pageSize': hotels_count,
    }

    if current_command == '/lowprice':
        query_data['sortOrder'] = 'PRICE'
        result = get_hotels(query_data)

    if current_command == '/highprice':
        query_data['sortOrder'] = 'PRICE_HIGHEST_FIRST'
        result = get_hotels(query_data)

    bot.send_message(message.from_user.id, f'Результаты поиска отелей в {location[1]}:\n{result}')
