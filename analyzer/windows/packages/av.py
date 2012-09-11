# Copyright (C) 2010-2012 Cuckoo Sandbox Developers.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.common.abstracts import Package
from lib.api.process import Process

import wmi
import os
import sqlite3

class Av(Package):
    """EXE analysis package."""

    def start(self, path):
        p  = Process()
        
        if "arguments" in self.options:
            x = p.execute(path=path, args=self.options["arguments"], suspended=False)
        else:
            x = p.execute(path=path, suspended=False)
        print "Write executon result on database. (%s)" % x
        f = open("C:\\Users\\avtest\\Documents\\results.txt", "wb")
        f.write(x)
        f.close()
        
        return p.pid

    def check(self):
        return True
        
    def finish(self):
        return True
