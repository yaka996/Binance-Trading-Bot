import os
# use if needed to pass args to external modules
import sys
# used for directory handling
import glob
import time
import threading

from helpers.parameters import (
    parse_args, load_config
)

# Load creds modules
from helpers.handle_creds import (
    load_correct_creds, test_api_key,
    load_telegram_creds
)

from settings import *

def dynamic_settings(type, DYNAMIC_WIN_LOSS_UP, DYNAMIC_WIN_LOSS_DOWN, STOP_LOSS, TAKE_PROFIT, TRAILING_STOP_LOSS, CHANGE_IN_PRICE_MAX, CHANGE_IN_PRICE_MIN, HOLDING_TIME_LIMIT):

    global session_struct

    if DYNAMIC_SETTINGS:

        if type == 'performance_adjust_up':
            STOP_LOSS = STOP_LOSS + (STOP_LOSS * DYNAMIC_WIN_LOSS_UP) / 100
            TAKE_PROFIT = TAKE_PROFIT + (TAKE_PROFIT * DYNAMIC_WIN_LOSS_UP) / 100
            TRAILING_STOP_LOSS = TRAILING_STOP_LOSS + (TRAILING_STOP_LOSS * DYNAMIC_WIN_LOSS_UP) / 100
            CHANGE_IN_PRICE_MAX = CHANGE_IN_PRICE_MAX + (CHANGE_IN_PRICE_MAX * DYNAMIC_WIN_LOSS_UP) /100
            CHANGE_IN_PRICE_MIN = CHANGE_IN_PRICE_MIN - (CHANGE_IN_PRICE_MIN * DYNAMIC_WIN_LOSS_UP) /100
            HOLDING_TIME_LIMIT = HOLDING_TIME_LIMIT + (HOLDING_TIME_LIMIT * DYNAMIC_WIN_LOSS_UP) / 100
            session_struct['dynamic'] = 'none'
            print(f'{txcolors.NOTICE}>> Last Trade WON Changing STOP_LOSS: {STOP_LOSS:.2f}/{DYNAMIC_WIN_LOSS_UP:.2f}  - TAKE_PROFIT: {TAKE_PROFIT:.2f}/{DYNAMIC_WIN_LOSS_UP:.2f} - TRAILING_STOP_LOSS: {TRAILING_STOP_LOSS:.2f}/{DYNAMIC_WIN_LOSS_UP:.2f} CIP:{CHANGE_IN_PRICE_MIN:.4f}/{CHANGE_IN_PRICE_MAX:.4f}/{DYNAMIC_WIN_LOSS_UP:.2f} HTL: {HOLDING_TIME_LIMIT:.2f} <<{txcolors.DEFAULT}')

        if type == 'performance_adjust_down':
            STOP_LOSS = STOP_LOSS - (STOP_LOSS * DYNAMIC_WIN_LOSS_DOWN) / 100
            TAKE_PROFIT = TAKE_PROFIT - (TAKE_PROFIT * DYNAMIC_WIN_LOSS_DOWN) / 100
            TRAILING_STOP_LOSS = TRAILING_STOP_LOSS - (TRAILING_STOP_LOSS * DYNAMIC_WIN_LOSS_DOWN) / 100
            CHANGE_IN_PRICE_MAX = CHANGE_IN_PRICE_MAX - (CHANGE_IN_PRICE_MAX * DYNAMIC_WIN_LOSS_DOWN) /100
            CHANGE_IN_PRICE_MIN = CHANGE_IN_PRICE_MIN + (CHANGE_IN_PRICE_MIN * DYNAMIC_WIN_LOSS_DOWN) /100
            HOLDING_TIME_LIMIT = HOLDING_TIME_LIMIT - (HOLDING_TIME_LIMIT * DYNAMIC_WIN_LOSS_DOWN) / 100
            session_struct['dynamic'] = 'none'
            print(f'{txcolors.NOTICE}>> Last Trade LOST Changing STOP_LOSS: {STOP_LOSS:.2f}/{DYNAMIC_WIN_LOSS_DOWN:.2f} - TAKE_PROFIT: {TAKE_PROFIT:.2f}/{DYNAMIC_WIN_LOSS_DOWN:.2f}  - TRAILING_STOP_LOSS: {TRAILING_STOP_LOSS:.2f}/{DYNAMIC_WIN_LOSS_DOWN:.2f} CIP:{CHANGE_IN_PRICE_MIN:.4f}/{CHANGE_IN_PRICE_MAX:.4f}/{DYNAMIC_WIN_LOSS_UP:.2f} HTL:{HOLDING_TIME_LIMIT:.2f} <<{txcolors.DEFAULT}')

        if type == 'reset':
            STOP_LOSS = parsed_config['trading_options']['STOP_LOSS']
            TAKE_PROFIT = parsed_config['trading_options']['TAKE_PROFIT']
            TRAILING_STOP_LOSS = parsed_config['trading_options']['TRAILING_STOP_LOSS']
            CHANGE_IN_PRICE_MAX = parsed_config['trading_options']['CHANGE_IN_PRICE_MAX']
            CHANGE_IN_PRICE_MIN = parsed_config['trading_options']['CHANGE_IN_PRICE_MIN']

            if not TEST_MODE: HOLDING_TIME_LIMIT = (parsed_config['trading_options']['TIME_DIFFERENCE'] * 60 * 1000) * parsed_config['trading_options']['HOLDING_INTERVAL_LIMIT']
            if TEST_MODE: HOLDING_TIME_LIMIT = (parsed_config['trading_options']['TIME_DIFFERENCE'] * 60) * parsed_config['trading_options']['HOLDING_INTERVAL_LIMIT']

            print(f'{txcolors.NOTICE}>> DYNAMIC SETTINGS RESET - STOP_LOSS: {STOP_LOSS:.2f}/{DYNAMIC_WIN_LOSS_DOWN:.2f} - TAKE_PROFIT: {TAKE_PROFIT:.2f}/{DYNAMIC_WIN_LOSS_DOWN:.2f}  - TRAILING_STOP_LOSS: {TRAILING_STOP_LOSS:.2f}/{DYNAMIC_WIN_LOSS_DOWN:.2f}CIP:{CHANGE_IN_PRICE_MIN:.4f}/{CHANGE_IN_PRICE_MAX:.4f}/{DYNAMIC_WIN_LOSS_UP:.2f} HTL: {HOLDING_TIME_LIMIT:.2f} <<{txcolors.DEFAULT}')
            session_struct['dynamic'] = 'none'

        if CHANGE_IN_PRICE_MIN > 0:
            CHANGE_IN_PRICE_MIN = parsed_config['trading_options']['CHANGE_IN_PRICE_MIN'] - (CHANGE_IN_PRICE_MIN * session_struct['market_support'])
            CHANGE_IN_PRICE_MAX = parsed_config['trading_options']['CHANGE_IN_PRICE_MAX'] - (CHANGE_IN_PRICE_MAX * session_struct['market_support'])

        if CHANGE_IN_PRICE_MAX < 0:
            CHANGE_IN_PRICE_MIN = parsed_config['trading_options']['CHANGE_IN_PRICE_MIN'] + (CHANGE_IN_PRICE_MIN * session_struct['market_support'])
            CHANGE_IN_PRICE_MAX = parsed_config['trading_options']['CHANGE_IN_PRICE_MAX'] + (CHANGE_IN_PRICE_MAX * session_struct['market_support'])

    return STOP_LOSS, TAKE_PROFIT, TRAILING_STOP_LOSS, CHANGE_IN_PRICE_MAX, CHANGE_IN_PRICE_MIN, HOLDING_TIME_LIMIT