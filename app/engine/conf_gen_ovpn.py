#!/usr/bin/python3
import os
import random
from . import conf_gen_systemctl

out_dir = '/home/master/scripts/out_config'

#radius_secret =  ''.join([random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')) for x in range(12)])   #'j13vTiuuaRKE3KCGq2xt'
radius_secret = 'e4TgtR0nDz5atpt3IU4O'
# const for ovpn subnet 10.8.X.X
subnet_octet = 8

def generate_ovpn(s, i , tcp_or_udp, appendix):
    out_conf = []    
    out_conf.append('local {0}\n'.format(s))       
    out_conf.append('management 127.0.0.1 {0}\n'.format(1150 + i))
    out_conf.append('port 443\n')
    out_conf.append('proto {0}\n'.format(tcp_or_udp))
    out_conf.append('dev tun{0}\n'.format(i))
    out_conf.append('ca ca.crt\n')
    out_conf.append('cert server2.crt\n')
    out_conf.append('key server2.key\n')
    out_conf.append('dh dh2048.pem\n')
    out_conf.append('server 10.{0}.{1}.0 255.255.255.0\n'.format(subnet_octet,i))
    out_conf.append('push "route 10.{0}.{1}.0 255.255.255.0"\n'.format(subnet_octet, i))
    out_conf.append('push "redirect-gateway def1"\n')
    out_conf.append('push "dhcp-option DNS 8.8.8.8"\n')
    out_conf.append('push "dhcp-option DNS 8.8.4.4"\n')
    out_conf.append('#keepalive 10 120\n')
    out_conf.append('ping 10\n')
    out_conf.append('ping-exit 60\n')    
    out_conf.append('#reneg-sec 0\n')
    out_conf.append('tcp-queue-limit 256\n')
    out_conf.append('tun-mtu 1500\n')
    out_conf.append('comp-lzo\n')
    out_conf.append('user nobody\n')
    out_conf.append('group nogroup\n')
    out_conf.append('persist-key\n')
    out_conf.append('persist-tun\n')
    out_conf.append('#status /etc/openvpn/log/openvpn-status{0}.log\n'.format(appendix))
    out_conf.append('#log /etc/openvpn/log/openvpn{0}.log\n'.format(appendix))
    out_conf.append('#verb 1\n')
    out_conf.append('plugin /etc/openvpn/radiusplugin{0}.so /etc/openvpn/radiusplugin{1}.cnf\n'.format(appendix,appendix))
    out_conf.append('push "block-outside-dns"\n')
    out_conf.append('reneg-sec 43200\n')
    out_conf.append('cipher AES-256-CBC\n')

    return out_conf

def generate_rad(server, i , appendix):
    
    out_conf_radplugin = [] 
    out_conf_radplugin.append('NAS-Identifier=OpenVpn\n')
    out_conf_radplugin.append('Service-Type=5\n')
    out_conf_radplugin.append('Framed-Protocol=1\n')
    out_conf_radplugin.append('NAS-Port-Type=5\n')
    out_conf_radplugin.append('NAS-IP-Address={0}\n'.format(server))
    out_conf_radplugin.append('OpenVPNConfig=/etc/openvpn/openvpn{0}.conf\n'.format(appendix))
    out_conf_radplugin.append('subnet=255.255.255.0\n')
    out_conf_radplugin.append('overwriteccfiles=true\n')
    out_conf_radplugin.append('nonfatalaccounting=false\n')
    out_conf_radplugin.append('server\n')
    out_conf_radplugin.append('{\n')
    out_conf_radplugin.append('acctport=1813\n')
    out_conf_radplugin.append('authport=1812\n')
    out_conf_radplugin.append('name=88.198.246.49\n')
    out_conf_radplugin.append('retry=3\n')
    out_conf_radplugin.append('wait=3\n')
    out_conf_radplugin.append('sharedsecret={0}\n'.format(radius_secret))
    out_conf_radplugin.append('}')

    return out_conf_radplugin

def generate( servers ):  #,   #tcp_or_udp = 'tcp'):   # 444 
    
    # output config for single server ip
    out_dict = {}
    out_conf = []               # config for openvpn
    out_conf_radplugin = []     # config for radiusplugin
    
    for i,s in enumerate(servers):
        # appendix for filename
        appendix_tcp =  str(i) 
        appendix_udp =  str(i) + '_udp'

        ovpn_tcp = generate_ovpn(s, i , 'tcp', appendix_tcp)
        ovpn_udp = generate_ovpn(s, i+100 , 'udp', appendix_udp)
        ovpn_rad_tcp = generate_rad(s, i , appendix_tcp)  #out_conf_radplugin
        ovpn_rad_udp = generate_rad(s, i , appendix_udp)

        out_dict[s] = ovpn_tcp 
        out_dict[s + '_udp'] = ovpn_udp   # name for udp diff by 100
        
        out_dict['{}_radplg'.format(s)] =  ovpn_rad_tcp
        out_dict['{}_radplg'.format(s + '_udp')] = ovpn_rad_udp 

        # write files        
        fileOvpn_tcp = os.path.join(out_dir, 'openvpn{0}.conf'.format(appendix_tcp))
        fileRadiusPlugin_tcp = os.path.join(out_dir, 'radiusplugin{0}.cnf'.format(appendix_tcp))
        fileOvpn_udp = os.path.join(out_dir, 'openvpn{0}.conf'.format(appendix_udp))
        fileRadiusPlugin_udp = os.path.join(out_dir, 'radiusplugin{0}.cnf'.format(appendix_udp))
        with open(fileOvpn_tcp, 'w', encoding='utf-8') as f:
            f.writelines(ovpn_tcp)
        with open(fileRadiusPlugin_tcp, 'w', encoding='utf-8') as f:
            f.writelines(ovpn_rad_tcp)
        with open(fileOvpn_udp, 'w', encoding='utf-8') as f:
            f.writelines(ovpn_udp)
        with open(fileRadiusPlugin_udp, 'w', encoding='utf-8') as f:
            f.writelines(ovpn_rad_udp)    

        #systemd files
        fileSystemd_tcp = os.path.join(out_dir, 'openvpn{0}.service'.format(appendix_tcp))
        with open(fileSystemd_tcp, 'w', encoding='utf-8') as f:
            f.writelines(conf_gen_systemctl.generate(appendix_tcp))

        fileSystemd_udp = os.path.join(out_dir, 'openvpn{0}.service'.format(appendix_udp))
        with open(fileSystemd_udp, 'w', encoding='utf-8') as f:
            f.writelines(conf_gen_systemctl.generate(appendix_udp))

    # iptables
    #out_dict['iptables'] = ovpn_tcp

    return out_dict

if __name__ == '__main__':
    servers = ['1.2.3.4', '5.5.6.6']
    
    test_out = generate(servers) 
    print(test_out)
    for key,row in test_out.items():
        print(key)
        print('--------------------')
        for v in row:
             print(v)
      #  print(value)