# Copyright (C) 2010-2012 Cuckoo Sandbox Developers.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.common.abstracts import Package
from lib.api.process import Process

import wmi
import os

class Av(Package):
    """EXE analysis package."""

    def start(self, path):
        p = Process()
        
        print "Started analysis AV Package. Lets find EXE file"

        if "arguments" in self.options:
            x = p.execute(path=path, args=self.options["arguments"], suspended=False)
        else:
            x = p.execute(path=path, suspended=False)
        
        print "this is execution: %s" % x
        
        if x == False:
            return False

        #p.resume()

        return p.pid

    def check(self):
        return True
        
    def finish(self):
        return True
