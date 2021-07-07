import time
import db
from telegram import Bot


def check_(updater):
    bot: Bot = updater.bot

    while True:
        # print(1)
        for s in db.Subscription.select():
            # print(s.chat_id, s.was_sending, s.is_active)
            if s.was_sending == 0 and s.is_active:
                bot.send_message(s.chat_id,
                                 f'Актуальный курс USD за {db.ExchangeRate.get(db.ExchangeRate.id == db.ExchangeRate.select().count()).date}: {db.ExchangeRate.get(db.ExchangeRate.id == db.ExchangeRate.select().count()).value}$')
                s.was_sending = 1
                s.save()
        time.sleep(2)
