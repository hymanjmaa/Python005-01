#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import time
import os
import pathlib
import logging


def record_call_time(log_file_fmt='/var/log'):
    call_time = datetime.utcnow().strftime('%y%m%d%H%M%S')
    file_path = (log_file_fmt + '/python-{}/{}.log').format(call_time, __name__)
    p = pathlib.Path(file_path)
    if not os.path.exists(p.parent):
        try:
            os.mkdir(p.parent)
        except PermissionError:
            print('no permission, please contact admin or replace log file dir')
            return
    logging.basicConfig(filename=file_path,
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.info('call timestamp: {}'.format(time.time()))


if __name__ == '__main__':
    record_call_time('/Users/hyman/py5/Python005-01/week01')
