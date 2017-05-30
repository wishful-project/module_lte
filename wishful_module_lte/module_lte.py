__author__ = "Francesco Giannone, Domenico Garlisi"
__copyright__ = "Copyright (c) 2017, Sant'Anna, CNIT"
__version__ = "0.1.0"
__email__ = "{francesco.giannone@santannapisa.it, domenico.garlisi@cnit.it}"

import logging
import subprocess
from datetime import date, datetime
import os
from os import remove
from shutil import move
import sys

import wishful_framework as wishful_module
import functional_split
import wishful_upis as upis
import wishful_upis.lte.meta_radio as radio
import wishful_upis.lte.meta_net as net
import wishful_framework as wishful_module
from wishful_framework.classes import exceptions
from functional_split import Functional_split

#for setting the environmental variable with the path to the openairinterface root folder.
os.environ["OAI_5G_PATH"] = "/home/fabrizio/oai/openairinterface5g/"
OPENAIR_5G_PATH=os.environ["OAI_5G_PATH"]

my_path_enb = OPENAIR_5G_PATH+"targets/PROJECTS/GENERIC-LTE-EPC/CONF/"
my_path_epc = "/usr/local/etc/oai/"

MME_CONF_FILENAME = "/usr/local/etc/oai/mme.conf"
SPGW_CONF_FILENAME = "/usr/local/etc/oai/spgw.conf"
ENB_CONF_FILENAME = OPENAIR_5G_PATH+"targets/PROJECTS/GENERIC-LTE-EPC/CONF/enb.band7.tm1.usrpb210.conf"
RRU_IF4p5_CONF_FILENAME = OPENAIR_5G_PATH+"targets/PROJECTS/GENERIC-LTE-EPC/CONF/rru.band7.tm1.if4p5.usrpb210.conf"
RRU_IF5_CONF_FILENAME = OPENAIR_5G_PATH+"targets/PROJECTS/GENERIC-LTE-EPC/CONF/rru.band7.tm1.if5.usrpb210.conf"
RCC_IF4p5_CONF_FILENAME = OPENAIR_5G_PATH+"targets/PROJECTS/GENERIC-LTE-EPC/CONF/rcc.band7.tm1.if4p5.usrpb210.conf"
RCC_IF5_CONF_FILENAME = OPENAIR_5G_PATH+"targets/PROJECTS/GENERIC-LTE-EPC/CONF/rcc.band7.tm1.if5.usrpb210.conf"



