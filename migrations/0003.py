#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'SPridannikov'


import datetime as DT

import db


for s in db.ExchangeRate.select():
    s.date=DT.datetime.strptime(s.date, '%d.%m.%Y')
    s.save()
