# Copyright (C) 2010-2012 Cuckoo Sandbox Developers.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.common.abstracts import Package
from lib.api.process import Process

import wmi
import os

parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print parentdir
os.sys.path.insert(0,parentdir) 
from lib.cuckoo.core.database import Database

class Av(Package):
    """EXE analysis package."""

    def start(self, path):
        #db = Database()
        p  = Process()
        
        if "arguments" in self.options:
            x = p.execute(path=path, args=self.options["arguments"], suspended=False)
        else:
            x = p.execute(path=path, suspended=False)
        print "Write executon result on database. (%s)" % x
        return p.pid

    def check(self):
        return True
        
    def finish(self):
        return True
