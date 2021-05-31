from collections import defaultdict
from decouple import config
from app import SharifDailyBot


SharifDailyBot(
    config('TOKEN'), 
    config('ADMIN_ID', cast=int),
    config('LOG_LEVEL', default='INFO')
    ).run()