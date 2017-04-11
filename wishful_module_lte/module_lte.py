import logging
import wishful_framework as wishful_module
import subprocess
from scapy.all import *
from datetime import date, datetime
import os
from wishful_upis.meta_models import Attribute, Measurement, Event, Action, ValueDoc
from os import remove
from shutil import move
import sys
import functional_split

__author__ = "Domenico Garlisi, ..."
__copyright__ = "Copyright (c) 2017, CNIT"
__version__ = "0.1.0"
__email__ = "domenico.garlisi@cnit.it"

# ATTRIBUTES of NET_UPI
MME_REALM = Attribute(key='MME_REALM', type=int, isReadOnly=False)  #:
MME_SERVED_ENB = Attribute(key='MME_SERVED_ENB', type=int, isReadOnly=False)  #:
MME_SERVED_UE = Attribute(key='MME_SERVED_UE', type=int, isReadOnly=False)  #:
MME_TAI_LIST = Attribute(key='MME_TAI_LIST', type=int, isReadOnly=False)  #:
MME_GUMMEI_LIST = Attribute(key='MME_GUMMEI_LIST', type=int, isReadOnly=False)  #:

ENB_NAME = Attribute(key='ENB_NAME', type=int, isReadOnly=False)  #:
ENB_ID = Attribute(key='ENB_ID', type=int, isReadOnly=False)  #:
ENB_CELL_TYPE = Attribute(key='ENB_CELL_TYPE', type=int, isReadOnly=False)  #:
ENB_TRACKING_AREA_CODE = Attribute(key='ENB_TRACKING_AREA_CODE', type=int, isReadOnly=False)  #:
ENB_MCC = Attribute(key='ENB_MCC', type=int, isReadOnly=False)  #:
ENB_MNC = Attribute(key='ENB_MNC', type=int, isReadOnly=False)  #:

RRU_NAME = Attribute(key='RRU_NAME', type=int, isReadOnly=False)  #:
RRU_ID = Attribute(key='RRU_ID', type=int, isReadOnly=False)  #:
RRU_CELL_TYPE = Attribute(key='ENB_CELL_TYPE', type=int, isReadOnly=False)  #:
RRU_TRACKING_AREA_CODE = Attribute(key='ENB_TRACKING_AREA_CODE', type=int, isReadOnly=False)  #:
RRU_MCC = Attribute(key='ENB_MCC', type=int, isReadOnly=False)  #:
RRU_MNC = Attribute(key='ENB_MNC', type=int, isReadOnly=False)  #:

RCC_NAME = Attribute(key='RRC_NAME', type=int, isReadOnly=False)  #:
RCC_ID = Attribute(key='RRC_ID', type=int, isReadOnly=False)  #:
RCC_CELL_TYPE = Attribute(key='ENB_CELL_TYPE', type=int, isReadOnly=False)  #:
RCC_TRACKING_AREA_CODE = Attribute(key='ENB_TRACKING_AREA_CODE', type=int, isReadOnly=False)  #:
RCC_MCC = Attribute(key='ENB_MCC', type=int, isReadOnly=False)  #:
RCC_MNC = Attribute(key='ENB_MNC', type=int, isReadOnly=False)  #:

SPLIT_LEVEL = Attribute(key='SPLIT_LEVEL', type=int, isReadOnly=False)  #:
FRONTHAUL_TRANSPORT_MODE = Attribute(key='FRONTHAUL_TRANSPORT_MODE', type=int, isReadOnly=False)  #:

mme_S1_name = Attribute(key='mme_S1_name', type=int, isReadOnly=False)  #:
mme_S1_addr = Attribute(key='mme_S1_addr', type=int, isReadOnly=False)  #:
mme_S11_name = Attribute(key='mme_S11_name', type=int, isReadOnly=False)  #:
mme_S11_addr = Attribute(key='mme_S11_addr', type=int, isReadOnly=False)  #:
mme_S11_port = Attribute(key='mme_S11_port', type=int, isReadOnly=False)  #:

sgw_S1U_S12_S4_name = Attribute(key='sgw_S1U_S12_S4_name', type=int, isReadOnly=False)  #:
sgw_S1U_S12_S4_addr = Attribute(key='sgw_S1U_S12_S4_addr', type=int, isReadOnly=False)  #:
sgw_S1U_S12_S4_port = Attribute(key='sgw_S1U_S12_S4_port', type=int, isReadOnly=False)  #:
sgw_S5_S8_name = Attribute(key='sgw_S5_S8_name', type=int, isReadOnly=False)  #:
sgw_S5_S8_addr = Attribute(key='sgw_S5_S8_addr', type=int, isReadOnly=False)  #:

pgw_S5_S8_name = Attribute(key='pgw_S5_S8_name_PGW', type=int, isReadOnly=False)  #:
pgw_SGi_name = Attribute(key='pgw_SGi_name', type=int, isReadOnly=False)  #:

ip_address_pool = Attribute(key='ip_address_pool', type=int, isReadOnly=False)  #:
default_DNS_addr = Attribute(key='default_DNS_addr', type=int, isReadOnly=False)  #:

enb_mme_addr = Attribute(key='enb_mme_addr', type=int, isReadOnly=False)  #:
enb_S1_name = Attribute(key='enb_S1_name', type=int, isReadOnly=False)  #:
enb_S1_addr = Attribute(key='enb_S1_addr', type=int, isReadOnly=False)  #:
enb_S1U_name = Attribute(key='enb_S1U_name', type=int, isReadOnly=False)  #:
enb_S1U_addr = Attribute(key='enb_S1U_addr', type=int, isReadOnly=False)  #:
enb_S1U_port = Attribute(key='enb_S1U_port', type=int, isReadOnly=False)  #:

rru_local_if_name = Attribute(key='rru_local_if_name', type=int, isReadOnly=False)  #:
rru_local_address = Attribute(key='rru_local_address', type=int, isReadOnly=False)  #:
rru_local_port = Attribute(key='rru_local_port', type=int, isReadOnly=False)  #:
rru_remote_address = Attribute(key='rru_remote_address', type=int, isReadOnly=False)  #:
rru_remote_port = Attribute(key='rru_remote_port', type=int, isReadOnly=False)  #:

