import datetime
import requests
from typing import Optional
import json

from assets.constants import constants


def get_distance_to_centre(landmarks: list) -> Optional[str]:
    """
    Function is for getting a distance to center of the city.

    :param landmarks: list of landmarks
    :return: distance to center as string
    """

    for i in landmarks:
        if i['label'] == 'Центр города':
            return i['distance']
    return None


def get_address(address: dict) -> str:
    """
    Function is for getting an address of the city.

    :param address: dict - current address
    :return: address of the city as string
    """

    if 'streetAddress' in address:
        return address['streetAddress']
    return address['locality']


def search_result_to_human_string(data: dict) -> str:
    """
    Function is for converting a search result to a string.

    :param data: dict - search result
    :return: search result as string
    """

    search_result = data['searchResults']['results']
    if search_result:
        human_string = ''
        for i_hotel in search_result:
            description = f"Отель - {i_hotel['name']}\n" \
                          f"Адрес - {get_address(i_hotel['address'])}\n" \
                          f"Цена за ночь - {i_hotel['ratePlan']['price']['exactCurrent']} руб\n"

            distance = get_distance_to_centre(i_hotel['landmarks'])
            if distance:
                description += f"Расстояние до центра - {distance}\n"
            human_string += description + '------------------------------\n'
        return human_string
    return 'По вашему запросу ничего не найдено. Попробуйте еще раз.'


def get_hotels(query_data: dict):
    """
    Function is for getting hotels from API

    :param query_data: dict - request parameters
    :return: str - hotels
    """

    url = 'https://hotels4.p.rapidapi.com/properties/list'

    querystring = {
        "adults1": 1,
        "pageNumber": 1,
        "checkOut": datetime.datetime.now().date() + datetime.timedelta(days=2),
        "checkIn": datetime.datetime.now().date() + datetime.timedelta(days=1),
        "locale": "ru_RU",
        "currency": "RUB",
    }

    querystring.update(query_data)

    response = requests.request("GET", url, headers=constants.headers, params=querystring)
    hotels_description = search_result_to_human_string(json.loads(response.text)['data']['body'])

    return hotels_description
