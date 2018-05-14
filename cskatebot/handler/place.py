# coding: utf8

import logging
from telegram.ext import Handler

logger = logging.getLogger(__name__)


class PlaceHandler(Handler):

    def __init__(self, storage, *args, **kwargs):
        self.storage = storage

    def check_update(self, update):
        for place in self.storage.places.values():
            if place.is_relative_text(update.message.text):
                return True
        return False

    def handle_update(self, update, dispatcher):
        bot = dispatcher.bot  # noqa
        place = None
        for plc in self.storage.places.values():
            if plc.is_relative_text(update.message.text):
                place = plc
                break

        if place is None:
            update.message.reply_text('Внутренняя ошибка, не смогли определить место')
            return

        action, info = place.detect_type_and_process_message(update.message.text)
        if action == 'join':
            place.set_attendant(update.message.from_user, info)
            total = place.get_stats()
            update.message.reply_html(
                "<b>%s</b>\n\nСпасибо, что придёшь\n\nВсего отметилось: <b>%s</b>\n\nПосмотреть список: %s\nПолный список: /stat" % (
                    place.name,
                    total,
                    '/' + place.id + '_list'
                )
            )
            return
        elif action == 'leave':
            place.set_attendant(update.message.from_user, 0)
            total = place.get_stats()
            update.message.reply_html(
                "<b>%s</b>\n\nОчень жаль, нам будет тебя не хватать\n\nБез тебя останется <b>%s</b> человек.\n\nПосмотреть список: %s\nПрисоединиться: %s\nПолный список: /stat" % (
                    place.name,
                    total,
                    '/' + place.id + '_list',
                    '/' + place.id + '_join',
                )
            )
            return

        total = place.get_stats()

        attendants_string = '\n'.join([" %s +%s" % (v['name'], v['amount']) for v in place.attendants.values()])
        in_place_string = ''
        if place.is_attendant(update.message.from_user):
            in_place_string = 'Вы тоже отметились\nОтказаться: %s' % ('/' + place.id + '_leave')
        else:
            in_place_string = 'Вы пока не идёте\nПрисоединиться: %s' % ('/' + place.id + '_join')

        if attendants_string == '':
            attendants_string = 'Никого не будет'

        text = """<b>%s</b>
Сегодня здесь будут:
%s

<b>Всего: %s</b>
%s
Полный список: /stat
""" % (
            place.name,
            attendants_string,
            total,
            in_place_string
        )

        update.message.reply_html(text)