rcc_mme_addr = Attribute(key='rcc_mme_addr', type=int, isReadOnly=False)  #:
rcc_S1_name = Attribute(key='rcc_S1_name', type=int, isReadOnly=False)  #:
rcc_S1_addr = Attribute(key='rcc_S1_addr', type=int, isReadOnly=False)  #:
rcc_S1U_name = Attribute(key='rcc_S1U_name', type=int, isReadOnly=False)  #:
rcc_S1U_addr = Attribute(key='rcc_S1U_addr', type=int, isReadOnly=False)  #:
rcc_S1U_port = Attribute(key='rcc_S1U_port', type=int, isReadOnly=False)  #:
rcc_local_if_name = Attribute(key='rcc_local_if_name', type=int, isReadOnly=False)  #:
rcc_local_address = Attribute(key='rcc_local_address', type=int, isReadOnly=False)  #:
rcc_local_port = Attribute(key='rcc_local_port', type=int, isReadOnly=False)  #:
rcc_remote_address = Attribute(key='rcc_remote_address', type=int, isReadOnly=False)  #:
rcc_remote_port = Attribute(key='rcc_remote_port', type=int, isReadOnly=False)  #:  # ATTRIBUTES

# ATTRIBUTES of NET_UPI
PUCCH_nom = Attribute(key='PUCCH_nom', type=int, isReadOnly=False)  #:
PUSCH_nom = Attribute(key='PUSCH_nom', type=int, isReadOnly=False)  #:
RX_GAIN = Attribute(key='RX_GAIN', type=int, isReadOnly=False)  #:
TX_GAIN = Attribute(key='TX_GAIN', type=int, isReadOnly=False)  #:
TX_BANDWIDTH = Attribute(key='TX_BANDWIDTH', type=int, isReadOnly=False)  #:
TX_CHANNEL = Attribute(key='TX_CHANNEL', type=int, isReadOnly=False)  #:
TX_MODE = Attribute(key='TX_MODE', type=int, isReadOnly=False)  #:
UL_FREQ_OFFSET = Attribute(key='UL_FREQ_OFFSET', type=int, isReadOnly=False)  #:

my_path_enb = "/home/wishful/openairinterface5g/targets/PROJECTS/GENERIC-LTE-EPC/CONF/"
my_path_epc = "/usr/local/etc/oai/"

MME_CONF_FILENAME = "/usr/local/etc/oai/mme.conf"
SPGW_CONF_FILENAME = "/usr/local/etc/oai/spgw.conf"
ENB_CONF_FILENAME = "/home/wishful/openairinterface5g/targets/PROJECTS/GENERIC-LTE-EPC/CONF/enb.band7.tm1.usrpb210.conf"
RRU_IF4p5_CONF_FILENAME = "/home/wishful/openairinterface5g/targets/PROJECTS/GENERIC-LTE-EPC/CONF/rru.band7.tm1.if4p5.usrpb210.conf"
RRU_IF5_CONF_FILENAME = "/home/wishful/openairinterface5g/targets/PROJECTS/GENERIC-LTE-EPC/CONF/rru.band7.tm1.if5.usrpb210.conf"
RCC_IF4p5_CONF_FILENAME = "/home/wishful/openairinterface5g/targets/PROJECTS/GENERIC-LTE-EPC/CONF/rcc.band7.tm1.if4p5.usrpb210.conf"
RCC_IF5_CONF_FILENAME = "/home/wishful/openairinterface5g/targets/PROJECTS/GENERIC-LTE-EPC/CONF/rcc.band7.tm1.if5.usrpb210.conf"

