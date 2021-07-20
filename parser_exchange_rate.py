#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'SPridannikov'


import datetime as DT
from decimal import Decimal
from typing import Tuple

import requests
from bs4 import BeautifulSoup

import db


def get_last_usd() -> Tuple[DT.date, Decimal]:
    url = 'https://www.cbr.ru/scripts/XML_daily.asp'

    rs = requests.get(url)
    soup = BeautifulSoup(rs.content, 'html.parser')

    for s in soup.find_all('valute'):
        if s.charcode.string == 'USD':
            date = DT.datetime.strptime(
                soup.valcurs['date'], '%d.%m.%Y'
            )
            return date.date(), Decimal(s.value.string.replace(',', '.'))

    raise Exception('Не удалось найти значение USD!')


def parse():
    date, value = get_last_usd()

    exchange_rate = db.ExchangeRate.get_or_none(db.ExchangeRate.date == date)
    if not exchange_rate:
        db.ExchangeRate.create(date=date, value=value)
        print(f'Добавлено: {date:%d.%m.%Y} = {value}')

        for s in db.Subscription.select():
            s.was_sending = False
            s.save()