import subprocess, os
import hashlib, md5
import string, random
from time import sleep
from threading import Thread


class Screener(Thread):
    
    # path to save screens
    # path vmrun
    def __init__(self, vmrun, vm_path, username, password, shot_path):
        Thread.__init__(self)
        self.lock_file = None
        self.vmrun = vmrun
        self.vm_path = vm_path
        self.username = username
        self.password = password
        self.shot_path = shot_path
        
    #def do_start(self, vm_path, username, password, shot_path):
    def run(self):
        # creating a file .pid
        self.lock_file = '/tmp/lock.pid'
        if not os.path.exists(self.lock_file):
            lock = open(self.lock_file, 'w')
            lock.write("\n\n")
            lock.close()
        
        #first = "%s/%s.png" % (self.shot_path.replace(' ','\ '), "".join(random.sample(string.letters, 5)))
        if not os.path.exists(self.shot_path + "/shots"):
            os.mkdir(self.shot_path + "/shots")
        #first = u"%s/shots/%s.png" % (self.shot_path, "".random.sample(string.letters, 5))
        first = self.shot_path + "/shots/" + "".join(random.sample(string.letters, 5)) + ".png"
        self.proc = subprocess.Popen([self.vmrun,
                                    "-gu", "%s" % self.username,
                                    "-gp", "%s" % self.password,
                                    "captureScreen",
                                    self.vm_path,
                                    first])
        #first_hash = hashlib.md5(open(first.replace(" ", "\ "), 'r').read()).digest()
        #if os.path.exists(first):
        #    f = open(first, 'rb')
        #    first_hash = hashlib.md5(f.read()).digest()
        
        while True:
            
            if not os.path.exists(self.lock_file):
                print "stopping time"
                break
            
            # Take screenshot
            # TODO: 
            # username, password of guest account
            cur = self.shot_path + "/shots/" + "".join(random.sample(string.letters, 5)) + ".png"
            #print "saving to %s" % cur
            self.proc = subprocess.Popen([self.vmrun,
                                        "-gu", "%s" % self.username,
                                        "-gp", "%s" % self.password,
                                        "captureScreen",
                                        self.vm_path,
                                        cur])
            # 2. md5 of file
            #cur_hash = hashlib.md5(open(cur.replace(" ", "\ "), 'r').read()).digest()
            if os.path.exists(cur):
                f = open(cur, 'rb')
                cur_hash = hashlib.md5(f.read()).digest()
                #cur_hash = hashlib.md5(open(cur, 'rb').read()).digest()
            
            '''    
            # 3. if md5 current == previous delete file
            if cur_hash == first_hash:
                print "removing %s" % cur
                os.remove(cur)
            '''
            # 4. sleeping time
            sleep(1)
        print "cheerz....\n\n"
    
    
    def stop(self):
        if os.path.exists(self.lock_file):
            os.remove(self.lock_file)
            
    '''
    def run(self):
        print "calling do_start"
        self.do_start(self.vm_path, self.username, self.password, self.shot_path)
        print "end of thread"
    '''