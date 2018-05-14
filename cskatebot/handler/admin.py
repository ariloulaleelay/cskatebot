# coding: utf8
import os
import logging
import datetime
from telegram.ext import Handler

logger = logging.getLogger(__name__)


class AdminHandler(Handler):

    command_prefix = '/admin '

    def __init__(self, storage):
        self.start_time = datetime.datetime.now()
        self.storage = storage

    def check_update(self, update):
        return update.message.text.startswith(self.command_prefix)

    def handle_update(self, update, dispatcher):
        text = update.message.text

        if update.message.from_user.id not in {163176649}:
            update.message.reply_text('go away')
            return

        if not text.startswith(self.command_prefix):
            update.message.reply_text('something gone wrong\ncommand: %s' % (text, ))
            return

        command = text[len(self.command_prefix):]
        if command == 'save':
            self.storage.dump()
            update.message.reply_text('done')
        elif command == 'attendants':
            msg = ''
            for place in self.storage.places.values():
                msg += 'place: %s\n' % (place.name, )
                for k, v in place.attendants.items():
                    ts = datetime.datetime.fromtimestamp(v['ts'])
                    msg += '  %s %s %s %s\n' % (k, v['name'], v['amount'], ts.isoformat())
                msg += '\n'
            update.message.reply_text(msg)
        elif command == 'uptime':
            update.message.reply_text(str(datetime.datetime.now() - self.start_time))
        elif command == 'reboot':
            self.storage.dump()
            os._exit(0)
        elif command == 'help':
            update.message.reply_text('save attendants shutdown')
        else:
            update.message.reply_text('unknown command: %s' % (command, ))
