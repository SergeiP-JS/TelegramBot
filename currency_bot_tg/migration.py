
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#schema-migrations


from playhouse.migrate import *
from db import DB_FILE_NAME


db = SqliteDatabase(DB_FILE_NAME)
migrator = SqliteMigrator(db)

with db.atomic():
    migrate(
        migrator.alter_column_type('subscription','chat_id',IntegerField(unique=True)),
        migrator.alter_column_type('exchangeRate', 'date', DateField(unique=True)),
    )