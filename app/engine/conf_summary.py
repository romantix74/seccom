#!/usr/bin/python3

mgmt_servers = '62.212.85.101,85.17.178.20,88.198.246.60'
radius_server = '88.198.246.49'
zabbix_server = '88.198.246.38'
subnet_octet = 8
# generate iptables config
def generate(servers, net_card):
    
    out_conf = [] 
    
	
    # tcp section
    for i,server in enumerate(servers):
        #eth0:0  85.17.178.25              openvpn2.conf  tun2   10.8.25.0/24   mgmt_port 1152
        out_conf.append('{0}     {1}           openvpn{2}.conf  tun{3}   10.{4}.{5}.0/24    mgmt_port {6}'.format(net_card+':'+str(i), server, i,i, subnet_octet, i, 1150+i)) 

    # udp section
    for i,server in enumerate(servers):
        #eth0:0  85.17.178.25              openvpn2.conf  tun2   10.8.25.0/24   mgmt_port 1152
        out_conf.append('{0}     {1}           openvpn{2}.conf  tun{3}   10.{4}.{5}.0/24    mgmt_port {6}'.format(net_card+':'+str(i), server, i+100,i+100, subnet_octet, i+100, 1150+i+100)) 
                

    return out_conf

if __name__ == '__main__':
    servers = ['1.2.3.4', '5.5.6.6']
    
    test_out = generate(servers, 'eth0') 
    #print(test_out)
    for row in test_out:
        print(row)
        
        