@wishful_module.build_module
class LteModule(wishful_module.AgentModule):

    def __init__(self):
        super(LteModule, self).__init__()
        self.log = logging.getLogger('lte_module.main')

        # Dictionary for the matching the value to the relative SET/GET functions of NET_UPI
        self.param_key_functions_dict = {
            'MME_REALM': {'set': self.set_mme_realm, 'get': self.get_mme_realm},
            'MME_SERVED_ENB': {'set': self.set_mme_served_enb, 'get': self.get_mme_served_enb},
            'MME_SERVED_UE': {'set': self.set_mme_served_ue, 'get': self.get_mme_served_ue},
            'MME_TAI_LIST': {'set': self.set_mme_tai_list, 'get': self.get_mme_tai_list},
            'MME_GUMMEI_LIST': {'set': self.set_mme_gummei_list, 'get': self.get_mme_gummei_list},
            'ENB_NAME': {'set': self.set_enb_name, 'get': self.get_enb_name},
            'ENB_ID': {'set': self.set_enb_id, 'get': self.get_enb_id},
            'ENB_CELL_TYPE': {'set': self.set_enb_cell_type, 'get': self.get_enb_cell_type},
            'ENB_TRACKING_AREA_CODE': {'set': self.set_enb_tracking_area_code, 'get': self.get_enb_tracking_area_code},
            'ENB_MCC': {'set': self.set_enb_mcc, 'get': self.get_enb_mcc},
            'ENB_MNC': {'set': self.set_enb_mnc, 'get': self.get_enb_mnc},
            'RRU_NAME': {'set': self.set_rru_name, 'get': self.get_rru_name},
            'RRU_ID': {'set': self.set_rru_id, 'get': self.get_rru_id},
            'RRU_CELL_TYPE': {'set': self.set_rru_cell_type, 'get': self.get_rru_cell_type},
            'RRU_TRACKING_AREA_CODE': {'set': self.set_rru_tracking_area_code, 'get': self.get_rru_tracking_area_code},
            # 'RRU_MCC': {'set': set_rru_mcc, 'get': get_rru_mcc},
            'RRU_MNC': {'set': self.set_rru_mnc, 'get': self.get_rru_mnc},
            # 'RCC_NAME': {'set': set_rcc_name, 'get': get_rcc_name},
            # 'RCC_ID': {'set': set_rcc_id, 'get': get_rcc_id},
            'RCC_CELL_TYPE': {'set': self.set_rcc_cell_type, 'get': self.get_rcc_cell_type},
            'RCC_TRACKING_AREA_CODE': {'set': self.set_rcc_tracking_area_code, 'get': self.get_rcc_tracking_area_code},
            'RCC_MCC': {'set': self.set_rcc_mcc, 'get': self.get_rcc_mcc},
            'SPLIT_LEVEL': {'set': Functional_split.set_split_level, 'get': Functional_split.get_split_level},
            'FRONTHAUL_TRANSPORT_MODE': {'set': self.set_fronthaul_transport_mode, 'get': self.get_fronthaul_transport_mode},
            'mme_S1_name': {'set': self.set_mme_name_s1, 'get': self.get_mme_name_s1},
            'mme_S1_addr': {'set': self.set_mme_addr_s1, 'get': self.get_mme_addr_s1},
            'mme_S11_name': {'set': self.set_mme_name_s11, 'get': self.get_mme_name_s11},
            'mme_S11_addr': {'set': self.set_mme_addr_s11, 'get': self.get_mme_addr_s11},
            'mme_S11_port': {'set': self.set_mme_port_s11, 'get': self.get_mme_port_s11},
            'sgw_S11_name': {'set': self.set_sgw_name_s11, 'get': self.get_sgw_name_s11},
            'sgw_S11_addr': {'set': self.set_sgw_addr_s11, 'get': self.get_sgw_addr_s11},
            'sgw_S1U_S12_S4_name': {'set': self.set_sgw_name_s1u_s12_s4, 'get': self.get_sgw_name_s1u_s12_s4},
            'sgw_S1U_S12_S4_addr': {'set': self.set_sgw_addr_s1u_s12_s4, 'get': self.get_sgw_addr_s1u_s12_s4},
            'sgw_S1U_S12_S4_port': {'set': self.set_sgw_port_s1u_s12_s4, 'get': self.get_sgw_port_s1u_s12_s4},
            'sgw_S5_S8_name': {'set': self.set_sgw_name_s5_s8, 'get': self.get_sgw_name_s5_s8},
            'sgw_S5_S8_addr': {'set': self.set_sgw_addr_s5_s8, 'get': self.get_sgw_addr_s5_s8},
            'pgw_S5_S8_name': {'set': self.set_pgw_name_s5_s8, 'get': self.get_pgw_name_s5_s8},
            'pgw_SGi_name': {'set': self.set_pgw_name_sgi, 'get': self.get_pgw_name_sgi},
            'ip_address_pool': {'set': self.set_ue_ip_addr_pool, 'get': self.get_ue_ip_addr_pool},
            'default_DNS_addr': {'set': self.set_default_dns_addr, 'get': self.get_default_dns_addr},
            'enb_mme_ip_addr': {'set': self.set_enb_mme_ip_addr, 'get': self.get_enb_mme_ip_addr},
            'enb_name_s1': {'set': self.set_enb_name_s1, 'get': self.get_enb_name_s1},
            'enb_s1_addr': {'set': self.set_enb_addr_s1, 'get': self.get_enb_addr_s1},
            'enb_name_s1u': {'set': self.set_enb_name_s1u, 'get': self.get_enb_name_s1u},
            'enb_addr_s1u': {'set': self.set_enb_addr_s1u, 'get': self.get_enb_addr_s1u},
            'enb_port_s1u': {'set': self.set_enb_port_s1u, 'get': self.get_enb_port_s1u},
            'rru_local_if_name': {'set': self.set_rru_local_if_name, 'get': self.get_rru_local_if_name},
            'rru_local_addr': {'set': self.set_rru_local_addr, 'get': self.get_rru_local_addr},
            'rru_local_port': {'set': self.set_rru_local_port, 'get': self.get_rru_local_port},
            'rru_remote_addr': {'set': self.set_rru_remote_addr, 'get': self.get_rru_remote_addr},
            'rru_remote_port': {'set': self.set_rru_remote_port, 'get': self.get_rru_remote_port},
            'rcc_mme_ip_addr': {'set': self.set_rcc_mme_ip_addr, 'get': self.get_rcc_mme_ip_addr},
            'rcc_name_s1': {'set': self.set_rcc_name_s1, 'get': self.get_rcc_name_s1},
            'rcc_addr_s1': {'set': self.set_rcc_addr_s1, 'get': self.get_rcc_addr_s1},
            'rcc_name_s1u': {'set': self.set_rcc_name_s1u, 'get': self.get_rcc_name_s1u},
            'rcc_addr_s1u': {'set': self.set_rcc_addr_s1u, 'get': self.get_rcc_addr_s1u},
            'rcc_port_s1u': {'set': self.set_rcc_port_s1u, 'get': self.get_rcc_port_s1u},
            'rcc_local_if_name': {'set': self.set_rcc_local_if_name, 'get': self.get_rcc_local_if_name},
            'rcc_local_address': {'set': self.set_rcc_local_addr, 'get': self.get_rcc_local_addr},
            'rcc_local_port': {'set': self.set_rcc_local_port, 'get': self.get_rcc_local_port},
            'rcc_remote_addr': {'set': self.set_rcc_remote_addr, 'get': self.get_rcc_remote_addr},
            'rcc_remote_port': {'set': self.set_rcc_remote_port, 'get': self.get_rcc_remote_port},
            'PUCCH_ENB': {'set': self.set_pucch_enb, 'get': self.get_pucch_enb},
            'PUSCH_ENB': {'set': self.set_pusch_enb, 'get': self.get_pusch_enb},
            'RX_GAIN_enb': {'set': self.set_rx_gain_enb, 'get': self.get_rx_gain_enb},
            'TX_GAIN_enb': {'set': self.set_tx_gain_enb, 'get': self.get_tx_gain_enb},
            'TX_BANDWIDTH_enb': {'set': self.set_tx_bandwidth_enb, 'get': self.get_tx_bandwidth_enb},
            'TX_CHANNEL_enb': {'set': self.set_tx_channel_enb, 'get': self.get_tx_channel_enb},
            'TX_MODE_enb': {'set': self.set_tx_mode_enb, 'get': self.get_tx_mode_enb},
            # 'UPLINK_FREQ_OFFSET_ENB': {'set': set_ul_freq_offset_enb, 'get': get_ul_freq_offset_enb},
            # 'PUCCH_RCC': {'set': set_pucch_RCC, 'get': get_pucch_RCC},
            # 'PUSCH_RCC': {'set': set_pusch_RCC, 'get': get_pusch_RCC},
            # 'RX_GAIN_RCC': {'set': set_rx_gain_RCC, 'get': get_rx_gain_RCC},
            # 'TX_GAIN_RCC': {'set': set_tx_gain_RCC, 'get': get_tx_gain_RCC},
            # 'TX_BANDWIDTH_RCC': {'set': set_tx_bandwidth_RCC,'get': get_tx_bandwidth_RCC},
            # 'TX_CHANNEL_RCC': {'set': set_tx_channel_RCC, 'get': get_tx_channel_RCC},
            # 'TX_MODE_RCC': {'set': set_tx_mode_RCC, 'get': get_tx_mode_RCC},
            # 'UPLINK_FREQ_OFFSET_RCC': {'set': set_ul_freq_offset_RCC, 'get': get_ul_freq_offset_RCC},
            # 'PUCCH_RRU': {'set': set_pucch_RRU, 'get': get_pucch_RRU},
            # 'PUSCH_RRU': {'set': set_pusch_RRU, 'get': get_pusch_RRU},
            # 'RX_GAIN_RRU': {'set': set_rx_gain_RRU, 'get': get_rx_gain_RRU},
            # 'TX_GAIN_RRU': {'set': set_tx_gain_RRU, 'get': get_tx_gain_RRU},
            # 'TX_BANDWIDTH_RRU': {'set': set_tx_bandwidth_RRU, 'get': get_tx_bandwidth_RRU},
            # 'TX_CHANNEL_RRU': {'set': set_tx_channel_RRU, 'get': get_tx_channel_RRU},
            # 'TX_MODE_RRU': {'set': set_tx_mode_RRU, 'get': get_tx_mode_RRU},
            # 'UPLINK_FREQ_OFFSET_RRU': {'set': set_ul_freq_offset_RRU, 'get': get_ul_freq_offset_RRU},
        }


    @wishful_module.bind_function(upis.net.set_parameters)
    def set_parameters(self, param_key_values_dict):
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
        for param_key, value in param_key_values_dict.items():
            try:
                print(param_key)
                print(value)
                ret = self.param_key_functions_dict[param_key]['set'](value)
            except (Exception) as err:
                print("exception", err)
                print("Error: unable to performs set_parameters")
                ret = 1
            dict_return_set[param_key] = ret
        return dict_return_set

    @wishful_module.bind_function(upis.net.get_parameters)
    def get_parameters(self, param_key_list):
        """Get the parameter on higher layers of protocol stack (higher MAC and above)
        Args:
           param_key_list: must a list of the parameters identified by their key.
        Returns:
            a dictionary of the pair (parameter key , value)
        """

        dict_return_get = {}
        for key in param_key_list:
            try:
                value = self.param_key_functions_dict[key]['get']()
                dict_return_get[key] = value
            except:
                pass
        return dict_return_get

    @wishful_module.bind_function(upis.net.MME_activation)
    def MME_activation(self):
        return

    @wishful_module.bind_function(upis.net.MME_deactivation)
    def MME_deactivation(self):
        return

    @wishful_module.bind_function(upis.net.HSS_activation)
    def HSS_activation(self):
        return

    @wishful_module.bind_function(upis.net.HSS_deactivation)
    def HSS_deactivation(self):
        return

    @wishful_module.bind_function(upis.net.SPGW_activation)
    def SPGW_activation(self):
        return

    @wishful_module.bind_function(upis.net.SPGW_deactivation)
    def SPGW_deactivation(self):
        return

    @wishful_module.bind_function(upis.net.eNB_activation)
    def eNB_activation(self):
        return

    @wishful_module.bind_function(upis.net.eNB_deactivation)
    def eNB_deactivation(self):
        return

    @wishful_module.bind_function(upis.net.RRU_activation)
    def RRU_activation(self):
        return

    @wishful_module.bind_function(upis.net.get_parameters)
    def RRU_deactivation(self):
        return

    @wishful_module.bind_function(upis.net.RRU_deactivation)
    def RCC_activation(self):
        return

    @wishful_module.bind_function(upis.net.RCC_deactivation)
    def RCC_deactivation(self):
        return

    @wishful_module.bind_function(upis.net.UE_activation)
    def UE_activation(self):
        return

    @wishful_module.bind_function(upis.net.UE_deactivation)
    def UE_deactivation(self):
        return

    @wishful_module.bind_function(upis.net.UE_attach)
    def UE_attach(self):
        return

    @wishful_module.bind_function(upis.net.UE_detach)
    def UE_detach(self):
        return


    #CHECK if the environmental variable is properly set
    def check_environment_variable(self):
        if "OAI_5G_PATH" in os.environ:
            return True
        print("Please set the environmental variable OPENAIR_5G_PATH with the path to the openairinterface root folder.")
        return False

    # SET FUNCTIONS of NET_UPI
    def set_generic(self, filename, key, value):
        # for setting the number of eNB served by the same MME.
        conf_path_1 = filename
        conf_path_2 = filename + ".temp"
        try:
            f_1 = open(conf_path_1)
            f_2 = open(conf_path_2, 'w')
        except (Exception) as err:
            print("exception", err)
            print("Error: unable to open configuration file")
            return 1
        line = f_1.readline()

        ## If the file is not empty keep reading line one at a time till the file is empty
        check_find = False
        while line:
            finded = line.find(key)
            if finded != -1:
                check_find = True
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
        if check_find  == False:
            return 1
        return 0

    def get_generic(self, filename, key):
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

    def set_mme_realm(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "REALM"
        return self.set_generic(MME_CONF_FILENAME, TO_FIND, value)

    def set_mme_served_enb(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "MAXENB"
        return self.set_generic(MME_CONF_FILENAME, TO_FIND, value)

    def set_mme_served_ue(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "MAXUE"
        return self.set_generic(MME_CONF_FILENAME, TO_FIND, value)

    def set_mme_tai_list(self, mcc, mnc, tac):
        if not self.check_environment_variable():
            return
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
        check_find = False
        while line:
            finded = line.find("    TAI_LIST")
            f_2.write(line)
            if finded != -1:
                check_find = True
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
        if check_find  == False:
            return 1
        return 0

    def set_mme_gummei_list(self, mcc, mnc, mme_gid, mme_code):
        if not self.check_environment_variable():
            return
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
        check_find == False
        while line:
            f_2.write(line)
            finded = line.find("    GUMMEI_LIST = (")
            if finded != -1:
                check_find = True
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
        if check_find  == False:
            return 1
        return 0

    def set_enb_name(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND_1 = "eNB_name"
        TO_FIND_2 = "Active_eNBs"
        ret_1 = self.set_generic(ENB_CONF_FILENAME, TO_FIND_1, value + "LTE_Box")
        if ret_1 != 0:
            return self.set_generic(ENB_CONF_FILENAME, TO_FIND_2, value + "LTE_Box")
        return ret_1

    def set_enb_id(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "eNB_ID"
        return self.set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_enb_cell_type(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "cell_type"
        return self.set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_enb_tracking_area_code(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "tracking_area_code"
        return self.set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_enb_mcc(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "mobile_country_code"
        return self.set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_enb_mnc(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "mobile_network_code"
        return self.set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_enb_mnc(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "mobile_network_code"
        return self.set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_rru_name(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND_1 = "eNB_name"
        TO_FIND_2 = "Active_eNBs"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            ret_1 = self.set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND_1, value + "LTE_Box")
            if ret_1 != 0:
                return self.set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND_2, value + "LTE_Box")
            return ret_1
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            ret_1 = self.set_generic(RRU_IF5_CONF_FILENAME, TO_FIND_1, value + "LTE_Box")
            if ret_1 != 0:
                return self.set_generic(RRU_IF5_CONF_FILENAME, TO_FIND_2, value + "LTE_Box")
            return ret_1

    def set_rru_id(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "eNB_ID"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rru_cell_type(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "cell_type"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rru_tracking_area_code(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "tracking_area_code"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

        def set_rru_mcc(self, value):
            if not self.check_environment_variable():
                return
            TO_FIND = "mobile_country_code"
            if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
                return self.set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
            elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
                return self.set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rru_mnc(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "mobile_network_code"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_name(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND_1 = "eNB_name"
        TO_FIND_2 = "Active_eNBs"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            ret_1 = self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND_1, value + "LTE_Box")
            if ret_1 != 0:
                return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND_2, value + "LTE_Box")
            return ret_1
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            ret_1 = self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND_1, value + "LTE_Box")
            if ret_1 != 0:
                return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND_2, value + "LTE_Box")
            return ret_1

    def set_rcc_id(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "eNB_ID"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value + "LTE_Box")
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value + "LTE_Box")

    def set_rcc_cell_type(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "cell_type"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_tracking_area_code(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "tracking_area_code"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_mcc(value):
        if not self.check_environment_variable():
            return
        TO_FIND = "mobile_country_code"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)
        return

    def set_rcc_mnc(value):
        if not self.check_environment_variable():
            return
        TO_FIND = "mobile_network_code"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_fronthaul_transport_mode(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "tr_preference"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_mme_name_s1(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "MME_INTERFACE_NAME_FOR_S1_MME"
        return self.set_generic(MME_CONF_FILENAME, TO_FIND, value)

    def set_mme_addr_s1(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "MME_IPV4_ADDRESS_FOR_S1_MME"
        return self.set_generic(MME_CONF_FILENAME, TO_FIND, value)

    def set_mme_name_s11(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "MME_INTERFACE_NAME_FOR_S11_MME"
        return self.set_generic(MME_CONF_FILENAME, TO_FIND, value)

    def set_mme_addr_s11(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = " MME_IPV4_ADDRESS_FOR_S11_MME"
        return self.set_generic(MME_CONF_FILENAME, TO_FIND, value)

    def set_mme_port_s11(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "MME_PORT_FOR_S11_MME"
        return self.set_generic(MME_CONF_FILENAME, TO_FIND, value)

    def set_sgw_name_s11(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "SGW_INTERFACE_NAME_FOR_S11"
        return self.set_generic(SPGW_CONF_FILENAME, TO_FIND, value)

    def set_sgw_addr_s11(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = " SGW_IPV4_ADDRESS_FOR_S11"
        return self.set_generic(MME_CONF_FILENAME, TO_FIND, value)

    def set_sgw_name_s1u_s12_s4(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "SGW_INTERFACE_NAME_FOR_S1U_S12_S4_UP"
        return self.set_generic(SPGW_CONF_FILENAME, TO_FIND, value)

    def set_sgw_addr_s1u_s12_s4(value):
        if not self.check_environment_variable():
            return
        TO_FIND = "SGW_IPV4_ADDRESS_FOR_S1U_S12_S4_UP"
        return self.set_generic(SPGW_CONF_FILENAME, TO_FIND, value)

    def set_sgw_port_s1u_s12_s4(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "SGW_IPV4_PORT_FOR_S1U_S12_S4_UP"
        return self.set_generic(SPGW_CONF_FILENAME, TO_FIND, value)

    def set_sgw_name_s5_s8(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "SGW_INTERFACE_NAME_FOR_S5_S8_UP"
        return self.set_generic(SPGW_CONF_FILENAME, TO_FIND, value)

    def set_sgw_addr_s5_s8(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "SGW_IPV4_ADDRESS_FOR_S5_S8_UP"
        return self.set_generic(SPGW_CONF_FILENAME, TO_FIND, value)

    def set_pgw_name_s5_s8(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "PGW_INTERFACE_NAME_FOR_S5_S8"
        return self.set_generic(SPGW_CONF_FILENAME, TO_FIND, value)

    def set_pgw_name_sgi(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "PGW_INTERFACE_NAME_FOR_SGI"
        return self.set_generic(SPGW_CONF_FILENAME, TO_FIND, value)

    def set_ue_ip_addr_pool(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "IPV4_LIST"
        return self.set_generic(SPGW_CONF_FILENAME, TO_FIND, value)

    def set_default_dns_addr(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "DEFAULT_DNS_IPV4_ADDRESS"
        return self.set_generic(SPGW_CONF_FILENAME, TO_FIND, value)

    def set_enb_mme_ip_addr(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "mme_ip_address"
        return self.set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_enb_name_s1(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "ENB_INTERFACE_NAME_FOR_S1_MME"
        return self.set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_enb_addr_s1(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "ENB_IPV4_ADDRESS_FOR_S1_MME"
        return self.set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_enb_name_s1u(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "ENB_INTERFACE_NAME_FOR_S1U"
        return self.set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_enb_addr_s1u(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "ENB_IPV4_ADDRESS_FOR_S1U"
        return self.set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_enb_port_s1u(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "ENB_PORT_FOR_S1U"
        return self.set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_rru_local_if_name(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "local_if_name"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rru_local_addr(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "local_address"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rru_local_if_name(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "local_if_name"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rru_local_port(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "local_port"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rru_remote_addr(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "remote_address"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rru_remote_port(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "remote_port"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_mme_ip_addr(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "mme_ip_address"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_name_s1(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "ENB_INTERFACE_NAME_FOR_S1_MME"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_addr_s1(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "ENB_IPV4_ADDRESS_FOR_S1_MME"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_name_s1u(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "ENB_INTERFACE_NAME_FOR_S1U"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_addr_s1u(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "ENB_IPV4_ADDRESS_FOR_S1U"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_port_s1u(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "ENB_PORT_FOR_S1U"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_local_if_name(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "local_if_name"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_local_addr(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "local_address"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_local_if_name(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "local_if_name"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_local_port(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "local_port"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_remote_addr(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "remote_address"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rcc_remote_port(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "remote_port"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    # SET FUNCTIONS OF RADIO UPI
    def set_pucch_enb(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "pucch_p0_Nominal"
        return self.set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_pusch_enb(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "pusch_p0_Nominal"
        return self.set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_rx_gain_enb(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "rx_gain"
        return self.set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_tx_gain_enb(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "tx_gain"
        return self.set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_tx_bandwidth_enb(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "N_RB_DL"
        return self.set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_tx_channel_enb(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "downlink_frequency"
        return self.set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_tx_mode_enb(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "frame_type"
        return self.set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_ul_freq_offset_enb(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "uplink_frequency_offset"
        return self.set_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def set_pucch_rcc(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "pucch_p0_Nominal"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_pusch_rcc(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "pusch_p0_Nominal"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rx_gain_rcc(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "rx_gain"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_tx_gain_rcc(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "tx_gain"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_tx_bandwidth_rcc(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "N_RB_DL"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_tx_channel_rcc(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "downlink_frequency"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_tx_mode_rcc(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "frame_type"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_ul_freq_offset_rcc(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "uplink_frequency_offset"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.set_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def set_pucch_rru(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "pucch_p0_Nominal"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_pusch_rru(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "pusch_p0_Nominal"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_rx_gain_rru(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "rx_gain"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_tx_gain_rru(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "tx_gain"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_tx_bandwidth_rru(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "N_RB_DL"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_tx_channel_rru(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "downlink_frequency"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_tx_mode_rru(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "frame_type"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def set_ul_freq_offset_rru(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "uplink_frequency_offset"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.set_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.set_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    # GET FUNCTIONS OF NET UPI
    def get_mme_realm(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "REALM"
        return self.get_generic(MME_CONF_FILENAME, TO_FIND)

    def get_mme_served_enb(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "MAXENB"
        return self.get_generic(MME_CONF_FILENAME, TO_FIND)

    def get_mme_served_ue(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "MAXUE"
        return self.get_generic(MME_CONF_FILENAME, TO_FIND)

    def get_mme_tai_list(self):
        if not self.check_environment_variable():
            return
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

    def get_mme_gummei_list(self):
        if not self.check_environment_variable():
            return
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

    def get_enb_name(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "eNB_name"
        return self.get_generic(ENB_CONF_FILENAME, TO_FIND_1)

    def get_enb_id(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "eNB_ID"
        return self.get_generic(ENB_CONF_FILENAME, TO_FIND)

    def get_enb_cell_type(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "cell_type"
        return self.get_generic(ENB_CONF_FILENAME, TO_FIND)

    def get_enb_tracking_area_code(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "tracking_area_code"
        return self.get_generic(ENB_CONF_FILENAME, TO_FIND)

    def get_enb_mcc(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "mobile_country_code"
        return self.get_generic(ENB_CONF_FILENAME, TO_FIND)

    def get_enb_mnc(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "mobile_network_code"
        return self.get_generic(ENB_CONF_FILENAME, TO_FIND)

    def get_rru_name(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "eNB_name"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)

    def get_rru_id(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "eNB_ID"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)

    def get_rru_cell_type(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "cell_type"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)

    def get_rru_tracking_area_code(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "tracking_area_code"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)

    def get_rru_mcc(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "mobile_country_code"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)

    def get_rru_mnc(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "mobile_network_code"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)

    def get_rrc_name(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "eNB_name"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rrc_id(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "eNB_ID"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_cell_type(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "cell_type"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_tracking_area_code(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "tracking_area_code"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_mcc(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "mobile_country_code"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_mnc(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "mobile_network_code"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_fronthaul_transport_mode(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "tr_preference"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_mme_name_s1(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "MME_INTERFACE_NAME_FOR_S1_MME"
        return self.get_generic(MME_CONF_FILENAME, TO_FIND)

    def get_mme_addr_s1(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "MME_IPV4_ADDRESS_FOR_S1_MME"
        return self.get_generic(MME_CONF_FILENAME, TO_FIND)

    def get_mme_name_s11(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "MME_INTERFACE_NAME_FOR_S11_MME"
        return self.get_generic(MME_CONF_FILENAME, TO_FIND)

    def get_mme_addr_s11(self):
        if not self.check_environment_variable():
            return
        TO_FIND = " MME_IPV4_ADDRESS_FOR_S11_MME"
        return self.get_generic(MME_CONF_FILENAME, TO_FIND)

    def get_mme_port_s11(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "MME_PORT_FOR_S11_MME"
        return self.get_generic(MME_CONF_FILENAME, TO_FIND)

    def get_sgw_name_s11(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "SGW_INTERFACE_NAME_FOR_S11"
        return self.get_generic(SPGW_CONF_FILENAME, TO_FIND)

    def get_sgw_addr_s11(self):
        if not self.check_environment_variable():
            return
        TO_FIND = " SGW_IPV4_ADDRESS_FOR_S11"
        return self.get_generic(MME_CONF_FILENAME, TO_FIND)

    def get_sgw_name_s1u_s12_s4(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "SGW_INTERFACE_NAME_FOR_S1U_S12_S4_UP"
        return self.get_generic(SPGW_CONF_FILENAME, TO_FIND)

    def get_sgw_addr_s1u_s12_s4(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "SGW_IPV4_ADDRESS_FOR_S1U_S12_S4_UP"
        return self.get_generic(SPGW_CONF_FILENAME, TO_FIND)

    def get_sgw_port_s1u_s12_s4(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "SGW_IPV4_PORT_FOR_S1U_S12_S4_UP"
        return self.get_generic(SPGW_CONF_FILENAME, TO_FIND)

    def get_sgw_name_s5_s8(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "SGW_INTERFACE_NAME_FOR_S5_S8_UP"
        return self.get_generic(SPGW_CONF_FILENAME, TO_FIND)

    def get_sgw_addr_s5_s8(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "SGW_IPV4_ADDRESS_FOR_S5_S8_UP"
        return self.get_generic(SPGW_CONF_FILENAME, TO_FIND)

    def get_pgw_name_s5_s8(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "PGW_INTERFACE_NAME_FOR_S5_S8"
        return self.get_generic(SPGW_CONF_FILENAME, TO_FIND)

    def get_pgw_name_sgi(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "PGW_INTERFACE_NAME_FOR_SGI"
        return self.get_generic(SPGW_CONF_FILENAME, TO_FIND)

    def get_ue_ip_addr_pool(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "IPV4_LIST"
        return self.get_generic(SPGW_CONF_FILENAME, TO_FIND)

    def get_default_dns_addr(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "DEFAULT_DNS_IPV4_ADDRESS"
        return self.get_generic(SPGW_CONF_FILENAME, TO_FIND)

    def get_enb_mme_ip_addr(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "mme_ip_address"
        return self.get_generic(ENB_CONF_FILENAME, TO_FIND)

    def get_enb_name_s1(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "ENB_INTERFACE_NAME_FOR_S1_MME"
        return self.get_generic(ENB_CONF_FILENAME, TO_FIND)

    def get_enb_addr_s1(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "ENB_IPV4_ADDRESS_FOR_S1_MME"
        return self.get_generic(ENB_CONF_FILENAME, TO_FIND)

    def get_enb_name_s1u(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "ENB_INTERFACE_NAME_FOR_S1U"
        return self.get_generic(ENB_CONF_FILENAME, TO_FIND)

    def get_enb_addr_s1u(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "ENB_IPV4_ADDRESS_FOR_S1U"
        return self.get_generic(ENB_CONF_FILENAME, TO_FIND)

    def get_enb_port_s1u(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "ENB_PORT_FOR_S1U"
        return self.get_generic(ENB_CONF_FILENAME, TO_FIND)

    def get_rru_local_if_name(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "local_if_name"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)

    def get_rru_local_addr(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "local_address"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)

    def get_rru_local_if_name(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "local_if_name"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)

    def get_rru_local_port(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "local_port"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)

    def get_rru_remote_addr(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "remote_address"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)

    def get_rru_remote_port(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "remote_port"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RRU_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_mme_ip_addr(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "mme_ip_address"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_name_s1(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "ENB_INTERFACE_NAME_FOR_S1_MME"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_addr_s1(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "ENB_IPV4_ADDRESS_FOR_S1_MME"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_name_s1u(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "ENB_INTERFACE_NAME_FOR_S1U"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_addr_s1u(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "ENB_IPV4_ADDRESS_FOR_S1U"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_port_s1u(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "ENB_PORT_FOR_S1U"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_local_if_name(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "local_if_name"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_local_addr(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "local_address"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_local_if_name(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "local_if_name"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_local_port(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "local_port"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_remote_addr(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "remote_address"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    def get_rcc_remote_port(self):
        if not self.check_environment_variable():
            return
        TO_FIND = "remote_port"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND)
        elif Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND)

    #T FUNCTIONS OF RADIO_UPI
    def get_pucch_enb(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "pucch_p0_Nominal"
        return self.get_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def get_pusch_enb(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "pusch_p0_Nominal"
        return self.get_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def get_rx_gain_enb(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "rx_gain"
        return self.get_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def get_tx_gain_enb(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "tx_gain"
        return self.get_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def get_tx_bandwidth_enb(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "N_RB_DL"
        return self.get_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def get_tx_channel_enb(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "downlink_frequency"
        return self.get_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def get_tx_mode_enb(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "frame_type"
        return self.get_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def get_ul_freq_offget_enb(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "uplink_frequency_offget"
        return self.get_generic(ENB_CONF_FILENAME, TO_FIND, value)

    def get_pucch_rcc(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "pucch_p0_Nominal"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def get_pusch_rcc(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "pusch_p0_Nominal"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def get_rx_gain_rcc(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "rx_gain"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def get_tx_gain_rcc(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "tx_gain"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def get_tx_bandwidth_rcc(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "N_RB_DL"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def get_tx_channel_rcc(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "downlink_frequency"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def get_tx_mode_rcc(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "frame_type"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def get_ul_freq_offget_rcc(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "uplink_frequency_offget"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RCC_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.get_generic(RCC_IF5_CONF_FILENAME, TO_FIND, value)

    def get_pucch_rru(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "pucch_p0_Nominal"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.get_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def get_pusch_rru(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "pusch_p0_Nominal"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.get_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def get_rx_gain_rru(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "rx_gain"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.get_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def get_tx_gain_rru(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "tx_gain"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.get_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def get_tx_bandwidth_rru(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "N_RB_DL"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.get_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def get_tx_channel_rru(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "downlink_frequency"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.get_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def get_tx_mode_rru(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "frame_type"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.get_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)

    def get_ul_freq_offset_rru(self, value):
        if not self.check_environment_variable():
            return
        TO_FIND = "uplink_frequency_offset"
        if Functional_split.get_split_level() == Functional_split.FUNCTIONAL_SPLIT_TYPES.FOURpFIVE:
            return self.get_generic(RRU_IF4p5_CONF_FILENAME, TO_FIND, value)
        elif current_functional_split == FUNCTIONAL_SLPIT_TYPES.FIVE:
            return self.get_generic(RRU_IF5_CONF_FILENAME, TO_FIND, value)