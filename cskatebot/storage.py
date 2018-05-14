# coding: utf8

import re
import os
import time
import logging
import json
import copy
import datetime

logger = logging.getLogger(__name__)


class Place(object):

    def __init__(self, id, name, description='', keywords=None):
        self.id = id
        self.name = name
        self.description = description
        self.attendants = {}
        self.keywords = set([id, name])
        if keywords is not None:
            for word in keywords:
                self.keywords.add(word)
        regexstr = r'^/?(%s)([\s\_\-\+].*|$)' % ('|'.join(self.keywords))
        self._is_relative_regex = re.compile(regexstr, re.IGNORECASE)

    def is_relative_text(self, text):
        logger.info("tesing %s against %s", text, self._is_relative_regex)
        return self._is_relative_regex.search(text) is not None

    def detect_type_and_process_message(self, text):
        m = self._is_relative_regex.search(text)
        if m is None:
            return 'error', None
        cmd = m.group(2)
        if cmd is None:
            cmd = ''
        if cmd == '_join':
            cmd = '+1'
        if cmd == '_leave':
            cmd = '-'
        cmd = re.sub(r'[^\+\-0-9]', '', cmd.lower())
        if cmd.startswith('+'):
            cmd = re.sub(r'\+', '', cmd)
            amount = 1
            if cmd != '':
                amount = int(cmd)
            return 'join', amount
        elif cmd.startswith('-'):
            cmd = re.sub(r'\-', '', cmd)
            amount = 1
            if cmd != '':
                amount = int(cmd)
            return 'leave', None

        return 'info', None

    def _cleanup_old_attendants(self):
        keys = list(self.attendants.keys())
        today = datetime.date.today()
        for key in keys:
            attendant = self.attendants[key]
            attendant_day = datetime.date.fromtimestamp(attendant['ts'])
            if attendant_day != today:
                logger.info("attendance %s too old %s != %s so delete it", attendant['name'], attendant_day, today)
                del self.attendants[key]

    def set_attendant(self, user, amount, timestamp=None):
        self._cleanup_old_attendants()
        if timestamp is None:
            timestamp = time.time()
        userid = str(user.id)
        if amount > 0:
            name = user.username
            if name is None:
                if user.first_name is not None and user.last_name is not None:
                    name = user.first_name + user.last_name
                else:
                    name = str(user.id)
            self.attendants[userid] = {
                'name': name,
                'amount': amount,
                'ts': timestamp
            }
        elif userid in self.attendants:
            del self.attendants[userid]

    def get_stats(self):
        self._cleanup_old_attendants()
        total = sum([v['amount'] for v in self.attendants.values()])
        return total

    def is_attendant(self, user):
        return str(user.id) in self.attendants

    def dump(self):
        return copy.deepcopy(self.attendants)
        result = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'keywords': copy.deepcopy(self.keywords),
            'attendants': copy.deepcopy(self.attendants),
        }
        return result

    def load(self, struct):
        self.attendants = copy.deepcopy(struct)


class Storage(object):

    def __init__(self, filename='storage.json'):
        places = [
            Place('luzhniki', 'Лужники', keywords=['лужники', 'лужа', 'luzha', 'luzhniki']),
            Place('vdnkh', 'Лосятник', keywords=['ввц', 'вднх', 'vvc', 'vdnkh', 'vdnh', 'cc', 'цц', 'лось', 'лосятник']),
            Place('poklonka', 'Поклонка', keywords=['пг', 'поклонка']),
            Place('sokolniki', 'Сокольники', keywords=['сокольники']),
        ]
        self.filename = filename
        self.places = {}
        for place in places:
            self.places[place.id] = place

    def get_place(self, key):
        return self.places.get(key, None)

    def dump(self):
        attendants = {}
        for key, place in self.places.items():
            attendants[key] = place.dump()
        result = {
            'attendants': attendants
        }
        with open(self.filename, 'wb') as fp:
            result_string = json.dumps(result, ensure_ascii=False, skipkeys=True).encode('utf8')
            fp.write(result_string)

    def load(self):
        data = None
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as fp:
                contents = fp.read().decode('utf8')
                if contents != '':
                    data = json.loads(contents)

        if data is None:
            return

        for place_key, place_data in data.get('attendants', {}).items():
            if place_key not in self.places:
                continue
            self.places[place_key].load(place_data)
