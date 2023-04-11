from mmcv.utils import Registry

from .base_port_manager import BasePortManager
from .centos_firewall_port_manager import CentOSFirewallPortManager
from .nginx_port_manager import NginxPortManager

PORT_MANAGERS = Registry('port_manager')

PORT_MANAGERS.register_module(
    name='CentOSFirewallPortManager', module=CentOSFirewallPortManager)
PORT_MANAGERS.register_module(name='NginxPortManager', module=NginxPortManager)


def build_port_manager(cfg) -> BasePortManager:
    """Build port_manager."""
    return PORT_MANAGERS.build(cfg)
