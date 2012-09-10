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
        c = wmi.WMI()
        self.process_watcher = c.Win32_Process.watch_for("creation")
        p = Process()

        if "arguments" in self.options:
            x = p.execute(path=path, args=self.options["arguments"], suspended=True)
        else:
            x = p.execute(path=path, suspended=True)
        
        print "this is execution: %s" % x
        
        if not x:
            return False
            
        p.resume()

        return p.pid

    def check(self):
        proc = self.process_watcher()
        if proc:
            print proc.Caption
            return False
        return True
        
    def finish(self):
        return True
