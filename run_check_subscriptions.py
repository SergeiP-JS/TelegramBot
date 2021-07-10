#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'SPridannikov'


import time

from telegram import Bot, ParseMode

import db


def check_(updater):
    bot: Bot = updater.bot

    while True:
        # print(1)
        for s in db.Subscription.select():
            # print(s.chat_id, s.was_sending, s.is_active)
            if s.was_sending == False and s.is_active:
                bot.send_message(s.chat_id,
                    f'Актуальный курс USD за <b><u>{db.ExchangeRate.get_last().date}</u></b>: '
                    f'{db.ExchangeRate.get_last().value}₽',
                    parse_mode=ParseMode.HTML)

                s.was_sending = True
                s.save()

        time.sleep(2)
