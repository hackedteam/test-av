import argparse
import sys
from time import sleep

from lib.config import Config
from lib.command import Command			

class PutFile:
	def __init__(self):
		self.config_file = "c:/test-av/conf/vmware.conf"
		self.conf = Config(self.config_file)
		self.cmd = Command(self.conf.path, self.conf.host, self.conf.user, self.conf.passwd)
		
		self.dst_dir = "c:/Users/avtest/Desktop"
		
		