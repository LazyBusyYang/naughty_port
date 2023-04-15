type = 'HourScheduler'
period = 24
init_port = None
black_list = [
    23333,
]
cur_port_path = 'logs/cur_port.txt'
port_managers = [
    dict(
        type='CentOSFirewallPortManager',
        name='firewall_manager',
    ),
    dict(
        type='NginxPortManager',
        name='nginx_manager',
        nginx_conf_path='/etc/nginx/nginx.conf',
    )
]
