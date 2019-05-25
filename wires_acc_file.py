# -*- coding: utf-8 -*-
import datetime

# Python module to proces WiresAccess.log file.
# Usage: create istance of wires_acc_file, pass path to file as parameter.
#        Access "calls" member (list) for individual log entries.
#        See "wires_log_entry" for accessible members.

# List compiled by Peter HB9DWW, maps radio id prefix to radio type
RADIO_TYPE_MAP = {
        'E0' : 'FT-1D',
        'E5' : 'FT-2D',
        'F0' : 'FTM-400D',
        'F5' : 'FTM-100D',
        'G0' : 'FT-991',
        'H5' : 'FT-70D',
        'R'  : 'repeater',
        }

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
        if self.location:
            location_tokens = self.location.split(' / ')
            if location_tokens[0].startswith('Lat:'):
                location_tokens[0] = location_tokens[0][4:]
            if location_tokens[1].startswith('Lon:'):
                location_tokens[1] = location_tokens[1][4:]
            location_tokens[0] = location_tokens[0][2:]+location_tokens[0][0]
            location_tokens[1] = location_tokens[1][2:]+location_tokens[1][0]
            self.position_pretty = location_tokens[0] + ' ' + location_tokens[1]

        self.radio = self.infer_radiotype()

    def infer_radiotype(self):
        for (prefix, radio_type) in RADIO_TYPE_MAP.items():
            if self.id.startswith(prefix): return radio_type

        if self.id.isdigit():
            number = int(self.id)
            if number >= 10000 and number < 20000 or \
               number >= 30000 and number < 40000 or \
               number >= 50000 and number < 60000:
                return 'node'
            if number >= 20000 and number < 30000 or \
               number >= 40000 and number < 50000 or \
               number >= 60000 and number < 70000:
                return 'room'
        return 'unknown'


    def get_timestamp_epoch(self):
        if self.timestamp == '0000/00/00 00:00:00':
            return 0.
        d = datetime.datetime.strptime(self.timestamp, '%Y/%m/%d %H:%M:%S')
        return d.timestamp()

    def dump(self):
        print('%s\n  ID: %s (%s)\n  Description: %s\n  Timestamp: %s\n  Activity: %s\n  Location: %s\n\n' %
                (self.call, self.id, self.radio, self.description, self.timestamp, self.activity, self.location ))

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


