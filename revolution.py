from mastodon import Mastodon
from repcal import RepublicanDate, DecimalTime
from datetime import datetime
import os
import traceback

IS_HOURLY = 'HOURLY' in os.environ

ENABLE_SEND = not True
ACCESS_TOKEN = open('access-token.txt').read().strip()
BASE_URL = 'https://botsin.space/'

HOUR_DELAY = 3601
DAY_DELAY = 24 * 3600 + 11
DELAY = HOUR_DELAY if IS_HOURLY else DAY_DELAY
MAX_LEN = 500

TAGS = """

#France #revolution #calendar #calendrier"""
MSG_LEN = MAX_LEN - len(TAGS)


def mastodon():
    return Mastodon(
        access_token = ACCESS_TOKEN,
        api_base_url = 'https://botsin.space/'
    )


def heure():
    n = datetime.now()
    rd = RepublicanDate.from_gregorian(n.date())
    dt = DecimalTime.from_standard_time(n.time())
    t = dt.get_formatter().format('%Hʰ %Mᵐ %Sˢ')
    return f'\n{dt}\n{t}'


def main():
    while True:
        h = heure()
        print(h)
        try:
            if ENABLE_SEND:
                mastodon().status_post(h + TAGS)
        except Exception:
            traceback.print_exc()
        time.sleep(DELAY)


if __name__ == '__main__':
    main()
