# -*- coding: utf-8 -*-
import datetime

# Python module to proces WiresAccess.log file.
# Usage: create istance of wires_acc_file, pass path to file as parameter.
#        Access "calls" member (list) for individual log entries.
#        See "wires_log_entry" for accessible members.

class wires_log_entry:
    def __init__(self, tokens):
        self.tokens = tokens
        self.call = tokens[0]
        self.id = tokens[1]
        self.description = tokens[2]
        self.timestamp = tokens[3]
        self.activity = tokens[4]
        self.location = tokens[6]
        self.position_pretty = ''
        self.radio = 'unknown'
        if self.location:
            location_tokens = self.location.split(' / ')
            if location_tokens[0].startswith('Lat:'):
                location_tokens[0] = location_tokens[0][4:]
            if location_tokens[1].startswith('Lon:'):
                location_tokens[1] = location_tokens[1][4:]
            location_tokens[0] = location_tokens[0][2:]+location_tokens[0][0]
            location_tokens[1] = location_tokens[1][2:]+location_tokens[1][0]
            self.position_pretty = location_tokens[0] + ' ' + location_tokens[1]


    def get_timestamp_epoch(self):
        if self.timestamp == '0000/00/00 00:00:00':
            return 0.
        d = datetime.datetime.strptime(self.timestamp, '%Y/%m/%d %H:%M:%S')
        return d.timestamp()

    def dump(self):
        print('%s\n  ID: %s\n  Description: %s\n  Timestamp: %s\n  Activity: %s\n  Location: %s\n\n' %
                (self.call, self.id, self.description, self.timestamp, self.activity, self.location ))

class wires_acc_file:
    def __init__(self, path):
        with open(path, encoding='latin1') as fh:
            self.newest_entry_timestamp = 0
            self.calls = []
            for line in fh.readlines():
                tokens = line.rstrip('\n').split('%')
                # FIXME: Assert len(tokens) == 13
                entry = wires_log_entry(tokens)
                self.calls.append(entry)
                if entry.get_timestamp_epoch() > self.newest_entry_timestamp:
                    self.newest_entry_timestamp = entry.get_timestamp_epoch()


