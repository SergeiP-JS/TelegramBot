#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'SPridannikov'
import os
import time
import datetime as DT
from threading import Thread
import db
from parser_ import parser_
from run_check_subscriptions import check_


# pip install python-telegram-bot
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext,CallbackQueryHandler
from telegram.ext.dispatcher import run_async

from config import TOKEN
from common import get_logger, log_func, reply_error


log = get_logger(__file__)

COMMANDS = [['Подписаться'],['Последнее значение', 'За неделю', 'За месяц']]
REPLY_KEYBOARD_MARKUP = ReplyKeyboardMarkup(COMMANDS, resize_keyboard=True)
@run_async
@log_func(log)
def on_start(update: Update, context: CallbackContext):
    # TODO: добавить описание бота и как с ним работать
    # TODO: отобразить клавиатуру
    update.message.reply_text(
        'Данный бот способен отслежтвать USD валюту и отправлять вам уведомление при изменении $.'
        ' С помощью меню вы можете подписаться/отписаться от рассылки, узнать актуальный курс за день, неделю или месяц.',
        reply_markup=REPLY_KEYBOARD_MARKUP
    )
@run_async
@log_func(log)
def on_reply_command(update: Update, context: CallbackContext):
    message = update.message

    message.reply_text(
        'Reply command: ' + message.text,
        reply_markup=REPLY_KEYBOARD_MARKUP
    )


@run_async
@log_func(log)
def on_command_up(update: Update, context: CallbackContext):
    message = update.message
    print()
    for s in db.Subscription.select():

        if s.chat_id == update.effective_chat.id:

            if s.is_active:
                s.is_active = 0
                s.save()
                s.was_sending = 0
                s.save()
                COMMANDS[0][0]="Подписаться"
                message.text = "отписались"
            else:
                s.is_active = 1
                s.save()
                s.modification_datetime = DT.datetime.now()
                s.save()
                COMMANDS[0][0] = "Отписаться"
                message.text="подписались"
            break


    if not db.Subscription.select().where(db.Subscription.chat_id == update.effective_chat.id):
            db.Subscription.create(chat_id=update.effective_chat.id, is_active='true', was_sending='false')

    message.reply_text(
        'Вы успешно ' + message.text,
        reply_markup=ReplyKeyboardMarkup(COMMANDS, resize_keyboard=True)
    )


@run_async
@log_func(log)
def on_command_0(update: Update, context: CallbackContext):
    if db.ExchangeRate.select().first():

        message = update.message
        message.reply_text(
            f'Актуальный курс USD за {db.ExchangeRate.get(db.ExchangeRate.id == db.ExchangeRate.select().count()).date}: {db.ExchangeRate.get(db.ExchangeRate.id == db.ExchangeRate.select().count()).value}$',
            reply_markup=ReplyKeyboardMarkup(COMMANDS, resize_keyboard=True)
        )
    else:
        message = update.message
        message.reply_text(
            'Бот ещё молодой и не имеет достаточно информации',
            reply_markup=ReplyKeyboardMarkup(COMMANDS, resize_keyboard=True)
        )

@run_async
@log_func(log)
def on_command_1(update: Update, context: CallbackContext):
        flag=0
        arr=[]
        i=0
        for val in reversed(db.ExchangeRate.select()):
            if i==7:
                flag=1
                break
            arr.append(val.value)
            i+=1
        if flag:
            message = update.message
            message.reply_text(
                f'Среднее USD за неделю: {float(sum(arr)) / max(len(arr), 1)}$',
                reply_markup=ReplyKeyboardMarkup(COMMANDS, resize_keyboard=True)
            )
        else:
            message = update.message
            message.reply_text(
                'Бот ещё молодой и не имеет достаточно информации',
                reply_markup=ReplyKeyboardMarkup(COMMANDS, resize_keyboard=True)
            )

@run_async
@log_func(log)
def on_command_2(update: Update, context: CallbackContext):
        flag=0
        arr = []
        i = 0
        for val in reversed(db.ExchangeRate.select()):
            if i == 30:
                flag = 1
                break
            arr.append(val.value)
            i += 1
        if flag:
            message = update.message
            message.reply_text(
                f'Среднее USD за месяц: {float(sum(arr)) / max(len(arr), 1)}$',
                reply_markup=ReplyKeyboardMarkup(COMMANDS, resize_keyboard=True)
            )
        else:
            message = update.message
            message.reply_text(
                'Бот ещё молодой и не имеет достаточно информации',
                reply_markup=ReplyKeyboardMarkup(COMMANDS, resize_keyboard=True)
            )



@run_async
@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.effective_message

    text = message.text

    message.reply_text(text)


def on_error(update: Update, context: CallbackContext):
    reply_error(log, update, context)


def main():

            cpu_count = os.cpu_count()
            workers = cpu_count
            log.debug('System: CPU_COUNT=%s, WORKERS=%s', cpu_count, workers)

            log.debug('Start')

            updater = Updater(
                TOKEN,
                workers=workers,
                use_context=True
            )
            Thread(target=check_,args=(updater,)).start()
            dp = updater.dispatcher

            # Кнопки
            dp.add_handler(CommandHandler('start', on_start))
            dp.add_handler(MessageHandler(Filters.text('Подписаться'), on_command_up))
            dp.add_handler(MessageHandler(Filters.text('Отписаться'), on_command_up))
            dp.add_handler(MessageHandler(Filters.text(COMMANDS[1][0]), on_command_0))
            dp.add_handler(MessageHandler(Filters.text(COMMANDS[1][1]), on_command_1))
            dp.add_handler(MessageHandler(Filters.text(COMMANDS[1][2]), on_command_2))
            dp.add_handler(MessageHandler(Filters.text, on_request))

            dp.add_error_handler(on_error)

            updater.start_polling()
            updater.idle()

            log.debug('Finish')
def pars():
    while True:
        parser_()
        time.sleep(8*3600)


def check_1():
    updater = Updater(TOKEN)
    bot: Bot = updater.bot

    while True:
        bot.send_message(973083137,"Привет")
        time.sleep(2)


if __name__ == '__main__':
     # asyncio.run(async_())
     Thread(target=pars).start()
     #
     while True:
         try:
             main()
         except:
             log.exception('')

             timeout = 15
             log.info(f'Restarting the bot after {timeout} seconds')
             time.sleep(timeout)

