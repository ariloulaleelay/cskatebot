# coding: utf8

import logging
from telegram.ext import Handler
from .base import HELP_MESSAGE

logger = logging.getLogger(__name__)


class AnyHandler(Handler):

    def __init__(self, storage):
        self.storage = storage

    def check_update(self, update):
        return True

    def handle_update(self, update, dispatcher):
        logger.info("got message: %s", update.message)

        places_string = ''
        ordered_places = []
        for place in self.storage.places.values():
            total = place.get_stats()
            ordered_places.append([place, total])
        ordered_places.sort(key=lambda x: -x[1])

        for place, total in ordered_places:
            join_or_leave = 'пойду: /%s_join' % (place.id)
            if place.is_attendant(update.message.from_user):
                join_or_leave = 'не пойду: /%s_leave' % (place.id)
            places_string += '<b>%s</b> %s\n%s\nподробнее: %s\n\n' % (
                place.name,
                total,
                join_or_leave,
                '/' + place.id + '_list',
            )

        text = HELP_MESSAGE % (places_string, )
        if update.message.text.lower() in {'/stat', '/stats', 'stats'}:
            text = "Список мест для катания\n" + places_string + '\nОбновить: /stat'

        update.message.reply_html(text)
