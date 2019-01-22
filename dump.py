# -*- coding: utf-8 -*-

# Standalone helper tool to dump WiresAccess.log.
# Usage: dump.py /path/to/WiresAccess.log

import sys
from wires_acc_file import wires_acc_file

acc_file = wires_acc_file(sys.argv[1])
for call in acc_file.calls:
    call.dump()
