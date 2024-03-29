import ipaddress
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler
try:

    def Site_types():
        print('''
_____________________________________________________________________
                    CPE Type
            [1] Primary CPE
            [2] Secondary CPE
______________________________________________________________________
        ''')
    env = Environment(loader=FileSystemLoader('Netmiko_Templates'))
    CPE_BGP = env.get_template('packet_prod_bgp_neighbor.txt')
    Lan_interface = env.get_template('packet_prod_LAN_interface.txt')


    def LAN_ip_check(ip):  # function checks the Lan subnet & returns the subnet mask.
        try:
            func_ip = ipaddress.ip_network(ip).with_netmask.split('/')
            return func_ip[1]
        except ValueError as e:
            return False


    def LAN_host(ip):  # function returns the list of hosts in lan subnet.
        try:
            func_host = ipaddress.ip_network(ip).hosts()
            func_list_of_host = []
            for host in func_host:
                func_list_of_host.append(host)
            return func_list_of_host
        except ValueError as e:
            return False


    def classhigh():
        env1 = Environment(loader=FileSystemLoader('Netmiko_Templates'))
        classification = env1.get_template('packet_prod_high_qos_template.txt')
        return classification


    def classlow():
        env2 = Environment(loader=FileSystemLoader('Netmiko_Templates'))
        classification = env2.get_template('packet_prod_low_qos_template.txt')
        return classification


    def snmp():
        env3 = Environment(loader=FileSystemLoader('Netmiko_Templates'))
        snmp_all = env3.get_template('packet_prod_snmp_all.txt').render().split('\n')
        return snmp_all


    def qos_interface():
        env4 = Environment(loader=FileSystemLoader('Netmiko_Templates'))
        int_qos = env4.get_template('packet_prod_qos_interface.txt').render().split('\n')
        return int_qos


    def bgp():
        env5 = Environment(loader=FileSystemLoader('Netmiko_Templates'))
        CPE_BGP = env5.get_template('packet_prod_bgp_neighbor.txt')
        return CPE_BGP

    def non_asr_fc_low_bandwidth_p():
        bw_in_bps = int(BW) * 1000000
        fc_Lan_interface = Lan_interface.render(LAN_IP=P_CPE_LAN, LAN_SUBNET=x).split('\n')
        output = netmiko_connect().send_config_set(classlow().render(Service_Bandwidth=bw_in_bps).split('\n'))
        output2 = netmiko_connect().send_config_set(qos_interface())
        output3 = netmiko_connect().send_config_set(fc_Lan_interface)
        output5 = netmiko_connect().send_config_set(bgp().render(CEBGP1=BGP1, CEBGP2=BGP2).split('\n'))
        output4 = netmiko_connect().send_config_set(snmp())
        exit()

    def non_asr_fc_highbandwidth_p():
        bw_in_bps = int(BW) * 1000000
        fc_Lan_interface = Lan_interface.render(LAN_IP=P_CPE_LAN, LAN_SUBNET=x).split('\n')
        output = netmiko_connect().send_config_set(classhigh().render(Service_Bandwidth=bw_in_bps).split('\n'))
        output2 = netmiko_connect().send_config_set(qos_interface())
        output3 = netmiko_connect().send_config_set(fc_Lan_interface)
        output5 = netmiko_connect().send_config_set(bgp().render(CEBGP1=BGP1, CEBGP2=BGP2).split('\n'))
        output4 = netmiko_connect().send_config_set(snmp())
        exit()


    def non_asr_fc_low_bandwidth_b():
        bw_in_bps = int(BW) * 1000000
        fc_Lan_interface = Lan_interface.render(LAN_IP=P_CPE_LAN, LAN_SUBNET=x).split('\n')
        output = netmiko_connect().send_config_set(classlow().render(Service_Bandwidth=bw_in_bps).split('\n'))
        output2 = netmiko_connect().send_config_set(qos_interface())
        output3 = netmiko_connect().send_config_set(fc_Lan_interface)
        output5 = netmiko_connect().send_config_set(bgp().render(CEBGP1=BGP1, CEBGP2=BGP2).split('\n'))
        output4 = netmiko_connect().send_config_set(snmp())
        exit()


    def non_asr_fc_highbandwidth_b():
        bw_in_bps = int(BW) * 1000000
        fc_Lan_interface = Lan_interface.render(LAN_IP=P_CPE_LAN, LAN_SUBNET=x).split('\n')
        output = netmiko_connect().send_config_set(classhigh().render(Service_Bandwidth=bw_in_bps).split('\n'))
        output2 = netmiko_connect().send_config_set(qos_interface())
        output3 = netmiko_connect().send_config_set(fc_Lan_interface)
        output5 = netmiko_connect().send_config_set(bgp().render(CEBGP1=BGP1, CEBGP2=BGP2).split('\n'))
        output4 = netmiko_connect().send_config_set(snmp())
        exit()

    def Bandwidth(b):
        if b.isdigit():
            return True
        else:
            return False


    def netmiko_connect():
        net_connect = ConnectHandler(
            device_type="cisco_ios",
            host="10.255.1.142",
            username="admin",
            password="admin",
            timeout='120'
        )
        return net_connect


    Site_types()
    site_options = input("Enter your options: ")
    while int(site_options) != 0:
        if int(site_options) == 1:
            lan_subnet = input("Introduce your LAN subnet: ")
            while True:
                if LAN_ip_check(lan_subnet) is False:
                    print("Provided LAN Subnet is Incorrect, Please Try again!!")
                else:
                    x = LAN_ip_check(lan_subnet)  # returns only subnet of LAN network
                    break
                lan_subnet = input("Introduce your LAN subnet again: ")
            hosts = LAN_host(lan_subnet)
            P_CPE_LAN = hosts[2]
            BGP1 = hosts[0]
            BGP2 = hosts[1]
            BW = input('Introduce your Bandwidth in Mbps: ')
            while True:
                if Bandwidth(BW) is False:
                    print('Invalid Bandwidth')
                elif int(BW) <= 10:
                    non_asr_fc_low_bandwidth_p()
                elif int(BW) > 10:
                    non_asr_fc_highbandwidth_p()
                else:
                    break
                BW = input('Introduce your Bandwidth in Mbps again: ')
        elif int(site_options) == 2:
            lan_subnet = input("Introduce your LAN subnet: ")
            while True:
                if LAN_ip_check(lan_subnet) is False:
                    print("Provided LAN Subnet is Incorrect, Please Try again!!")
                else:
                    x = LAN_ip_check(lan_subnet)  # returns only subnet of LAN network
                    break
                lan_subnet = input("Introduce your LAN subnet again: ")
            hosts = LAN_host(lan_subnet)
            P_CPE_LAN = hosts[3]
            BGP1 = hosts[0]
            BGP2 = hosts[1]
            BW = input('Introduce your Bandwidth in Mbps: ')
            while True:
                if Bandwidth(BW) is False:
                    print('Invalid Bandwidth')
                elif int(BW) <= 10:
                    non_asr_fc_low_bandwidth_b()
                elif int(BW) > 10:
                    non_asr_fc_highbandwidth_b()
                else:
                    break
                BW = input('Introduce your Bandwidth in Mbps again: ')
        else:
            print('Invalid options Selected !!')
            break
    Site_types()
    site_options = input("Enter your options again: ")
except KeyboardInterrupt:
    print("\n\nClosing down the Script, Something went Wrong!!\n\n")
