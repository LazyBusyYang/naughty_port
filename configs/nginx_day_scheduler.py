type = 'DayScheduler'
init_port = None
black_list = [
    23333,
]
date_port_base = 20000
timezone_utc = 8
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
