#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'SPridannikov'


# SOURCE: http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#schema-migrations


from playhouse.migrate import *

from db import DB_FILE_NAME


db = SqliteDatabase(DB_FILE_NAME)
migrator = SqliteMigrator(db)

with db.atomic():
    migrate(
        migrator.alter_column_type('subscription','is_active',BooleanField(default=True)),
        migrator.alter_column_type('subscription','was_sending',BooleanField(default=False)),
    )