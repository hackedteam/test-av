import subprocess
import configparser


'''
TODO:
 - find virtual machines
 - for each vm:
   * startup virtual machines
   * send cmd
   * delete current snapshot
   * save new snapshot as current
   * shutdown vm
'''

class Config:
    """ Manage a config file with vm
    """
    def __init__(self, filename):
        self.filename = filename
        self.config = ConfigParser.RawConfigParser()
        self.config.read(self.filename)

    def getVms(self):
        vms = self.config.get('vmware','machines')
        return vms

    def getVmxPath(self, vm):
        vmx = self.config.get(vm, 'label')
        return vmx


class Operator:
    """ Operator Class
    Sends primitive commands to vSphere via vmrun utility
    """
    
    def __init__(self, vmx):
        self.vmrunPath=""
        self.vsUrl="https://vcenter5.hackingteam.local/sdk"
        self.vsUser="avtest"
        self.vsPass="Av!123"
        self.vmUser="avtest"
        self.vmPass="avtest"
        self.vmx=vmx


	def start(self):
	    """Checking for interactive startup
	    """
		cmd = subprocess.Popen([self.vmrunPath,
								"-h", self.vsUrl,
								"-u", self.vsUser,
								"-p", self.vsPass,
								"start", self.vmx ])
		
	
	def stop(self, vm):
		cmd = subprocess.Popen([self.vmrunPath,
								"-h", self.vsUrl,
								"-u", self.vsUser,
								"-p", self.vsPass,
								"stop", self.vmx ])



    def delete(self, snapshot):
        cmd = subprocess.Popen([self.vmrunPath,
								"-h", self.vsUrl,
								"-u", self.vsUser,
								"-p", self.vsPass,
								"deleteSnapshot", self.vmx,
								snapshot ])
	
	
	def snapshot(self, snapshot):
        cmd = subprocess.Popen([self.vmrunPath,
    			                "-h", self.vsUrl,
    							"-u", self.vsUser,
    							"-p", self.vsPass,
    							"snapshot", self.vmx,
    					        snapshot ])
    
    
    def execute(self, script):
        cmd = subprocess.Popen([vmrunPath,
    			                "-h", self.vsUrl,
    							"-u", self.vsUser, "-p", self.vsPass,
    							"-gu", self.vmUser, "-gp", self.vmPass,
    							"runProgramInGuest", self.vmx,
    					        script ])
        



class Commander:    
    """
    Commander Class
    Sends operations to Operator for one Virtual Machine specified as input
    """
    
    def __init__(self, vm):
        self.vm = vm
        self.op = Operator(vm)
        
    def startVm(self):
        op.start()
        
    def stopVm(self):
        op.stop()
    
    def sendUpgrade(self, cmd):
        op.execute(cmd)

    def refreshSnapshot(self, snapshot):
        op.delete(snapshot)
        op.snapshot(snapshot)

        

if __name__ == "__main__":
    
    vmware_config_file=""
    cmd = ""
    snapshot="current"
    c = Config(vmware_config_file)
    vms = c.getVms()
    
    for vm in vms:
        cmd = Commander(c.getVmxPath(vm))
        
        sys.stdout.write("Starting Virtual Machine %s" % vm)
        cmd.startVm()
        
        sys.stdout.write("Starting Upgrade")
        cmd.sendUpgrade(cmd)
        
        sys.stdout.write("Refreshing Snapshot")
        cmd.refreshSnapshot(snapshot)
        
        sys.stdout.write("Stopping Virtual Machine %s" % vm)
        cmd.stopVm()
        
        sys.stdout.write("Done.")
    sys.stdout.write("End")    