# Dictionary for the matching the value to the relative SET/GET functions of NET_UPI
param_key_functions_dict = {
    'MME_REALM': {'set': set_mme_realm, 'get': get_mme_realm},
    'MME_SERVED_ENB': {'set': set_mme_served_enb, 'get': get_mme_served_enb},
    'MME_SERVED_UE': {'set': set_mme_served_ue, 'get': get_mme_served_ue},
    'MME_TAI_LIST': {'set': set_mme_tai_list, 'get': get_mme_tai_list},
    'MME_GUMMEI_LIST': {'set': set_mme_gummei_list, 'get': get_mme_gummei_list},
    'ENB_NAME': {'set'set_enb_name: 'get':get_enb_name},
    'ENB_ID': {'set': set_enb_id, 'get': get_enb_id},
    'ENB_CELL_TYPE': {'set': set_enb_cell_type, 'get': get_enb_cell_type},
    'ENB_TRACKING_AREA_CODE': {'set': set_enb_tracking_area_code, 'get': get_enb_tracking_area_code},
    'ENB_MCC': {'set': set_enb_mcc, 'get': get_enb_mcc},
    'ENB_MNC': {'set': set_enb_mnc, 'get': get_enb_mnc},
    'RRU_NAME': {'set': set_rru_name, 'get': get_rru_name},
    'RRU_ID': {'set': set_rru_id, 'get': get_rru_id},
    'RRU_CELL_TYPE': {'set': set_rru_cell_type, 'get': get_rru_cell_type},
    'RRU_TRACKING_AREA_CODE': {'set': set_rru_tracking_area_code, 'get': get_rru_tracking_area_code},
    'RRU_MCC': {'set': set_rru_mcc, 'get': get_rru_mcc},
    'RRU_MNC': {'set': set_rru_mnc, 'get': get_rru_mnc},
    'RCC_NAME': {'set': set_rcc_name, 'get': get_rcc_name},
    'RCC_ID': {'set': set_rcc_id, 'get': get_rcc_id},
    'RCC_CELL_TYPE': {'set': set_rcc_cell_type, 'get': get_rcc_cell_type},
    'RCC_TRACKING_AREA_CODE': {'set': set_rcc_tracking_area_code, 'get': get_rcc_tracking_area_code},
    'RCC_MCC': {'set': set_rcc_mcc, 'get': get_rcc_mcc},
    'SPLIT_LEVEL': {'set': Functional_split.set_split_level, 'get': Functional_split.get_split_level},
    'FRONTHAUL_TRANSPORT_MODE': {'set': set_fronthaul_transport_mode, 'get': get_fronthaul_transport_mode},
    'mme_S1_name': {'set': set_mme_name_s1, 'get': get_mme_name_s1},
    'mme_S1_addr': {'set': set_mme_addr_s1, 'get': get_mme_addr_s1},
    'mme_S11_name': {'set': set_mme_name_s11, 'get': get_mme_name_s11},
    'mme_S11_addr': {'set': set_mme_addr_s11, 'get': get_mme_addr_s11},
    'mme_S11_port': {'set': set_mme_port_s11, 'get': get_mme_port_s11},
    'sgw_S11_name': {'set': set_sgw_name_s11, 'get': get_sgw_name_s11},
    'sgw_S11_addr': {'set': set_sgw_addr_s11, 'get': get_sgw_addr_s11},
    'sgw_S1U_S12_S4_name': {'set': set_sgw_name_s1u_s12_s4,'get': get_sgw_name_s1u_s12_s4},
    'sgw_S1U_S12_S4_addr': {'set': set_sgw_addr_s1u_s12_s4,'get': get_sgw_addr_s1u_s12_s4},
    'sgw_S1U_S12_S4_port': {'set': set_sgw_port_s1u_s12_s4, 'get': get_sgw_port_s1u_s12_s4},
    'sgw_S5_S8_name': {'set': set_sgw_name_s5_s8, 'get': get_sgw_name_s5_s8},
    'sgw_S5_S8_addr': {'set': set_sgw_addr_s5_s8, 'get': get_sgw_addr_s5_s8},
    'pgw_S5_S8_name': {'set': set_pgw_name_s5_s8, 'get': get_pgw_name_s5_s8},
    'pgw_SGi_name': {'set': set_pgw_name_sgi, 'get': get_pgw_name_sgi},
    'ip_address_pool': {'set': set_ue_ip_addr_pool, 'get': get_ue_ip_addr_pool},
    'default_DNS_addr': {'set': set_default_dns_addr,'get': get_default_dns_addr},
    'enb_mme_ip_addr': {'set': set_enb_mme_ip_addr, 'get': get_enb_mme_ip_addr},
    'enb_name_s1': {'set': set_enb_name_s1, 'get': get_enb_name_s1},
    'enb_s1_addr': {'set': set_enb_addr_s1, 'get': get_enb_addr_s1},
    'enb_name_s1u': {'set': set_enb_name_s1u, 'get': get_enb_name_s1u},
    'enb_addr_s1u': {'set': set_enb_addr_s1u, 'get': get_enb_addr_s1u},
    'enb_port_s1u': {'set': set_enb_port_s1u, 'get': get_enb_port_s1u},
    'rru_local_if_name': {'set': set_rru_local_if_name, 'get': get_rru_local_if_name},
    'rru_local_addr': {'set': set_rru_local_addr, 'get': get_rru_local_addr},
    'rru_local_port': {'set': set_rru_local_port, 'get': get_rru_local_port},
    'rru_remote_addr': {'set': set_rru_remote_addr, 'get': get_rru_remote_addr},
    'rru_remote_port': {'set': set_rru_remote_port, 'get': get_rru_remote_port},
    'rcc_mme_ip_addr': {'set': set_rcc_mme_ip_addr, 'get': get_rcc_mme_ip_addr},
    'rcc_name_s1': {'set': set_rcc_name_s1, 'get': get_rcc_name_s1},
    'rcc_addr_s1': {'set': set_rcc_addr_s1, 'get': get_rcc_addr_s1},
    'rcc_name_s1u': {'set': set_rcc_name_s1u, 'get': get_rcc_name_s1u},
    'rcc_addr_s1u': {'set': set_rcc_addr_s1u, 'get': get_rcc_addr_s1u},
    'rcc_port_s1u': {'set': set_rcc_port_s1u, 'get': get_rcc_port_s1u},
    'rcc_local_if_name': {'set': set_rcc_local_if_name, 'get': get_rcc_local_if_name},
    'rcc_local_address': {'set': set_rcc_local_addr, 'get': get_rcc_local_addr},
    'rcc_local_port': {'set': set_rcc_local_port, 'get': get_rcc_local_port},
    'rcc_remote_addr': {'set': set_rcc_remote_addr, 'get': get_rcc_remote_addr},
    'rcc_remote_port': {'set': set_rcc_remote_port, 'get': get_rcc_remote_port},
    'PUCCH_ENB': {'set': set_pucch_enb, 'get': get_pucch_enb},
    'PUSCH_ENB': {'set': set_pusch_enb, 'get': get_pusch_enb},
    'RX_GAIN_ENB': {'set': set_rx_gain_enb, 'get': get_rx_gain_enb},
    'TX_GAIN_ENB': {'set': set_tx_gain_enb, 'get': get_tx_gain_enb},
    'TX_BANDWIDTH_ENB': {'set': set_tx_bandwidth_enb, 'get': get_tx_bandwidth_enb},
    'TX_CHANNEL_ENB': {'set': set_tx_channel_enb, 'get': get_tx_channel_enb},
    'TX_MODE_ENB': {'set': set_tx_mode_enb, 'get': get_tx_mode_enb},
    'UPLINK_FREQ_OFFSET_ENB': {set_ul_freq_offset_enb, 'get': get_ul_freq_offset_enb},
    'PUCCH_RCC': {'set': set_pucch_RCC, 'get': get_pucch_RCC},
    'PUSCH_RCC': {'set': set_pusch_RCC, 'get': get_pusch_RCC},
    'RX_GAIN_RCC': {'set': set_rx_gain_RCC, 'get': get_rx_gain_RCC},
    'TX_GAIN_RCC': {'set': set_tx_gain_RCC, 'get': get_tx_gain_RCC},
    'TX_BANDWIDTH_RCC': {'set': set_tx_bandwidth_RCC,'get': get_tx_bandwidth_RCC},
    'TX_CHANNEL_RCC': {'set': set_tx_channel_RCC, 'get': get_tx_channel_RCC},
    'TX_MODE_RCC': {'set': set_tx_mode_RCC, 'get': get_tx_mode_RCC},
    'UPLINK_FREQ_OFFSET_RCC': {set_ul_freq_offset_RCC, 'get': get_ul_freq_offset_RCC},
    'PUCCH_RRU': {'set': set_pucch_RRU, 'get': get_pucch_RRU},
    'PUSCH_RRU': {'set': set_pusch_RRU, 'get': get_pusch_RRU},
    'RX_GAIN_RRU': {'set': set_rx_gain_RRU, 'get': get_rx_gain_RRU},
    'TX_GAIN_RRU': {'set': set_tx_gain_RRU, 'get': get_tx_gain_RRU},
    'TX_BANDWIDTH_RRU': {'set': set_tx_bandwidth_RRU, 'get': get_tx_bandwidth_RRU},
    'TX_CHANNEL_RRU': {'set': set_tx_channel_RRU, 'get': get_tx_channel_RRU},
    'TX_MODE_RRU': {'set': set_tx_mode_RRU, 'get': get_tx_mode_RRU},
    'UPLINK_FREQ_OFFSET_RRU': {'set': set_ul_freq_offset_RRU, 'get': get_ul_freq_offset_RRU},
}

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

        # if err:
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

    def set_parameters(param_key_values_dict):
        """The UPI_N interface is able to configure the protocol (routing, transport, application) behavior by changing parameters.
        Parameters correspond to the  variables used in the protocols.
        This function (re)set the value(s) of the parameters specified in the dictionary argument.
        The list of available parameters supported by all platforms/OS are defined in this module.
        Parameters specific to a subgroup of platforms/OS are defined in the corresponding submodules.
        A list of supported parameters can be dynamically obtained using the get_info function on each module.
        Examples:
            .. code-block:: python
                >> param_key_values = {ROUTING_MAX_TTL : 5}
                >> result = control_engine.net.set_parameters(param_key_values)
                >> print result
                {ROUTING_MAX_TTL : 0}
        Args:
            param_key_values_dict (dict): dictionary containing the key (string) value (any) pairs for each parameter.
                An example is {CSMA_CW : 15, CSMA_CW_MIN : 15, CSMA_CW_MAX : 15}
        Returns:
            dict: A dictionary containing key (string name) error (0 = success, 1=fail, +1=error code) pairs for each parameter.
        """
        dict_return_set = {}
        for param_key, value in param_key_values_dict.iteritems():
            try:
                ret = param_key_functions_dict[param_key]['set'](value)
            except:
                ret = 1
            dict_return_set[param_key] = ret
        return dict_return_set

    def get_parameters(param_key_list):
        """Get the parameter on higher layers of protocol stack (higher MAC and above)
        Args:
           param_key_list: must a list of the parameters identified by their key.
        Returns:
        	a dictionary of the pair (parameter key , value)
        """

        dict_return_get = {}
        for key in param_key_list:
            try:
                value = param_key_functions_list[key]['get']()
                dict_return_get[key] = value
            except:
                pass
        return dict_return_get

    def set_generic(filename, key, value):
        # for setting the number of eNB served by the same MME.
        conf_path_1 = filename
        conf_path_2 = filename + ".temp"
        try:
            f_1 = open(conf_path_1)
            f_2 = open(conf_path_2, 'w')
        except IOError:
            return 1
        line = f_1.readline()
        ## If the file is not empty keep reading line one at a time till the file is empty
        trovato = False
        while line:
            finded = line.find(key)
            if finded != -1:
                trovato = True
                newline = key + " = " + value + ";"
                splits = line.split('#', 1)
                if (len(splits) > 1):
                    newline += "#" + splits[1]
                f_2.write(newline)
            else:
                f_2.write(line)
            line = f_1.readline()
        f_1.close()
        f_2.close()
        remove(conf_path_1)
        move(conf_path_1, conf_path_2)
        if trovato == False:
            return 1
        return 0

    def get_generic(filename, key):
        # for setting the number of eNB served by the same MME.
        conf_path_1 = filename
        f_1 = open(conf_path_1)
        line = f_1.readline()
        ## If the file is not empty keep reading line one at a time till the file is empty
        while line:
            finded = line.find(key)
            if finded != -1:
                splits = line.split('=', 1)
                if (len(splits) > 1):
                    splits_2 = splits[1].split(';', 1)
                    value = splits_2[0].replace(" ", "")
                    f_1.close()
                    return value
        f_1.close()
        return

    def MME_activation():
        return

    def MME_deactivation():
        return

    def HSS_activation():
        return

    def HSS_deactivation():
        return

    def SPGW_activation():
        return

    def SPGW_deactivation():
        return

    def eNB_activation():
        return

    def eNB_deactivation():
        return

    def RRU_activation():
        return

    def RRU_deactivation():
        return

    def RCC_activation():
        return

    def RCC_deactivation():
        return

    def UE_activation():
        return

    def UE_deactivation():
        return

    def UE_attach():
        return

    def UE_detach():
        return

    # SET FUNCTIONS of NET_UPI
    def set_mme_realm(value):
        TO_FIND = "REALM"
        return set_generic(MME_CONF_FILENAME, TO_FIND, value)

    def set_mme_served_enb(value):
        TO_FIND = "MAXENB"
        return set_generic(MME_CONF_FILENAME, TO_FIND, value)

    def set_mme_served_ue(value):
        TO_FIND = "MAXUE"
        return set_generic(MME_CONF_FILENAME, TO_FIND, value)

    def set_mme_tai_list(mcc, mnc, tac):
        # for setting the TAI list in the MME.
        conf_path_1 = my_path_epc + "/mme.conf"
        conf_path_2 = my_path_epc + "/mme_new.conf"
        try:
            f_1 = open(conf_path_1)
            f_2 = open(conf_path_2, 'w')
        except IOError:
            return 1
        line = f_1.readline()
        ## If the file is not empty keep reading line one at a time till the file is empty
        trovato = False
        while line:
            finded = line.find("    TAI_LIST")
            f_2.write(line)
            if finded != -1:
                trovato = True
                line1 = f_1.readline()
                while line1.find(");") == -1:
                    f_2.write(
                        "         {{MCC=\"{}\" ; MNC=\"{}\";  TAC = \"{}\"; }}                                   # YOUR TAI CONFIG HERE\n".format(
                            mcc, mnc, tac))
                    line1 = f_1.readline()
                f_2.write(line1)
            line = f_1.readline()
        f_1.close()
        f_2.close()
        remove(conf_path_1)
        move(conf_path_1, conf_path_2)
        if trovato == False:
            return 1
        return 0

    def set_mme_gummei_list(mcc, mnc, mme_gid, mme_code)
        # for setting the GUMMEI list in the MME.
        conf_path_1 = my_path_epc + "/mme.conf"
        conf_path_2 = my_path_epc + "/mme_new.conf"
        try:
            f_1 = open(conf_path_1)
            f_2 = open(conf_path_2, 'w')
        except IOError:
            return 1
        ## Read the first line
        line = f_1.readline()
        ## If the file is not empty keep reading line one at a time till the file is empty
        trovato == False
        while line:
            f_2.write(line)
            finded = line.find("    GUMMEI_LIST = (")
            if finded != -1:
                trovato = True
                line1 = f_1.readline()
                while line1.find(");") == -1:
                    f_2.write(
                        "         {{MCC=\"{}\" ; MNC=\"{}\";  MME_GID = \"{}\"; MME_CODE = \"{}\"; }}                                   # YOUR TAI CONFIG HERE\n".format(
                            mcc, mnc, mme_gid, mme_code))
                    line1 = f_1.readline()
                f_2.write(line1)
            line = f_1.readline()
        f_1.close()
        f_2.close()
        remove(conf_path_1)
        move(conf_path_1, conf_path_2)
        if trovato == False:
            return 1
        return 0

    def set_enb_name(value):
        TO_FIND_1 = "eNB_name"
        TO_FIND_2 = "Active_eNBs"
        ret_1 = set_generic(ENB_CONF_FILENAME, TO_FIND_1, value + "LTE_Box")
        if ret_1 != 0:
            return set_generic(ENB_CONF_FILENAME, TO_FIND_2, value + "LTE_Box")
        return ret_1

    def set_enb_id(value):
        TO_FIND = "eNB_ID"
        return set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_enb_cell_type(value):
        TO_FIND = "cell_type"
        return set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_enb_tracking_area_code(value):
        TO_FIND = "tracking_area_code"
        return set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_enb_mcc(value):
        TO_FIND = "mobile_country_code"
        return set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_enb_mnc(value):
        TO_FIND = "mobile_network_code"
        return set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_enb_mnc(value):
        TO_FIND = "mobile_network_code"
        return set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_rru_name(value):
        TO_FIND_1 = "eNB_name"
        TO_FIND_2 = "Active_eNBs"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            ret_1 = set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND_1, value + "LTE_Box")
            if ret_1 != 0:
                return set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND_2, value + "LTE_Box")
            return ret_1
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            ret_1 = set_generic(RRU_IF5_CONF_FILENAME, TO_FIND_1, value + "LTE_Box")
            if ret_1 != 0:
                return set_generic(RRU_IF5_CONF_FILENAME, TO_FIND_2, value + "LTE_Box")
            return ret_1

    def set_rru_id(value):
        TO_FIND = "eNB_ID"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rru_cell_type(value):
        TO_FIND = "cell_type"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rru_tracking_area_code(value):
        TO_FIND = "tracking_area_code"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rru_mcc(value):
        TO_FIND = "mobile_country_code"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rru_mnc(value):
        TO_FIND = "mobile_network_code"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_name(value):
        TO_FIND_1 = "eNB_name"
        TO_FIND_2 = "Active_eNBs"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            ret_1 = set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND_1, value + "LTE_Box")
            if ret_1 != 0:
                return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND_2, value + "LTE_Box")
            return ret_1
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            ret_1 = set_generic(RCC_IF5_CONF_FILENAME, TO_FIND_1, value + "LTE_Box")
            if ret_1 != 0:
                return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND_2, value + "LTE_Box")
            return ret_1

    def set_rcc_id(value):
        TO_FIND = "eNB_ID"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value + "LTE_Box")
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value + "LTE_Box")

    def set_rcc_cell_type(value):
        TO_FIND = "cell_type"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_tracking_area_code(value):
        TO_FIND = "tracking_area_code"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_mcc(value):
        TO_FIND = "mobile_country_code"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)
        return

    def set_rcc_mnc(value):
        TO_FIND = "mobile_network_code"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_fronthaul_transport_mode(value):
        TO_FIND = "tr_preference"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_mme_name_s1(value):
        TO_FIND = "MME_INTERFACE_NAME_FOR_S1_MME"
        return set_generic(MME_CONF_FILENAME, TO_FIND, value)

    def set_mme_addr_s1(value):
        TO_FIND = "MME_IPV4_ADDRESS_FOR_S1_MME"
        return set_generic(MME_CONF_FILENAME, TO_FIND, value)

    def set_mme_name_s11(value):
        TO_FIND = "MME_INTERFACE_NAME_FOR_S11_MME"
        return set_generic(MME_CONF_FILENAME, TO_FIND, value)

    def set_mme_addr_s11(value):
        TO_FIND = " MME_IPV4_ADDRESS_FOR_S11_MME"
        return set_generic(MME_CONF_FILENAME, TO_FIND, value)

    set_generic(SPGW_CONF_FILENAME, TO_FIND, value)

    def set_mme_port_s11(value):
        TO_FIND = "MME_PORT_FOR_S11_MME"
        return set_generic(MME_CONF_FILENAME, TO_FIND, value)

    def set_sgw_name_s11(value):
        TO_FIND = "SGW_INTERFACE_NAME_FOR_S11"
        return set_generic(SPGW_CONF_FILENAME, TO_FIND, value)

    def set_sgw_addr_s11(value):
        TO_FIND = " SGW_IPV4_ADDRESS_FOR_S11"
        return set_generic(MME_CONF_FILENAME, TO_FIND, value)

    set_generic(SPGW_CONF_FILENAME, TO_FIND, value)

    def set_sgw_name_s1u_s12_s4(value):
        TO_FIND = "SGW_INTERFACE_NAME_FOR_S1U_S12_S4_UP"
        return set_generic(SPGW_CONF_FILENAME, TO_FIND, value)

    def set_sgw_addr_s1u_s12_s4(value):
        TO_FIND = "SGW_IPV4_ADDRESS_FOR_S1U_S12_S4_UP"
        return set_generic(SPGW_CONF_FILENAME, TO_FIND, value)

    def set_sgw_port_s1u_s12_s4(value):
        TO_FIND = "SGW_IPV4_PORT_FOR_S1U_S12_S4_UP"
        return set_generic(SPGW_CONF_FILENAME, TO_FIND, value)

    def set_sgw_name_s5_s8(value):
        TO_FIND = "SGW_INTERFACE_NAME_FOR_S5_S8_UP"
        return set_generic(SPGW_CONF_FILENAME, TO_FIND, value)

    def set_sgw_addr_s5_s8(value):
        TO_FIND = "SGW_IPV4_ADDRESS_FOR_S5_S8_UP"
        return set_generic(SPGW_CONF_FILENAME, TO_FIND, value)

    def set_pgw_name_s5_s8(value):
        TO_FIND = "PGW_INTERFACE_NAME_FOR_S5_S8"
        return set_generic(SPGW_CONF_FILENAME, TO_FIND, value)

    def set_pgw_name_sgi(value):
        TO_FIND = "PGW_INTERFACE_NAME_FOR_SGI"
        return set_generic(SPGW_CONF_FILENAME, TO_FIND, value)

    def set_ue_ip_addr_pool(value):
        TO_FIND = "IPV4_LIST"
        return set_generic(SPGW_CONF_FILENAME, TO_FIND, value)

    def set_default_dns_addr(value):
        TO_FIND = "DEFAULT_DNS_IPV4_ADDRESS"
        return set_generic(SPGW_CONF_FILENAME, TO_FIND, value)

    def set_enb_mme_ip_addr(value):
        TO_FIND = "mme_ip_address"
        return set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_enb_name_s1(value)
        TO_FIND = "ENB_INTERFACE_NAME_FOR_S1_MME"
        return set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_enb_addr_s1(value):
        TO_FIND = "ENB_IPV4_ADDRESS_FOR_S1_MME"
        return set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_enb_name_s1u(value)
        TO_FIND = "ENB_INTERFACE_NAME_FOR_S1U"
        return set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_enb_addr_s1u(value)
        TO_FIND = "ENB_IPV4_ADDRESS_FOR_S1U"
        return set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_enb_port_s1u(value)
        TO_FIND = "ENB_PORT_FOR_S1U"
        return set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_rru_local_if_name(value):
        TO_FIND = "local_if_name"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rru_local_addr(value):
        TO_FIND = "local_address"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rru_local_if_name(value):
        TO_FIND = "local_if_name"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rru_local_port(value):
        TO_FIND = "local_port"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rru_remote_addr(value):
        TO_FIND = "remote_address"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rru_remote_port(value):
        TO_FIND = "remote_port"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_mme_ip_addr(value):
        TO_FIND = "mme_ip_address"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_name_s1(value)
        TO_FIND = "ENB_INTERFACE_NAME_FOR_S1_MME"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_addr_s1(value):
        TO_FIND = "ENB_IPV4_ADDRESS_FOR_S1_MME"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_name_s1u(value)
        TO_FIND = "ENB_INTERFACE_NAME_FOR_S1U"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_addr_s1u(value)
        TO_FIND = "ENB_IPV4_ADDRESS_FOR_S1U"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_port_s1u(value)
        TO_FIND = "ENB_PORT_FOR_S1U"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_local_if_name(value):
        TO_FIND = "local_if_name"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_local_addr(value):
        TO_FIND = "local_address"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_local_if_name(value):
        TO_FIND = "local_if_name"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_local_port(value):
        TO_FIND = "local_port"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_remote_addr(value):
        TO_FIND = "remote_address"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_remote_port(value):
        TO_FIND = "remote_port"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    # SET FUNCTIONS OF RADIO UPI
    def set_pucch_enb(value):
        TO_FIND = "pucch_p0_Nominal"
        return set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_pusch_enb(value):
        TO_FIND = "pusch_p0_Nominal"
        return set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_rx_gain_enb(value):
        TO_FIND = "rx_gain"
        return set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_tx_gain_enb(value):
        TO_FIND = "tx_gain"
        return set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_tx_bandwidth_enb(value):
        TO_FIND = "N_RB_DL"
        return set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_tx_channel_enb(value):
        TO_FIND = "downlink_frequency"
        return set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_tx_mode_enb(value):
        TO_FIND = "frame_type"
        return set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_ul_freq_offset_enb(value):
        TO_FIND = "uplink_frequency_offset"
        return set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_pucch_rcc(value):
        TO_FIND = "pucch_p0_Nominal"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_pusch_rcc(value):
        TO_FIND = "pusch_p0_Nominal"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rx_gain_rcc(value):
        TO_FIND = "rx_gain"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_tx_gain_rcc(value):
        TO_FIND = "tx_gain"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_tx_bandwidth_rcc(value):
        TO_FIND = "N_RB_DL"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_tx_channel_rcc(value):
        TO_FIND = "downlink_frequency"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_tx_mode_rcc(value):
        TO_FIND = "frame_type"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_ul_freq_offset_rcc(value):
        TO_FIND = "uplink_frequency_offset"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_pucch_rru(value):
        TO_FIND = "pucch_p0_Nominal"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_pusch_rru(value):
        TO_FIND = "pusch_p0_Nominal"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rx_gain_rru(value):
        TO_FIND = "rx_gain"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_tx_gain_rru(value):
        TO_FIND = "tx_gain"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_tx_bandwidth_rru(value):
        TO_FIND = "N_RB_DL"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_tx_channel_rru(value):
        TO_FIND = "downlink_frequency"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_tx_mode_rru(value):
        TO_FIND = "frame_type"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_ul_freq_offset_rru(value):
        TO_FIND = "uplink_frequency_offset"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    # GET FUNCTIONS OF NET UPI
    def get_mme_realm():
        TO_FIND = "REALM"
        return get_generic(MME_CONF_FILENAME, TO_FIND)

    def get_mme_served_enb():
        TO_FIND = "MAXENB"
        return get_generic(MME_CONF_FILENAME, TO_FIND)

    def get_mme_served_ue():
        TO_FIND = "MAXUE"
        return get_generic(MME_CONF_FILENAME, TO_FIND)

    def get_mme_tai_list():
        # for getting the TAI list in the MME.
        conf_path_1 = my_path_epc + "/mme.conf"
        conf_path_2 = my_path_epc + "/mme_new.conf"
        f_1 = open(conf_path_1)
        f_2 = open(conf_path_2, 'w')
        line = f_1.readline()
        ## If the file is not empty keep reading line one at a time till the file is empty
        while line:
            finded = line.find("    TAI_LIST")
            f_2.write(line)
            if finded != -1:
                line1 = f_1.readline()
                while line1.find(");") == -1:
                    f_2.write(
                        "         {{MCC=\"{}\" ; MNC=\"{}\";  TAC = \"{}\"; }}                                   # YOUR TAI CONFIG HERE\n".format(
                            mcc, mnc, tac))
                    line1 = f_1.readline()
                f_2.write(line1)
            line = f_1.readline()
        f_1.close()
        f_2.close()
        remove(conf_path_1)
        move(conf_path_1, conf_path_2)
        return

    def get_mme_gummei_list()
        # for getting the GUMMEI list in the MME.
        conf_path_1 = my_path_epc + "/mme.conf"
        conf_path_2 = my_path_epc + "/mme_new.conf"
        f_1 = open(conf_path_1)
        f_2 = open(conf_path_2, 'w')
        ## Read the first line
        line = f_1.readline()
        ## If the file is not empty keep reading line one at a time till the file is empty
        while line:
            f_2.write(line)
            finded = line.find("    GUMMEI_LIST = (")
            if finded != -1:
                line1 = f_1.readline()
                while line1.find(");") == -1:
                    f_2.write(
                        "         {{MCC=\"{}\" ; MNC=\"{}\";  MME_GID = \"{}\"; MME_CODE = \"{}\"; }}                                   # YOUR TAI CONFIG HERE\n".format(
                            mcc, mnc, mme_gid, mme_code))
                    line1 = f_1.readline()
                f_2.write(line1)
            line = f_1.readline()
        f_1.close()
        f_2.close()
        remove(conf_path_1)
        move(conf_path_1, conf_path_2)
        return

    def get_enb_name():
        TO_FIND = "eNB_name"
        return get_generic(ENB_CONF_FILENAME, TO_FIND_1)

    def get_enb_id():
        TO_FIND = "eNB_ID"
        return get_generic(ENB_CONF_FILENAME, TO_FIND)

    def get_enb_cell_type():
        TO_FIND = "cell_type"
        return get_generic(ENB_CONF_FILENAME, TO_FIND)

    def get_enb_tracking_area_code():
        TO_FIND = "tracking_area_code"
        return get_generic(ENB_CONF_FILENAME, TO_FIND)

    def get_enb_mcc():
        TO_FIND = "mobile_country_code"
        return get_generic(ENB_CONF_FILENAME, TO_FIND)

    def get_enb_mnc():
        TO_FIND = "mobile_network_code"
        return get_generic(ENB_CONF_FILENAME, TO_FIND)

    def get_enb_mnc():
        TO_FIND = "mobile_network_code"
        return get_generic(ENB_CONF_FILENAME, TO_FIND)

    def get_rru_name():
        TO_FIND = "eNB_name"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)

    def get_rru_id():
        TO_FIND = "eNB_ID"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)

    def get_rru_cell_type():
        TO_FIND = "cell_type"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)

    def get_rru_tracking_area_code():
        TO_FIND = "tracking_area_code"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)

    def get_rru_mcc():
        TO_FIND = "mobile_country_code"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)

    def get_rru_mnc():
        TO_FIND = "mobile_network_code"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)

    def get_rrc_name():
        TO_FIND = "eNB_name"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rrc_id():
        TO_FIND = "eNB_ID"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_cell_type():
        TO_FIND = "cell_type"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_tracking_area_code():
        TO_FIND = "tracking_area_code"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_mcc():
        TO_FIND = "mobile_country_code"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_mnc():
        TO_FIND = "mobile_network_code"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_fronthaul_transport_mode():
        TO_FIND = "tr_preference"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_mme_name_s1():
        TO_FIND = "MME_INTERFACE_NAME_FOR_S1_MME"
        return get_generic(MME_CONF_FILENAME, TO_FIND)

    def get_mme_addr_s1():
        TO_FIND = "MME_IPV4_ADDRESS_FOR_S1_MME"
        return get_generic(MME_CONF_FILENAME, TO_FIND)

    def get_mme_name_s11():
        TO_FIND = "MME_INTERFACE_NAME_FOR_S11_MME"
        return get_generic(MME_CONF_FILENAME, TO_FIND)

    def get_mme_addr_s11():
        TO_FIND = " MME_IPV4_ADDRESS_FOR_S11_MME"
        return get_generic(MME_CONF_FILENAME, TO_FIND)

    def get_mme_port_s11():
        TO_FIND = "MME_PORT_FOR_S11_MME"
        return get_generic(MME_CONF_FILENAME, TO_FIND)

    def get_sgw_name_s11():
        TO_FIND = "SGW_INTERFACE_NAME_FOR_S11"
        return get_generic(SPGW_CONF_FILENAME, TO_FIND)

    def get_sgw_addr_s11():
        TO_FIND = " SGW_IPV4_ADDRESS_FOR_S11"
        return get_generic(MME_CONF_FILENAME, TO_FIND)

    def get_sgw_name_s1u_s12_s4():
        TO_FIND = "SGW_INTERFACE_NAME_FOR_S1U_S12_S4_UP"
        return get_generic(SPGW_CONF_FILENAME, TO_FIND)

    def get_sgw_addr_s1u_s12_s4():
        TO_FIND = "SGW_IPV4_ADDRESS_FOR_S1U_S12_S4_UP"
        return get_generic(SPGW_CONF_FILENAME, TO_FIND)

    def get_sgw_port_s1u_s12_s4():
        TO_FIND = "SGW_IPV4_PORT_FOR_S1U_S12_S4_UP"
        return get_generic(SPGW_CONF_FILENAME, TO_FIND)

    def get_sgw_name_s5_s8():
        TO_FIND = "SGW_INTERFACE_NAME_FOR_S5_S8_UP"
        return get_generic(SPGW_CONF_FILENAME, TO_FIND)

    def get_sgw_addr_s5_s8():
        TO_FIND = "SGW_IPV4_ADDRESS_FOR_S5_S8_UP"
        return get_generic(SPGW_CONF_FILENAME, TO_FIND)

    def get_pgw_name_s5_s8():
        TO_FIND = "PGW_INTERFACE_NAME_FOR_S5_S8"
        return get_generic(SPGW_CONF_FILENAME, TO_FIND)

    def get_pgw_name_sgi():
        TO_FIND = "PGW_INTERFACE_NAME_FOR_SGI"
        return get_generic(SPGW_CONF_FILENAME, TO_FIND)

    def get_ue_ip_addr_pool():
        TO_FIND = "IPV4_LIST"
        return get_generic(SPGW_CONF_FILENAME, TO_FIND)

    def get_default_dns_addr():
        TO_FIND = "DEFAULT_DNS_IPV4_ADDRESS"
        return get_generic(SPGW_CONF_FILENAME, TO_FIND)

    def get_enb_mme_ip_addr():
        TO_FIND = "mme_ip_address"
        return get_generic(ENB_CONF_FILENAME, TO_FIND)

    def get_enb_name_s1():
        TO_FIND = "ENB_INTERFACE_NAME_FOR_S1_MME"
        return get_generic(ENB_CONF_FILENAME, TO_FIND)

    def get_enb_addr_s1():
        TO_FIND = "ENB_IPV4_ADDRESS_FOR_S1_MME"
        return get_generic(ENB_CONF_FILENAME, TO_FIND)

    def get_enb_name_s1u():
        TO_FIND = "ENB_INTERFACE_NAME_FOR_S1U"
        return get_generic(ENB_CONF_FILENAME, TO_FIND)

    def get_enb_addr_s1u():
        TO_FIND = "ENB_IPV4_ADDRESS_FOR_S1U"
        return get_generic(ENB_CONF_FILENAME, TO_FIND)

    def get_enb_port_s1u():
        TO_FIND = "ENB_PORT_FOR_S1U"
        return get_generic(ENB_CONF_FILENAME, TO_FIND)

    def get_rru_local_if_name():
        TO_FIND = "local_if_name"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)

    def get_rru_local_addr():
        TO_FIND = "local_address"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)

    def get_rru_local_if_name():
        TO_FIND = "local_if_name"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)

    def get_rru_local_port():
        TO_FIND = "local_port"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)

    def get_rru_remote_addr():
        TO_FIND = "remote_address"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)

    def get_rru_remote_port():
        TO_FIND = "remote_port"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_mme_ip_addr():
        TO_FIND = "mme_ip_address"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_name_s1():
        TO_FIND = "ENB_INTERFACE_NAME_FOR_S1_MME"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_addr_s1():
        TO_FIND = "ENB_IPV4_ADDRESS_FOR_S1_MME"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_name_s1u():
        TO_FIND = "ENB_INTERFACE_NAME_FOR_S1U"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_addr_s1u():
        TO_FIND = "ENB_IPV4_ADDRESS_FOR_S1U"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_port_s1u():
        TO_FIND = "ENB_PORT_FOR_S1U"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_local_if_name():
        TO_FIND = "local_if_name"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_local_addr():
        TO_FIND = "local_address"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_local_if_name():
        TO_FIND = "local_if_name"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_local_port():
        TO_FIND = "local_port"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_remote_addr():
        TO_FIND = "remote_address"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_remote_port():
        TO_FIND = "remote_port"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

