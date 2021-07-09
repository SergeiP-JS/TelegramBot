#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'SPridannikov'


from decimal import Decimal

import requests
from bs4 import BeautifulSoup

import db


def parse():
    url = 'https://www.cbr.ru/scripts/XML_daily.asp'  # url страницы

    r = requests.get(url)  # отправляем HTTP запрос и получаем результат
    soup = BeautifulSoup(r.text, 'html.parser')

    for s in soup.find_all('valute'):
        if s.charcode.string == 'USD':
            max_Exch_id = db.ExchangeRate.select().count()

            if not db.ExchangeRate.select().first():
                db.ExchangeRate.create(date=soup.valcurs['date'], value=Decimal(s.value.string.replace(',', '.')))
                print(s.charcode.string + " " + s.value.string)

                for s in db.Subscription.select():
                    s.was_sending = 0
                    s.save()
            else:
                if db.ExchangeRate.get(db.ExchangeRate.id == max_Exch_id).date != soup.valcurs['date']:
                    db.ExchangeRate.create(date=soup.valcurs['date'], value=Decimal(s.value.string.replace(',', '.')))
                    print(s.charcode.string + " " + s.value.string)

                    for s in db.Subscription.select():
                            s.was_sending = 0
                            s.save()
            break