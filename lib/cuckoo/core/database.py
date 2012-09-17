# Copyright (C) 2010-2012 Cuckoo Sandbox Developers.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import os
import sys
import MySQLdb

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql.expression import desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey

from lib.cuckoo.common.constants import CUCKOO_ROOT
from lib.cuckoo.common.exceptions import CuckooDatabaseError, CuckooOperationalError
from lib.cuckoo.common.abstracts import Dictionary
from lib.cuckoo.common.utils import create_folder

# SQL Alchemy init time
engine = create_engine("mysql://avtest:avtest@10.0.20.1:3306/avtest")
Session = sessionmaker(bind=engine)
s = Session()
Base = declarative_base()

# Table Exe abstraction
class Exe(Base):

	__tablename__ = "exe"
	
	id = Column(Integer, primary_key=True)
	file_path = Column(Text)
	md5 = Column(Text)
	
	def __init__(self, file_path, md5):
		self.file_path = file_path
		self.md5 = md5
		
# Table Analysis abstraction
class Analysis(Base):
    
	__tablename__ = "analysis"
	
	id = Column(Integer, primary_key=True)
	desc = Column(Text)
	exe_id = Column('exe_id', Integer, ForeignKey('exe.id'))
	exe = relationship("Exe")
	created_on = Column(DateTime)
	completed_on = Column(DateTime)
	lock = Column(Integer)
	status = Column(Integer)
	
	def __init__(self, desc, exe_id):
		self.desc = desc
		self.exe_id = exe_id
		
# Table Tasks abstraction
class Task(Base):
	__tablename__ = "tasks"
	
	id = Column(Integer, primary_key=True)
	a_id = Column("anal_id", Integer, ForeignKey('analysis.id'))
	md5 = Column(Text)
	file_path = Column(Text)
	timeout = Column(Integer)
	priority = Column(Integer)
	custom = Column(Text)
	machine = Column(Text)
	package = Column(Text)
	options = Column(Text)
	platform = Column(Text)
	lock = Column(Integer)
	status = Column(Integer)
	detected = Column(Integer)

	def __init__(self,
	             file_path,
	             a_id,
	             md5,
	             timeout,
	             package,
	             options,
	             priority,
	             custom,
	             machine,
	             platform):
		self.a_id = a_id
		self.md5 = md5
		self.file_path = file_path
		self.timeout = timeout
		self.priority = priority
		self.custom = custom
		self.machine = machine
		self.package = package
		self.options = options
		self.platform = platform
		self.lock = 0
		self.status = 0
        

