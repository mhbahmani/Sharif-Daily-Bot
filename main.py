from utils import seprate_admins
from decouple import config
from app import SharifDailyBot


SharifDailyBot(
    config('TOKEN'), 
    seprate_admins(config('ADMIN_ID')),
    config('LOG_LEVEL', default='INFO')
    ).run()