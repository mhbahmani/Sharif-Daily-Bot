from decouple import config
from app import SharifDailyBot


SharifDailyBot(
    config('TOKEN'), 
    config('ADMIN_ID'),
    config('LOG_LEVEL')).run()