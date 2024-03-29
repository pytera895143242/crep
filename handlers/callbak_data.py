from aiogram import types

from misc import dp, bot
from .sqlit import  cheak_traf, reg_user, reg_pod, reg_traf_support

import random

reg_user(1, 1)


def obnovlenie():
    global name_channel_1, name_channel_2, name_channel_3, link_channel_1, link_channel_2, link_channel_3
    list_channel = cheak_traf()

    name_channel_1 = list_channel[0][0][1:]
    link_channel_1 = list_channel[0][1]

    name_channel_2 = list_channel[1][0][1:]
    link_channel_2 = list_channel[1][1]

    name_channel_3 = list_channel[2][0][1:]
    link_channel_3 = list_channel[2][1]


obnovlenie()  # Стартовое обновление каналов


def markup_sub(name_channel):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='🥤Я ПОДПИСАЛСЯ🥤', callback_data=f'check{name_channel}')
    markup.add(bat_a)
    return markup


text_closed = f"""❌ ДОСТУП ЗАКРЫТ ❌

👉Для доступа к приватному каналу нужно быть подписчиком <b>Кино-каналов.</b>

Подпишись на <b>каналы</b> ниже 👇 и нажми кнопку <b>Я ПОДПИСАЛСЯ</b> для проверки!

<b>Канал 1</b> - <a href = "{link_channel_1}">https://t.me/{name_channel_1}</a>
<b>Канал 2</b> - <a href = "{link_channel_2}">https://t.me/{name_channel_2}</a>
<b>Канал 3</b> - <a href = "{link_channel_3}">https://t.me/{name_channel_3}</a>"""


@dp.callback_query_handler(text_startswith='start_watch')  # Нажал кнопку Начать смотреть
async def start_watch(call: types.callback_query):
    name_channel = call.data[12:]
    await bot.send_message(call.message.chat.id, text_closed, reply_markup=markup_sub(name_channel),
                           disable_web_page_preview=True)
    await bot.answer_callback_query(call.id)


@dp.callback_query_handler(text_startswith='check')  # Нажал кнопку Я ПОДПИСАЛСЯ. ДЕЛАЕМ ПРОВЕРКУ
async def check(call: types.callback_query):
    await bot.send_message(call.message.chat.id, '⏳ Ожидайте. Идёт проверка подписки.')
    name_channel = call.data[5:]

    try:  # Канал 1
        proverka1 = (await bot.get_chat_member(chat_id=f'@{name_channel_1}', user_id=call.message.chat.id)).status
        if proverka1 == 'member':
            reg_pod(id=call.message.chat.id, channel=name_channel_1)  # Регистрация статистики 1к
    except:
        proverka1 = 'member'
        reg_pod(id=call.message.chat.id, channel=name_channel_1)  # Регистрация статистики 1к

    try:  # Канал 2
        proverka2 = (await bot.get_chat_member(chat_id=f'@{name_channel_2}', user_id=call.message.chat.id)).status
        if proverka2 == 'member':
            reg_pod(id=call.message.chat.id, channel=name_channel_2)  # Регистрация статистики 2к
    except:
        proverka2 = 'member'
        reg_pod(id=call.message.chat.id, channel=name_channel_2)  # Регистрация статистики 2к

    try:  # Канал 3
        proverka3 = (await bot.get_chat_member(chat_id=f'@{name_channel_3}', user_id=call.message.chat.id)).status
        if proverka3 == 'member':
            reg_pod(id=call.message.chat.id, channel=name_channel_3)  # Регистрация статистики 3к
    except:
        proverka3 = 'member'
        reg_pod(id=call.message.chat.id, channel=name_channel_3)  # Регистрация статистики 3к

    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='🥤Я ПОДПИСАЛСЯ🥤', callback_data=f'check{name_channel}')
    markup.add(bat_a)

    if (proverka1 == 'member' and proverka2 == 'member' and proverka3 == 'member') or proverka1 == 'administrator' or proverka2 == 'administrator' or proverka3 == 'administrator':  # Человек прошел все 3 проверки
        if random.randint(1, 3) == 2:
            reg_traf_support(id=call.message.chat.id, channel=name_channel)
        if name_channel == '':
            ######  Человек перещел без реферальной ссылке    #####
            markup_2 = types.InlineKeyboardMarkup()
            bat_b = types.InlineKeyboardButton(text='🥤ПОДПИСАТЬСЯ🥤',
                                               url=f'https://t.me/{name_channel_1}')  # Cсылка на приват канал # ВАЖНО!!!!!
            markup_2.add(bat_b)
            await bot.send_message(call.message.chat.id, '✅ ДОСТУП ОТКРЫТ\n\n'
                                                         'Все новинки 2021 сливаем на наш приватный канал.<b> Подпишись</b> 👇',
                                   parse_mode='html', reply_markup=markup_2)

            ###########   Человек перешел по реферальной ссылке    ##########

        else:
            markup_2 = types.InlineKeyboardMarkup()
            bat_b = types.InlineKeyboardButton(text='🥤ПОДПИСАТЬСЯ🥤',
                                               url=f'https://t.me/{name_channel}')  # Cсылка на приват канал
            markup_2.add(bat_b)
            await bot.send_message(call.message.chat.id, '✅ ДОСТУП ОТКРЫТ\n\n'
                                                         'Все новинки 2021 сливаем на наш приватный канал.<b> Подпишись</b> 👇',
                                   parse_mode='html', reply_markup=markup_2)


    else:
        await bot.send_message(call.message.chat.id, '❌Вы не подписались на каналы ниже\n\n'
                                                     'Проверьте еще раз подписку на всех каналах. И нажми кнопку <b>Я ПОДПИСАЛСЯ</b> для проверки!\n\n'
                                                     f'<b>Канал 1</b> - <a href = "{link_channel_1}">https://t.me/{name_channel_1}</a>\n'
                                                     f'<b>Канал 2</b> - <a href = "{link_channel_2}">https://t.me/{name_channel_2}</a>\n'
                                                     f'<b>Канал 3</b> - <a href = "{link_channel_3}">https://t.me/{name_channel_3}</a>\n',
                               parse_mode='html', reply_markup=markup, disable_web_page_preview=True)

    await bot.answer_callback_query(call.id)
