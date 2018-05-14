# coding: utf8
import logging
from telegram.ext import Updater
from cskatebot.storage import Storage
from cskatebot.handler.admin import AdminHandler
from cskatebot.handler.any import AnyHandler
from cskatebot.handler.place import PlaceHandler

logger = logging.getLogger(__name__)

# HELP_MESSAGE = """Привет!
# Этот бот помогает собираться на площадке для игры в колдунчики.
# Для вывода этого сообщения напишите /start
#
# Сейчас доступны следующие площадки:
# %s
#
# За комментариями и улучшениями пишите @AndreyProskurnev
# """
#
#
# class PlaceHandler(Handler):
#
#     def __init__(self, storage, *args, **kwargs):
#         self.storage = storage
#
#     def check_update(self, update):
#         for place in self.storage.places.values():
#             if place.is_relative_text(update.message.text):
#                 return True
#         return False
#
#     def handle_update(self, update, dispatcher):
#         bot = dispatcher.bot  # noqa
#         place = None
#         for plc in self.storage.places.values():
#             if plc.is_relative_text(update.message.text):
#                 place = plc
#                 break
#
#         if place is None:
#             update.message.reply_text('Внутренняя ошибка, не смогли определить место')
#             return
#
#         action, info = place.detect_type_and_process_message(update.message.text)
#         if action == 'join':
#             place.set_attendant(update.message.from_user, info)
#             total = place.get_stats()
#             bot.send_message(
#                 chat_id=update.message.chat_id,
#                 text="<b>%s</b>\n\nСпасибо, что придёшь\n\nВсего отметилось: <b>%s</b>\n\nПосмотреть список: %s\nПолный список: /stat" % (
#                     place.name,
#                     total,
#                     '/' + place.id + '_list'
#                 ),
#                 parse_mode=telegram.ParseMode.HTML
#             )
#             return
#         elif action == 'leave':
#             place.set_attendant(update.message.from_user, 0)
#             total = place.get_stats()
#             bot.send_message(
#                 chat_id=update.message.chat_id,
#                 text="<b>%s</b>\n\nОчень жаль, нам будет тебя не хватать\n\nБез тебя останется <b>%s</b> человек.\n\nПосмотреть список: %s\nПрисоединиться: %s\nПолный список: /stat" % (
#                     place.name,
#                     total,
#                     '/' + place.id + '_list',
#                     '/' + place.id + '_join',
#                 ),
#                 parse_mode=telegram.ParseMode.HTML
#             )
#             return
#
#         total = place.get_stats()
#
#         attendants_string = '\n'.join([" %s +%s" % (v['name'], v['amount']) for v in place.attendants.values()])
#         in_place_string = ''
#         if place.is_attendant(update.message.from_user):
#             in_place_string = 'Вы тоже отметились\nОтказаться: %s' % ('/' + place.id + '_leave')
#         else:
#             in_place_string = 'Вы пока не идёте\nПрисоединиться: %s' % ('/' + place.id + '_join')
#
#         if attendants_string == '':
#             attendants_string = 'Никого не будет'
#
#         text = """<b>%s</b>
# Сегодня здесь будут:
# %s
#
# <b>Всего: %s</b>
# %s
# Полный список: /stat
# """ % (
#             place.name,
#             attendants_string,
#             total,
#             in_place_string
#         )
#
#         bot.send_message(
#             chat_id=update.message.chat_id,
#             text=text,
#             parse_mode=telegram.ParseMode.HTML,
#         )
#
#
# class AnyHandler(Handler):
#
#     def __init__(self, storage):
#         self.storage = storage
#
#     def check_update(self, update):
#         return True
#
#     def handle_update(self, update, dispatcher):
#         logger.info("got message: %s", update.message)
#         bot = dispatcher.bot
#
#         places_string = ''
#         ordered_places = []
#         for place in self.storage.places.values():
#             total = place.get_stats()
#             ordered_places.append([place, total])
#         ordered_places.sort(key=lambda x: -x[1])
#
#         for place, total in ordered_places:
#             join_or_leave = 'пойду: /%s_join' % (place.id)
#             if place.is_attendant(update.message.from_user):
#                 join_or_leave = 'не пойду: /%s_leave' % (place.id)
#             places_string += '<b>%s</b> %s\n%s\nподробнее: %s\n\n' % (
#                 place.name,
#                 total,
#                 join_or_leave,
#                 '/' + place.id + '_list',
#             )
#
#         text = HELP_MESSAGE % (places_string, )
#         if update.message.text.lower() in {'/stat', '/stats', 'stats'}:
#             text = "Список мест для катания\n" + places_string + '\nОбновить: /stat'
#
#         bot.send_message(
#             chat_id=update.message.chat_id,
#             text=text,
#             parse_mode=telegram.ParseMode.HTML,
#         )


def handle_error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def start_bot(config):
    storage = Storage()
    storage.load()

    updater = Updater(config['token'])

    dp = updater.dispatcher

    dp.add_handler(PlaceHandler(storage))
    dp.add_handler(AdminHandler(storage))
    dp.add_handler(AnyHandler(storage))

    dp.add_error_handler(handle_error)

    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
