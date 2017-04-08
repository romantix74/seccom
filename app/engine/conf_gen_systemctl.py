#!/usr/bin/python3

mgmt_servers = '62.212.85.101,85.17.178.20,88.198.246.60'
radius_server = '88.198.246.49'
zabbix_server = '88.198.246.38'
subnet_octet = 8
# generate iptables config
def generate(i):
    
    out_conf = [] 
    
    out_conf.append('[Unit]\n') 
    out_conf.append('Description=OpenVPN Robust And Highly Flexible Tunneling Application\n') 
    out_conf.append('After=syslog.target network.target\n\n') 
    out_conf.append('[Service]\n') 
    out_conf.append('Type=forking\n') 
    out_conf.append('ExecStart=/usr/sbin/openvpn --daemon --cd /etc/openvpn/ --config openvpn{0}.conf\n\n'.format(i)) 
    out_conf.append('[Install]\n') 
    out_conf.append('WantedBy=multi-user.target\n') 
    
    return out_conf

if __name__ == '__main__':
    
    
    test_out = generate('1') 
    print(test_out)
    print('--------')
    test_out = generate('1_udp') 
    print(test_out)
    
        
        