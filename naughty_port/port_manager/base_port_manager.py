from typing import Union
from xrprimer.utils.log_utils import get_logger, logging


class BasePortManager:

    def __init__(self, logger: Union[None, str, logging.Logger] = None):
        """
        Args:
            logger (Union[None, str, logging.Logger]):
                None for root logger. Besides, pass name of the
                logger or the logger itself.
                Defaults to None.
        """
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
        """List all ports in this service.

        Returns:
            str:
                A String for port information.
        """
        return ''
