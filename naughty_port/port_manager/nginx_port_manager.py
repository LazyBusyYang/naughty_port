# yapf: disable
import os
import subprocess
from typing import Union
from xrprimer.utils.log_utils import logging

from .base_port_manager import BasePortManager

# yapf: enable


class NginxPortManager(BasePortManager):
    _RELOAD_PORT_COMMAND = ['systemctl', 'restart', 'nginx']
    _LIST_PORT_COMMAND = ['netstat', '-ntlp']

    def __init__(self,
                 nginx_conf_path: str,
                 logger: Union[None, str, logging.Logger] = None):
        """
        Args:
            logger (Union[None, str, logging.Logger]):
                None for root logger. Besides, pass name of the
                logger or the logger itself.
                Defaults to None.
        """
        BasePortManager.__init__(self, logger)
        self.nginx_conf_path = nginx_conf_path

    def add_port(self, port: int) -> None:
        """Add port to this service.

        Args:
            port (int):
                Port to add.
        """
        with open(self.nginx_conf_path, 'r') as f_read:
            lines = f_read.readlines()
        new_lines = []
        for line in lines:
            if line.strip().startswith('listen'):
                new_line = f'    listen       {str(port)} ssl http2;\n'
            else:
                new_line = line
            new_lines.append(new_line)
        os.remove(self.nginx_conf_path)
        with open(self.nginx_conf_path, 'w') as f_write:
            for line in new_lines:
                f_write.write(line)
        self.reload_ports()
        port_info = self.list_ports()
        '0.0.0.0:23334'
        lines = port_info.split('\n')
        new_port_found = False
        for line in lines:
            if str(port) in line and 'nginx' in line:
                new_port_found = True
                break
        if not new_port_found:
            self.logger.error(
                f'Port {port} cannot be found in nignx after adding it.\n' +
                'Output of listing ports:\n' + f'{port_info}')
            raise RuntimeError
        return

    def reload_ports(self) -> None:
        """Reload this service to activate the port setting."""
        cmd_str = ' '.join(self._RELOAD_PORT_COMMAND)
        self.logger.info('Reloading nginx with command:\n' + f' {cmd_str}')
        process = subprocess.Popen(
            self._RELOAD_PORT_COMMAND,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        process.wait()
        return

    def list_ports(self) -> str:
        """List all ports in this service.

        Returns:
            str:
                A String for port information.
        """
        cmd_str = ' '.join(self._LIST_PORT_COMMAND)
        self.logger.info('Listing ports in firewall with command:\n' +
                         f' {cmd_str}')
        process = subprocess.Popen(
            self._LIST_PORT_COMMAND, stdout=subprocess.PIPE)
        process.wait()
        out, _ = process.communicate()
        return out.decode('utf-8')
