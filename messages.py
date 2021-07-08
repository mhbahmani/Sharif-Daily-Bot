start_message = """
سلام. به بات «برنامه‌های پیشنهادی فردا» روزنامه‌ی شریف خوش‌آمدید.
اگر برنامه‌ای در دانشگاه شریف برگزار می‌شود که دوست دارید در پست برنامه‌های پیشنهادی فردا در کانال روزنامه شریف درج شود، با استفاده از این بات می‌توانید زمان و مکان برگزاری آن‌را اعلام کنید.
برای افزدون برنامه، از دستور /add استفاده کنید.
"""

help_message = """
/add: اضافه کردن رویداد جدید

/help: مشاهده‌ی راهنما
"""

admin_help_message = """
دستورات کاربران:
{}

دستورات ادمین (این بخش به کاربران عادی نمایش داده نمی‌شود)
/get: با این دستور می‌توانید پیام برنامه‌های پیشنهادی فردا را دریافت کنید.
""".format(help_message)

add_message = """
هر کدام از اطلاعات زیر در مورد برنامه‌ی خود را با کلیک روی آن می‌توانید وارد کنید.
"""

choices_message = {
    'Title': 'عنوان برنامه‌',
    'Month': 'تاریخ برگزاری برنامه (نام ماه را به فارسی بنویسید)',
    'Day': """
تاریخ برگزاری برنامه (روز را به صورت یک عدد فارسی بنویسید)
نمونه: ۲۹    
    """,
    'Date': 'تاریخ برنامه‌ی خود رو در تقویم زیر انتخاب کنید:',
    'Time': 'ساعت برنامه',
    'Invited': 'مدعو برنامه',
    'Location': 'محل برگزاری برنامه (اگر برنامه به صورت حضوری برگزار می‌شود)',
    'Link': 'لینک حضور مجازی در برنامه',
    'Telegram Channel': 'کانال تلگرام برگزارکننده',
    'Calendar': 'لینک برنامه در تقویم گوگل',
    'Done': """
اطلاعات زیر در مورد برنامه‌ی شما دریافت شد:
{}
برای اضافه کردن برنامه‌ی جدید، از دستور /add استفاده کنید.
    """
}

received_info_message = """
دریافت شد. اطلاعاتی که تا کنون از برنامه‌ی خود داده‌اید:
{}
می‌توانید گزینه‌ی دیگری را انتخاب کنید و یا اطلاعات فعلی را اصلاح کنید و یا با کلیک روی گزینه‌ی «ثبت» برنامه‌ی خود را ثبت کنید.
"""


fa_choices_keyboard = [
    ['عنوان', 'مدعو'],
    ['ماه', 'روز', 'ساعت'],
    ['مکان (حضوری)', 'لینک برگزاری', 'کانال تلگرام'],
    ['ثبت', 'انصراف'],
]

choices_keyboard = [
    ['Title', 'Invited'],
    ['Date', 'Time'],
    ['Location', 'Link', 'Telegram Channel'],
    ['Done', 'Cancel'],
]

choices_to_fa = {
    'Title': 'عنوان برنامه',
    'Invited': 'مدعو برنامه',
    'Date': 'تاریخ برنامه',
    'Time': 'ساعت',
    'Location': 'مکان (حضوری)',
    'Link': 'لینک برگزاری',
    'Telegram Channel': 'کانال تلگرام برگزار کننده',
    'Calendar': 'لینک تقویم گوگل',
    'Done': 'ثبت',
    'Cancel': 'انصراف',
}

event_emojis = {
    'Title': '🔸',
    'Invited': '👤',
    'Time': '🕑 ساعت',
    'Location': 'مکان (حضوری)',
    'Link': '🖥',
    'Telegram Channel': '🆔',
    'Calendar': 'لینک تقویم گوگل',
}


months = [
    ['خرداد' ,'اردیبهشت' ,'فروردین', ],
    ['شهریور' ,'مرداد' ,'تیر'],
    ['آذر' ,'آبان' ,'مهر'],
    ['اسفند' ,'بهمن', 'دی',]
]

CALLBACK_ERROR = 'دریافت اطلاعات با خطا مواجه شد'

days = [
    'شنبه', 'یک‌‌شنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه'
]

info = ['Title', 'Time', 'Invited', 'Link', 'Location', 'Telegram Channel']

fill_mandatory_fields_message = """
برخی از مشخصات برنامه ضروری هستند. از اطلاعات ضروری، موارد زیر را تکمیل نکرده‌اید:
{}
"""

add_event_failed_message = 'اضافه کردن رویداد با خطایی مواجه شد. لطفا دوباره تلاش کنید. در صورت حل نشدن، مشکل را با ادمین در میان بگذارید.'

new_event_admin_message = 'برنامه‌ی جدید اضافه کرد {}'

new_event_failed_admin_message = """
اضافه کردن برنامه‌ی جدید {} با خطا مواجه شد
اطلاعات برنامه:
{}
"""


suggestion_message_header = '☀️برنامه‌های پیشنهادی فردا، %A {} %B:'

you_are_not_admin_message = 'You don\'t have the right access'

TIME_PICKER_CALLBACK = 'TIME'
CALENDAR_CALLBACK = 'CALENDAR'