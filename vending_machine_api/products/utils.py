from users.const import ALLOWED_COINS_TO_DEPOSIT


def get_change(amount):
    coins = []

    for coin in reversed(ALLOWED_COINS_TO_DEPOSIT):
        while amount >= coin:
            amount -= coin
            coins.append(coin)
    return coins
