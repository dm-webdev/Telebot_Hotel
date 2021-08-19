import requests
from typing import Optional
import json

import assets.constants.constants as constants


def find_destination_id(data: dict, name: str) -> Optional[list]:
    """
    Function is for search destination's id in api-response.

    :param data: dict - API response
    :param name: str - search string
    :return: destinationId: str - location's id and name of place from api
    """

    entries = list(filter(lambda i_data: i_data['group'] == 'CITY_GROUP', data['suggestions']))[0]['entities']
    if not entries:
        return None

    for i in entries:
        if name == i['name']:
            return [i['destinationId'], i['name']]
    return [entries[0]['destinationId'], entries[0]['name']]


def get_location_id(query_str: dict) -> list:
    """
    Function is for getting destination's id from API

    :param query_str: dict - request parameters
    :return: location
    """

    url = 'https://hotels4.p.rapidapi.com/locations/search'
    querystring = {'locale': 'ru_RU'}
    querystring.update(query_str)

    response = requests.request('GET', url, headers=constants.headers, params=querystring)

    location = find_destination_id(json.loads(response.text), querystring['query'])

    return location
