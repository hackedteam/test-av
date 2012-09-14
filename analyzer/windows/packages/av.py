# Copyright (C) 2010-2012 Cuckoo Sandbox Developers.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import MySQLdb

from lib.core.config import Config
from lib.common.abstracts import Package
from lib.api.process import Process

class Av(Package):
    """EXE analysis package."""
    def get_task_id(self):
        conf = Config("c:\\cuckoo\\analysis.conf")
        return conf.task_id

    def start(self, path):
        # TODO: proper constructor for MySQL connection handler
        host   = "10.0.20.1"
        user   = "avtest"
        passwd = "avtest"
        dbname = "avtest"
        
        conn = MySQLdb.connect(host, user, passwd, dbname)
        cursor = conn.cursor()
        
        task_id = self.get_task_id()
        
        p  = Process()
                
        if "arguments" in self.options:
            x = p.execute(path=path, args=self.options["arguments"], suspended=False)
        else:
            x = p.execute(path=path, suspended=False)
        
        if x == True:
            cursor.execute("UPDATE tasks SET detected = %s WHERE task_id = %s",
                            (1, task_id))
        elif x == False:
            cursor.execute("UPDATE tasks SET detected = %s WHERE task_id = %s",
                            (2, task_id))
        else:
            return False
        
        return p.pid

    def check(self):
        return True
        
    def finish(self):
        return True
