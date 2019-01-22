# -*- coding: utf-8 -*-
import os
import sys
import datetime
import time
import logging
from wires_acc_file import wires_acc_file

# Version 0.2

logging.basicConfig(filename='wires_acc.log', level=logging.INFO, format='%(asctime)s %(message)s')
acc_file = wires_acc_file(sys.argv[1])
last_mtime = os.path.getmtime(sys.argv[1])
while True:
    try:
        if os.path.getmtime(sys.argv[1]) > last_mtime:
            print('Update: %s' % datetime.datetime.now())
            new_acc_file = wires_acc_file(sys.argv[1])
            for entry in new_acc_file.calls:
                if entry.get_timestamp_epoch() > acc_file.newest_entry_timestamp:
                    entry.dump()
                    print(entry.tokens)
                    logging.info('%s, %s, %s, %s, %s, %s' % (entry.call, entry.id, entry.description, entry.timestamp, entry.activity, entry.location))
            
            last_mtime = os.path.getmtime(sys.argv[1])
            acc_file = new_acc_file
    except FileNotFoundError:
        print('Error: File not found')
    time.sleep(1)
