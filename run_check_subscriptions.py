#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'SPridannikov'


import time

from telegram import Bot, ParseMode

import db


def check(bot: Bot):
    while True:
        for s in db.Subscription.get_active_unsent_subscriptions():
            rate = db.ExchangeRate.get_last()

            bot.send_message(
                s.chat_id,
                f'Актуальный курс USD за <b><u>{rate.date:%d.%m.%Y}</u></b>: {rate.value}₽',
                parse_mode=ParseMode.HTML
             )

            s.was_sending = True
            s.save()

        time.sleep(2)
