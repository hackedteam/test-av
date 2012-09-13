# Copyright (C) 2010-2012 Cuckoo Sandbox Developers.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import os
import sys
import MySQLdb

from lib.cuckoo.common.constants import CUCKOO_ROOT
from lib.cuckoo.common.exceptions import CuckooDatabaseError, CuckooOperationalError
from lib.cuckoo.common.abstracts import Dictionary
from lib.cuckoo.common.utils import create_folder

# From http://docs.python.org/library/sqlite3.html
def dict_factory(cursor, row):
    d = Dictionary()
    for idx, col in enumerate(cursor.description):
        setattr(d, col[0], row[idx])
    return d

class Database:
    """Analysis queue database."""

    def __init__(self):
        """@param db_file: database file path."""
        self.hostname = "10.0.20.1"
        self.username = "avtest"
        self.password = "avtest"
        self.dbname   = "avtest"
        #self.generate()
        self.conn = MySQLdb.connect(self.hostname, self.username, self.password, self.dbname)
        self.conn.row_factory = dict_factory
        self.cursor = self.conn.cursor()
     
    def generate(self):
        """Create database.
        @return: operation status.
        """
        conn = MySQLdb.connect(self.hostname, self.username, self.password, self.dbname)
        cursor = conn.cursor()

        try:
            """We need 3 tables: Analysis, tasks and another one 
            needed for executables
            """
            cursor.execute("CREATE TABLE analysis ("                            \
                           "    `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,"    \
                           "    `desc` TEXT NULL,"                            \
                           "    `exe_id` INTEGER NOT NULL,"                           \
                           "    `created_on` TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "        \
                           "    `completed_on` TIMESTAMP NULL, "                   \
                           "    `lock` INTEGER DEFAULT 0, "                           \
                           # Status possible values:
                           #   0 = not completed
                           #   1 = error occurred
                           #   2 = completed successfully.
                           "`status` INTEGER DEFAULT 0"                           \
                           ");")
                           
            cursor.execute("CREATE TABLE exe ("                             \
                            "   `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,"    \
                            "   `file_path` TEXT NOT NULL, "                 \
                            "   `md5` TEXT NULL "                   \
                            ");")
            
            cursor.execute("CREATE TABLE tasks ( "                         \
                           "    `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, "                  \
                           "    `anal_id` INTEGER NOT NULL, "                \
                           "    `md5` TEXT NULL, "                   \
                           "    `file_path` TEXT NOT NULL, "                 \
                           "    `timeout` INTEGER DEFAULT NULL, "            \
                           "    `priority` INTEGER DEFAULT 0, "              \
                           "    `custom` TEXT NULL, "                \
                           "    `machine` TEXT NULL, "               \
                           "    `package` TEXT NULL, "               \
                           "    `options` TEXT NULL, "               \
                           "    `platform` TEXT NULL, "              \
                           "    `added_on` TIMESTAMP DEFAULT CURRENT_TIMESTAMP, " \
                           "    `completed_on` TIMESTAMP NULL, "          \
                           "    `lock` INTEGER DEFAULT 0, "                  \
                           # Status possible values:
                           #   0 = not completed
                           #   1 = error occurred
                           #   2 = completed successfully.
                           "    `status` INTEGER DEFAULT 0, "                 \
                           # Detected possible values:
                           #   0 = not completed
                           #   1 = not detected (success)
                           #   2 = detected (fail!)
                           "    `detected` INTEGER DEFAULT 0 "                \
                           ");")

        except MySQLdb.Error as e:
            raise CuckooDatabaseError("Unable to create database: %s" % e)

        return True
    
    def add(self,
            file_path,
            anal_id,
            md5="",
            timeout=0,
            package="",
            options="",
            priority=1,
            custom="",
            machine="",
            platform=""):
        """Add a task to database.
        @param file_path: sample path.
        @param anal_id: analysis id referenced to table.
        @param md5: sample MD5.
        @param timeout: selected timeout.
        @param options: analysis options.
        @param priority: analysis priority.
        @param custom: custom options.
        @param machine: selected machine.
        @param platform: platform
        @return: cursor or None.
        """
        if not file_path or not os.path.exists(file_path):
            return None

        try:
            print(file_path, anal_id, md5,timeout, package, options, priority, custom, machine, platform)
            self.cursor.execute(
                "INSERT INTO tasks " \
                "(`file_path`, `anal_id`, `md5`, `timeout`, `package`, `options`, `priority`, `custom`, `machine`, `platform`) " \
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (file_path, anal_id, md5, timeout, package, options, 
                                                           priority, custom, machine, platform))
            self.conn.commit()
            return self.cursor.lastrowid
        except MySQLdb.Error as e:
            raise CuckooDatabaseError("Unable to add task: %s" % e)

    def add_analysis(self, desc, exe_id):
        """ Add an analysis on database
        @param desc: description
        @param exe_id: id of executable to test
        @return: cursor or None
        """             
        if not exe_id:
            return None
        
        try:
            self.cursor.execute("INSERT INTO analysis (`desc`, `exe_id`) VALUES (?, ?);", (desc, exe_id))
            self.conn.commit()
            print "Last Row ID: %s" % str(self.cursor.lastrowid)
            return self.cursor.lastrowid
        except MySQLdb.Error as e:
            raise CuckooDatabaseError("Unable to create analysis: %s" % e)

    def add_exe(self, file_path, md5):
        """ Add an exe to db
        @param file_path: path to file
        @return: cursor or None
        """
        if not file_path or not os.path.exists(file_path):
            return None
            
        # check if md5 is present on db
        self.cursor.execute("SELECT id FROM exe WHERE `md5` = '%s';" % md5)
        id = self.cursor.fetchone()
        if row is not None:
            return int(id)
            
        try:
            self.cursor.execute("INSERT INTO exe (`file_path`, `md5`) " \
                                "VALUES (?, ?);", (file_path, md5))
            self.conn.commit()
            return int(self.cursor.lastrowid)
        except MySQLdb.Error as e:
            raise CuckooDatabaseError("Unable to add executable: %s" % e)
            
    def fetch(self):
        """Fetch a task.
        @return: task dict or None.
        """
        try:
            self.cursor.execute("SELECT * FROM tasks " \
                                "WHERE `lock` = 0 "      \
                                "AND `status` = 0 "      \
                                "ORDER BY `priority` DESC, `added_on` LIMIT 1;")
        except MySQLdb.Error as e:
            raise CuckooDatabaseError("Unable to fetch: %s" % e)

        row = self.cursor.fetchone()

        return row

    def lock(self, task_id):
        """Lock a task.
        @param task_id: task id.
        @return: operation status.
        """
        try:
            self.cursor.execute("SELECT id FROM tasks WHERE `id` = %s;" % task_id)
            row = self.cursor.fetchone()
        except MySQLdb.Error as e:
            raise CuckooDatabaseError("Unable to create database: %s" % e)

        if row:
            try:
                self.cursor.execute("UPDATE tasks SET `lock` = 1 WHERE `id` = %s;" % task_id)
                self.conn.commit()
            except MySQLdb.Error as e:
                raise CuckooDatabaseError("Unable to lock: %s" % e)
        else:
            return False

        return True

    def unlock(self, task_id):
        """Unlock a task.
        @param task_id: task id.
        @return: operation status.
        """
        try:
            self.cursor.execute("SELECT id FROM tasks WHERE `id` = %s;" % task_id)
            row = self.cursor.fetchone()
        except MySQLdb.Error as e:
            raise CuckooDatabaseError("Unable to create database: %s" % e)

        if row:
            try:
                self.cursor.execute("UPDATE tasks SET `lock` = 0 WHERE `id` = %s;" % task_id)
                self.conn.commit()
            except MySQLdb.Error as e:
                raise CuckooDatabaseError("Unable to unlock: %s" % e)
        else:
            return False

        return True

    def complete(self, task_id, success=True):
        """Mark a task as completed.
        @param task_id: task id.
        @param success: completed with status.
        @return: operation status.
        """
        try:
            self.cursor.execute("SELECT id FROM tasks WHERE `id` = %s;" % task_id)
            row = self.cursor.fetchone()
        except MySQLdb.Error as e:
            raise CuckooDatabaseError("Unable to create database: %s" % e)

        if row:
            if success:
                status = 2
            else:
                status = 1

            try:
                self.cursor.execute("UPDATE tasks SET `lock` = 0, "     \
                                    "`status` = %s, "                    \
                                    "`completed_on` = DATETIME('now') " \
                                    "WHERE `id` = %s;" % (status, task_id))
                self.conn.commit()
            except MySQLdb.Error as e:
                raise CuckooDatabaseError("Unable to complete: %s" % e)
        else:
            return False

        return True
