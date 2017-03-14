import logging
import random
import wishful_upis as upis
import wishful_framework as wishful_module
import subprocess
from wishful_framework.classes import exceptions
import inspect
import fcntl, socket, struct
import netifaces as ni
from scapy.all import *
from datetime import date, datetime
import os

__author__ = "Domenico Garlisi, ..."
__copyright__ = "Copyright (c) 2017, CNIT"
__version__ = "0.1.0"
__email__ = "domenico.garlisi@cnit.it"

@wishful_module.build_module
class LteModule(wishful_module.AgentModule):
    def __init__(self):
        super(LteModule, self).__init__()
        self.log = logging.getLogger('lte_module.main')
        self.interface = "wlan0"
        self.wlan_interface = "wlan0"
        self.gain = 1
        self.power = 1


    # @wishful_module.bind_function(upis.radio.set_tx_power)
    # def set_tx_power(self, power_dBm):
	#
    #     self.log.info('setting set_power(): %s->%s' % (str(self.wlan_interface), str(power_dBm)))
	#
    #     cmd_str = 'iw dev ' + self.wlan_interface + ' set txpower fixed ' + str(power_dBm) + 'dbm'
	#
    #     try:
    #         [rcode, sout, serr] = self.run_command(cmd_str)
    #     except Exception as e:
    #         fname = inspect.currentframe().f_code.co_name
    #         self.log.fatal("An error occurred in %s: %s" % (fname, e))
    #         raise exceptions.UPIFunctionExecutionFailedException(func_name=fname, err_msg=str(e))
	#
    #     self.power = power_dBm
	#
	#
    # @wishful_module.bind_function(upis.radio.get_tx_power)
    # def get_tx_power(self):
    #     self.log.debug("WIFI Module gets power of interface: {}".format(self.interface))
    #     return self.power



    def run_command(self, command):
        '''
            Method to start the shell commands and get the output as iterater object
        '''

        sp = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = sp.communicate()

        if True:
            if out:
                self.log.debug("standard output of subprocess:")
                self.log.debug(out)
            if err:
                self.log.debug("standard error of subprocess:")
                self.log.debug(err)

        #if err:
        #    raise Exception("An error occurred in Dot80211Linux: %s" % err)

        return [sp.returncode, out.decode("utf-8"), err.decode("utf-8")]

    def run_timeout_command(self, command, timeout):
        """
            Call shell-command and either return its output or kill it
            if it doesn't normally exit within timeout seconds and return None
        """
        cmd = command.split(" ")
        start = datetime.datetime.now()
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while process.poll() is None:
            time.sleep(0.1)
            now = datetime.datetime.now()
            if (now - start).seconds > timeout:
                os.kill(process.pid, signal.SIGKILL)
                os.waitpid(-1, os.WNOHANG)
                return process.stdout.read()
        return process.stdout.read()