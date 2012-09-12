#!/usr/bin/env python
# Copyright (C) 2010-2012 Cuckoo Sandbox Developers.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import os
import sys
import logging
import tempfile
import hashlib
import MySQLdb
from time import sleep
from mako.template import Template
from mako.lookup import TemplateLookup

logging.basicConfig()
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "../"))

from lib.cuckoo.core.database import Database
from lib.cuckoo.common.constants import CUCKOO_ROOT
from lib.bottle import route, run, static_file, redirect, request, HTTPError

# This directory will be created in $tmppath (see store_and_submit)
TMPSUBDIR = "cuckoo-web"
BUFSIZE = 1024

# Templates directory
lookup = TemplateLookup(directories=[os.path.join(CUCKOO_ROOT, "data", "html")],
                        output_encoding="utf-8",
                        encoding_errors="replace",
                        strict_undefined=False)

def store_and_submit_fileobj(fobj, filename, desc, package="", 
                            options="", timeout=0, priority=1, machines="", platform=""):
    # Do everything in tmppath/TMPSUBDIR
    tmppath = tempfile.gettempdir()
    targetpath = os.path.join(tmppath, TMPSUBDIR)
    if not os.path.exists(targetpath): os.mkdir(targetpath)

    # Upload will be stored in a tmpdir with the original name
    tmpdir = tempfile.mkdtemp(prefix="upload_", dir=targetpath)
    tmpf = open(os.path.join(tmpdir, filename), "wb")
    t = fobj.read(BUFSIZE)

    # While reading from client also compute md5hash
    md5h = hashlib.md5()
    while t:
        md5h.update(t)
        tmpf.write(t)
        t = fobj.read(BUFSIZE)

    tmpf.close()

    # Submit task to cuckoo db
    db = Database()
    # Create executable record if needed
    exe_id = db.add_exe(file_path=tmpf.name,
                        md5=md5h.hexdigest())
    print("EXE ID: %s" % str(exe_id))
    # Create analysis record
    anal_id = db.add_analysis(desc, exe_id[0])
    print("ANAL ID: %s" % anal_id)
    
    for machine in machines.split(","):
        task_id = db.add(file_path=tmpf.name,
                         anal_id=anal_id[0],
                         md5=md5h.hexdigest(),
                         package=package,
                         timeout=timeout,
                         options=options,
                         priority=priority,
                         machine=machine,
                         platform=platform)
        sleep(3)
        print("TASK ID: %s" % task_id)
        
    return anal_id

@route("/")
def index():
    context = {}
    template = lookup.get_template("submit.html")
    return template.render(**context)

@route("/browse")
def browse():
    db = Database()
    context = {}

    try:
        db.cursor.execute("SELECT * FROM tasks " \
                          "ORDER BY status, added_on DESC;")
    except MySQLdb.Error as e:
        context["error"] = "Could not load tasks from database."
        return template.render(**context)

    rows = db.cursor.fetchall()
    template = lookup.get_template("browse.html")
    context["cuckoo_root"] = CUCKOO_ROOT

    return template.render(os=os, rows=rows, **context)

#
@route("/analysis")
def analysis():
    db = Database()
    context = {}

    try:
        db.cursor.execute("SELECT * FROM analysis " \
                          "ORDER BY status, created_on DESC;")
    except MySQLdb.Error as e:
        context["error"] = "Could not load tasks from database."
        return template.render(**context)

    rows = db.cursor.fetchall()
    for row in rows:
        db.cursor.execute("SELECT * FROM exe " \
                          "WHERE id = ?;", (row.exe_id,))
        exe = db.cursor.fetchone()
        row.update({"file_path":exe.file_path})
        
    template = lookup.get_template("analysis.html")
    context["cuckoo_root"] = CUCKOO_ROOT
    return template.render(os=os, rows=rows, **context)

@route("/analysis/view/<anal_id>")
def analysis_view(anal_id):    
    db = Database()
    context = {}
    
    try:
        db.cursor.execute("SELECT * FROM tasks " \
                          "WHERE anal_id = ?;", (anal_id,))
    except MySQLdb.Error as e:
        context["error"] = "Could not load analysis from database"
        return template.render(**context)
    
    rows = db.cursor.fetchall()
    template = lookup.get_template("browse.html")
    context["cuckoo_root"] = CUCKOO_ROOT
    return template.render(os=os, rows=rows, **context)


@route("/static/<filename:path>")
def server_static(filename):
    return static_file(filename, root=os.path.join(CUCKOO_ROOT, "data", "html"))

# Handle upload form
@route("/submit", method="POST")
def submit():
    context = {}
    errors = False

    # Optional, can be empty
    desc     = request.forms.get("desc", "")
    package  = request.forms.get("package", "")
    options  = request.forms.get("options", "")
    machines = request.forms.get("machines", "")
    priority = request.forms.get("priority", 1)
    timeout  = request.forms.get("timeout", "")
    data = request.files.file

    # Convert priority
    try:
        priority = int(priority)
    except:
        context["error_toggle"] = True
        context["error_priority"] = "Needs to be a number"
        errors = True

    # File mandatory
    if data == None or data == "":
        context["error_toggle"] = True
        context["error_file"] = "Mandatory"
        errors = True

    # On errors, tell user
    if errors:
        template = lookup.get_template("submit.html")
        return template.render(timeout=timeout, priority=priority, options=options, package=package, **context)
    
    # Finally real store and submit
    analid = store_and_submit_fileobj(data.file, data.filename, desc=desc, 
                                    timeout=timeout, priority=priority, options=options, 
                                    machines=machines, package=package)
    # Show result
    template = lookup.get_template("success.html")
    return template.render(analid=analid, submitfile=data.filename)

# Find an HTML report and render it
@route("/view/<task_id>")
def view(task_id):
    # Check if the specified task ID is valid
    if not task_id.isdigit():
        return HTTPError(code=404, output="The specified ID is invalid")

    report_path = os.path.join(CUCKOO_ROOT, "storage", "analyses", task_id, "reports", "report.html")

    # Check if the HTML report exists
    if not os.path.exists(report_path):
        return HTTPError(code=404, output="Report not found")

    # Return content of the HTML report
    return open(report_path, "rb").read()

if __name__ == "__main__":
    run(host="0.0.0.0", port=8080, debug=True, reloader=True)