class Database:
    """Analysis queue database."""
     
    def generate(self):
        """Create database.
        @return: operation status.
        """
        conn = MySQLdb.connect("10.0.20.1", "avtest", "avtest", "avtest")
        cursor = conn.cursor()

        try:
            """We need 3 tables: Analysis, tasks and another one 
            needed for executables
            """
            cursor.execute("CREATE TABLE analysis ("                                \
                           "    `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,"  \
                           "    `desc` TEXT NULL,"                                  \
                           "    `exe_id` INTEGER NOT NULL,"                         \
                           "    `created_on` TIMESTAMP DEFAULT CURRENT_TIMESTAMP, " \
                           "    `completed_on` TIMESTAMP NULL, "                    \
                           "    `lock` INTEGER DEFAULT 0, "                         \
                           # Status possible values:
                           #   0 = not completed
                           #   1 = error occurred
                           #   2 = completed successfully.
                           "    `status` INTEGER DEFAULT 0"                         \
                           ");")
                           
            cursor.execute("CREATE TABLE exe ("                                     \
                            "   `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,"  \
                            "   `file_path` TEXT NOT NULL, "                        \
                            "   `md5` TEXT NULL "                                   \
                            ");")
            
            cursor.execute("CREATE TABLE tasks ( "                                  \
                           "    `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, " \
                           "    `anal_id` INTEGER NOT NULL, "                       \
                           "    `md5` TEXT NULL, "                                  \
                           "    `file_path` TEXT NOT NULL, "                        \
                           "    `timeout` INTEGER DEFAULT NULL, "                   \
                           "    `priority` INTEGER DEFAULT 0, "                     \
                           "    `custom` TEXT NULL, "                               \
                           "    `machine` TEXT NULL, "                              \
                           "    `package` TEXT NULL, "                              \
                           "    `options` TEXT NULL, "                              \
                           "    `platform` TEXT NULL, "                             \
                           "    `added_on` TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "   \
                           "    `completed_on` TIMESTAMP NULL, "                    \
                           "    `lock` INTEGER DEFAULT 0, "                         \
                           # Status possible values:
                           #   0 = not completed
                           #   1 = error occurred
                           #   2 = completed successfully.
                           "    `status` INTEGER DEFAULT 0, "                       \
                           # Detected possible values:
                           #   0 = not completed
                           #   1 = not detected (success)
                           #   2 = detected (fail!)
                           "    `detected` INTEGER DEFAULT 0 "                      \
                           ");")

        except MySQLdb.Error as e:
            raise CuckooDatabaseError("Unable to create database: %s" % e)

        return True
    
    def add(self,
            file_path,
            a_id,
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
            
        if not timeout:
            timeout = 0
            
        try:
            
            task = Task(file_path,
                        a_id,
                        md5,
                        timeout,
                        package,
                        options,
                        priority,
                        custom,
                        machine,
                        platform)
            
            s.add(task)
            s.commit()
            return task.id
        except MySQLdb.Error as e:
            raise CuckooDatabaseError("Unable to add task: %s" % e)
        
    def add_analysis(self, desc, exe_id):
        """ Add an analysis on database
        @param desc: description
        @param exe_id: id of executable to test
        @return: cursor or None
        """
        a = Analysis(desc, exe_id)
                    
        try:
            s.add(a)
            s.commit()
            return a.id
        except SQLAlchemyError as e:
            raise CuckooDatabaseError("Unable to create analysis: %s" % e)
    
    def add_exe(self, file_path, md5):
        """ Add an exe to db
        @param file_path: path to file
        @return: cursor or None
        """
        if not file_path or not os.path.exists(file_path):
            return None
        
        row = s.query(Exe).filter_by(md5=md5).first()
        
        if row is not None:
            return row.id
        try:
            exe = Exe(file_path, md5)
            s.add(exe)
            s.commit()
            return exe.id
        except SQLAlchemyError as e:
            raise CuckooDatabaseError("Unable to add executable, reason: %s" % e)

    def fetch(self):
        try:
            s = Session()
            task = s.query(Task).filter_by(lock=0, status=0).order_by(desc(Task.priority)).first()
            #print("fetching task %s" % task)
            s.close()
            return task
            
        except SQLAlchemyError as e:
            raise CuckooDatabaseError("Unable to fetch, reason: %s" % e)
        
    def lock(self, task_id):
        """Lock a task.
        @param task_id: task id.
        @return: operation status.
        """
        try:
            task = s.query(Task).filter_by(id=task_id).first()
        except SQLAlchemyError as e:
            raise CuckooDatabaseError("Unable to find lock, reason: %s" % e)
            
        if task:
            try:
                task.lock = 1
                s.commit()
            except SQLAlchemyError as e:
                raise CuckooDatabaseError("Unable to update lock, reason: %s" % e)
        else:
            return False
        return True

    def unlock(self, task_id):
        """Unlock a task.
        @param task_id: task id.
        @return: operation status.
        """
        try:
            task = s.query(Task).filter_by(id=task_id).first()
        except SQLAlchemyError as e:
            raise CuckooDatabaseError("Unable to find lock, reason: %s" % e)
        
        if row:
            try:
                task.lock = 0
                s.commit()
            except SQLAlchemyError as e:
                raise CuckooDatabaseError("Unable to unlock, reason: %s" % e)
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
            task = s.query(Task).filter_by(id=task_id).first()
        except SQLAlchemyError as e:
            raise CuckooDatabaseError("Unable to find locked task, reason: %s" % e)
        
        if task:
            if success:
                task.status = 2
            else:
                task.status = 1
                
            try:
                s.commit()
            except SQLAlchemyError as e:
                raise CuckooDatabaseError("Unable to complete, reason: %s" % e)
        else:
            return False
        return True

    def get_all_analysis(self):
        try:
            analysis = s.query(Analysis).order_by(desc(Analysis.status),desc(Analysis.created_on)).all()
            for b in analysis:
                print b.exe
            return analysis
        except SQLAlchemyError as e:
            raise CuckooDatabaseError("Unable to get all analysis, reason:" % e)
            
    
    def get_analysis(self, a_id):
        try:
            tasks = s.query(Analysis).filter_by(anal_id=a_id).all()
            return tasks
        except SQLAlchemyError as e:
            raise CuckooDatabaseError("Unable to get all tasks for analysis, reason: %s" % e)
            
    def get_task(self, task_id):
        try:
            task = s.query(Analysis).filter_by(task_id=task_id).first()
            return task
        except SQLAlchemyError as e:
            raise CuckooDatabaseError("Unable to get all tasks for analysis, reason: %s" % e)
        