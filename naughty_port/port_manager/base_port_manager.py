import subprocess
from typing import Union
from xrprimer.utils.log_utils import get_logger, logging


class BasePortManager:
    _LIST_PORT_COMMAND = ['netstat', '-ntlp']

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
        self.name = name
        self.logger = get_logger(logger)

    def add_port(self, port: int) -> None:
        """Add port to this service.

        Args:
            port (int):
                Port to add.
        """
        return

    def remove_port(self, port: int) -> None:
        """Remove port from this service.

        Args:
            port (int):
                Port to remove.
        """
        return

    def reload_ports(self) -> None:
        """Reload this service to activate the port setting."""
        return

    def list_ports(self) -> str:
        """List all ports in use.

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
