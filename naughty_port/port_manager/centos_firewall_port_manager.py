# yapf: disable
import subprocess
from typing import Union
from xrprimer.utils.log_utils import logging

from .base_port_manager import BasePortManager

# yapf: enable


class CentOSFirewallPortManager(BasePortManager):
    _ADD_PORT_COMMAND = [
        'firewall-cmd', '--zone=public', '--add-port=PORT_TO_ADD/tcp',
        '--permanent'
    ]
    _REMOVE_PORT_COMMAND = [
        'firewall-cmd', '--zone=public', '--remove-port=PORT_TO_REMOVE/tcp',
        '--permanent'
    ]
    _RELOAD_PORT_COMMAND = ['firewall-cmd', '--reload']
    _LIST_PORT_COMMAND = ['firewall-cmd', '--list-all']

    def __init__(self,
                 name: str,
                 logger: Union[None, str, logging.Logger] = None):
        """
        Args:
            name (str):
                Name of this port manager.
            logger (Union[None, str, logging.Logger]):
                None for root logger. Besides, pass name of the
                logger or the logger itself.
                Defaults to None.
        """
        BasePortManager.__init__(self, name=name, logger=logger)

    def add_port(self, port: int) -> None:
        """Add port to firewall.

        Args:
            port (int):
                Port to add.
        """
        command = self._ADD_PORT_COMMAND.copy()
        for idx, arg in enumerate(command):
            if 'PORT_TO_ADD' in arg:
                arg = arg.replace('PORT_TO_ADD', str(port))
                command[idx] = arg
        cmd_str = ' '.join(command)
        self.logger.info(f'Adding port {port} to firewall with command:\n' +
                         f' {cmd_str}')
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        self.reload_ports()
        port_info = self.list_ports()
        if f'{port}/tcp' not in port_info:
            self.logger.error(
                f'Port {port} not found in firewall after adding it.\n' +
                'Output of listing ports:\n' + f'{port_info}')
            raise RuntimeError
        return

    def remove_port(self, port: int) -> None:
        """Remove port from firewall.

        Args:
            port (int):
                Port to remove.
        """
        command = self._REMOVE_PORT_COMMAND.copy()
        for idx, arg in enumerate(command):
            if 'PORT_TO_REMOVE' in arg:
                arg = arg.replace('PORT_TO_REMOVE', str(port))
                command[idx] = arg
        cmd_str = ' '.join(command)
        self.logger.info(
            f'Removing port {port} from firewall with command:\n' +
            f' {cmd_str}')
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        self.reload_ports()
        port_info = self.list_ports()
        if f'{port}/tcp' in port_info:
            self.logger.error(
                f'Port {port} still found in firewall after removing it.\n' +
                'Output of listing ports:\n' + f'{port_info}')
            raise RuntimeError
        return

    def reload_ports(self) -> None:
        """Reload firewall."""
        cmd_str = ' '.join(self._RELOAD_PORT_COMMAND)
        self.logger.info('Reloading firewall with command:\n' + f' {cmd_str}')
        process = subprocess.Popen(
            self._RELOAD_PORT_COMMAND,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        process.wait()

    def list_ports(self) -> str:
        """List all ports in firewall.

        Returns:
            str:
                Ports in firewall.
        """
        cmd_str = ' '.join(self._LIST_PORT_COMMAND)
        self.logger.info('Listing ports in firewall with command:\n' +
                         f' {cmd_str}')
        process = subprocess.Popen(
            self._LIST_PORT_COMMAND, stdout=subprocess.PIPE)
        process.wait()
        out, _ = process.communicate()
        return out.decode('utf-8')
