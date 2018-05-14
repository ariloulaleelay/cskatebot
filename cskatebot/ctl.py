#!/usr/bin/env python

import cskatebot._init_logger  # noqa
import logging
import sys
from pyhocon import ConfigFactory
from cskatebot.bot import start_bot

logger = logging.getLogger(__name__)


def main():
    config = ConfigFactory.parse_file(sys.argv[1])
    start_bot(config)


if __name__ == '__main__':
    main()
