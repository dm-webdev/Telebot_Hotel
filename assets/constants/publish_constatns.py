from commands import bestdeal
from commands import help
from commands import start
from commands import by_price


MENU = {
    '/help': help.get_help,
    '/lowprice': by_price.get_by_price,
    '/highprice': by_price.get_by_price,
    '/bestdeal': bestdeal.get_best_deal,
    '/start': start.get_start
}

MAX_HOTEL_COUNT = 20
MAX_PRICE = 100000
MAX_DISTANCE = 20
