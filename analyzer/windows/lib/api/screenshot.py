# Copyright (C) 2010-2012 Cuckoo Sandbox Developers.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

try:
    import Image
    import ImageGrab
    import ImageChops
    HAVE_PIL = True
except:
    HAVE_PIL = False

class Screenshot:
    """Get screenshots."""

    def have_pil(self):
        """Is Python Image Library installed?
        @return: installed status.
        """
        return HAVE_PIL

    def equal(self, img1, img2):
        """Compares two screenshots.
        @param img1: screenshot to compare.
        @param img2: screenshot to compare.
        @return: equal status.
        """
        if not HAVE_PIL:
            return None

        return ImageChops.difference(img1, img2).getbbox() is None

    def take(self):
        """Take a screenshot.
        @return: screenshot or None.
        """
        if not HAVE_PIL:
            return None

        return ImageGrab.grab()



import subprocess, os
import hashlib
from time import sleep
from threading import Thread


class Screener(Thread):

    # path to save screens
    # path vmrun
    def __init__(self, vmrun):
        self.vmrun = vmrun
    
    def start(self, vm_path, username="", password="", shot_path=""):
        # creating a file .pid
        self.lock_file = '/tmp/lock.pid'
        if not os.path.exists(self.lock_file):
            lock = open(self.lock_file, 'w')
            lock.close()
        
        first = "%s/file1.png" % shot_path  
        self.proc = subprocess.Popen("%s -gu %s -gp %s captureScreen %s %s" % (self.vmrun, username, password, vm_path, first))
        first_hash = hashlib.md5(open(first, 'r').read()).digest()
        
        while True:
            
            if not os.path.exists(self.lock_file):
                print "stopping time"
                break
            
            # Take screenshot
            # TODO: 
            # username, password of guest account

            cur = "%s/file12.png" % shot_path  
            self.proc = subprocess.Popen("%s -gu %s -gp %s captureScreen %s %s" % (self.vmrun, username, password, vm_path, cur))
            # 2. md5 of file
            cur_hash = hashlib.md5(open(cur, 'r').read()).digest()

            # 3. if md5 current == previous delete file
            if cur_hash == first_hash:
                print "removing %s" % cur
                os.remove(cur)
            # 4. sleeping time
            sleep(1)


    def stop():
        if os.path.exists(self.lock_file):
            os.remove(self.lock_file)