# GET FUNCTIONS OF RADIO_UPI
    def get_pucch_enb(value):
        TO_FIND = "pucch_p0_Nominal"
        return get_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def get_pusch_enb(value):
        TO_FIND = "pusch_p0_Nominal"
        return get_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def get_rx_gain_enb(value):
        TO_FIND = "rx_gain"
        return get_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def get_tx_gain_enb(value):
        TO_FIND = "tx_gain"
        return get_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def get_tx_bandwidth_enb(value):
        TO_FIND = "N_RB_DL"
        return get_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def get_tx_channel_enb(value):
        TO_FIND = "downlink_frequency"
        return get_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def get_tx_mode_enb(value):
        TO_FIND = "frame_type"
        return get_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def get_ul_freq_offget_enb(value):
        TO_FIND = "uplink_frequency_offget"
        return get_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def get_pucch_rcc(value):
        TO_FIND = "pucch_p0_Nominal"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def get_pusch_rcc(value):
        TO_FIND = "pusch_p0_Nominal"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def get_rx_gain_rcc(value):
        TO_FIND = "rx_gain"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def get_tx_gain_rcc(value):
        TO_FIND = "tx_gain"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def get_tx_bandwidth_rcc(value):
        TO_FIND = "N_RB_DL"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def get_tx_channel_rcc(value):
        TO_FIND = "downlink_frequency"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def get_tx_mode_rcc(value):
        TO_FIND = "frame_type"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def get_ul_freq_offget_rcc(value):
        TO_FIND = "uplink_frequency_offget"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return get_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def get_pucch_rru(value):
        TO_FIND = "pucch_p0_Nominal"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return get_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def get_pusch_rru(value):
        TO_FIND = "pusch_p0_Nominal"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return get_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def get_rx_gain_rru(value):
        TO_FIND = "rx_gain"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return get_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def get_tx_gain_rru(value):
        TO_FIND = "tx_gain"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return get_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def get_tx_bandwidth_rru(value):
        TO_FIND = "N_RB_DL"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return get_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def get_tx_channel_rru(value):
        TO_FIND = "downlink_frequency"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return get_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def get_tx_mode_rru(value):
        TO_FIND = "frame_type"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return get_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def get_ul_freq_offset_rru(value):
        TO_FIND = "uplink_frequency_offset"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return get_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)