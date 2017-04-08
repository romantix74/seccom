#!/usr/bin/python3

mgmt_servers = '62.212.85.101,85.17.178.20,88.198.246.60'
radius_server = '88.198.246.49'
zabbix_server = '88.198.246.38'
subnet_octet = 8
# generate iptables config
def generate_iptables(servers, net_card):
    
    out_conf = [] 
    out_conf.append('iptables -A INPUT -p icmp -j ACCEPT\n')
    out_conf.append('iptables -A INPUT -s 127.0.0.0/8 -i lo -j ACCEPT\n')
    out_conf.append('iptables -A INPUT -p tcp -m tcp --dport 80 -m state --state NEW,ESTABLISHED -m comment --comment "web-server speedtest" -j ACCEPT\n')
    out_conf.append('iptables -A INPUT -s {0}/32 -m state --state NEW,ESTABLISHED -m comment --comment "Zabbix server" -j ACCEPT\n'.format(zabbix_server))
    out_conf.append('iptables -A INPUT -s {0}/32 -p tcp -m tcp --dport 22 -m state --state NEW,ESTABLISHED -m comment --comment "ssh mgmt" -j ACCEPT\n'.format(mgmt_servers))
    out_conf.append('iptables -A INPUT -p tcp -m tcp --dport 443 -m comment --comment "tcp OpenVPN" -j ACCEPT')
    out_conf.append('iptables -A INPUT -p udp -m udp --dport 443 -m comment --comment "udp OpenVPN" -j ACCEPT')
    out_conf.append('iptables -A INPUT -s {0}/32 -p udp -m udp --sport 1812:1813 -m comment --comment "Взаимодействие с FreeRADIUS" -j ACCEPT'.format(radius_server))
    out_conf.append('iptables -A INPUT -p udp -m udp --sport 53 -m state --state ESTABLISHED -m comment --comment "DNS запросы" -j ACCEPT')
    out_conf.append('iptables -A INPUT -p tcp -m tcp --sport 53 -m state --state ESTABLISHED -m comment --comment "DNS запросы" -j ACCEPT')
    out_conf.append('iptables -A INPUT -p udp -m udp --sport 123 -m state --state ESTABLISHED -m comment --comment "NTP запросы" -j ACCEPT')

    out_conf.append('iptables -A FORWARD -p tcp -m tcp --tcp-flags SYN,RST SYN -m comment --comment "Path MTU discovery (RFC 1191)" -j TCPMSS –clamp-mss-to-pmtu')
	
    out_conf.append('iptables -A OUTPUT -d 127.0.0.0/8 -o lo -j ACCEPT')
    out_conf.append('iptables -A OUTPUT -p icmp -m comment --comment "исходящие пинги" -j ACCEPT')
    out_conf.append('iptables -A OUTPUT -p udp --dport 33435: -m comment --comment "traceroute" -j ACCEPT')
    out_conf.append('iptables -A OUTPUT -p tcp -m state --state ESTABLISHED -m comment --comment "Обратный траффик" -j ACCEPT')
    out_conf.append('iptables -A OUTPUT -p udp -m state --state ESTABLISHED -m comment --comment "Обратный траффик" -j ACCEPT')
    out_conf.append('iptables -A OUTPUT -d {0}/32  -m comment --comment "Zabbix сервер" -j ACCEPT'.format(zabbix_server))
    out_conf.append('iptables -A OUTPUT -d {0}/32 -p udp -m udp --dport 1812:1813 -m comment --comment "Взаимодействие с FreeRADIUS" -j ACCEPT'.format(radius_server))
    out_conf.append('iptables -A OUTPUT -p udp -m udp --dport 53 -m state --state NEW,ESTABLISHED -m comment --comment "DNS запросы" -j ACCEPT')
    out_conf.append('iptables -A OUTPUT -p tcp -m tcp --dport 53 -m state --state NEW,ESTABLISHED -m comment --comment "DNS запросы" -j ACCEPT')
    out_conf.append('iptables -A OUTPUT -p udp -m udp --dport 123 -m state --state NEW,ESTABLISHED -m comment --comment "NTP запросы" -j ACCEPT')
	
    # NAT section
    for i,server in enumerate(servers):
        out_conf.append('iptables -t nat -A POSTROUTING -s 10.{0}.{1}.0/24 -o {2} -j SNAT --to-source {3}'.format(subnet_octet, i, net_card, server)) 
        out_conf.append('iptables -t nat -A POSTROUTING -s 10.{0}.{1}.0/24 -o {2} -j SNAT --to-source {3}'.format(subnet_octet, i+100, net_card,server))        

    return out_conf

if __name__ == '__main__':
    servers = ['1.2.3.4', '5.5.6.6']
    
    test_out = generate_iptables(servers, 'eth0') 
    #print(test_out)
    for row in test_out:
        print(row)
        
        