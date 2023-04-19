import random
import time
from typing import List, Union
from xrprimer.utils.log_utils import get_logger, logging

from naughty_port.utils.date_utils import datetime, get_datetime_utc
from ..port_manager.builder import BasePortManager, build_port_manager


class DayScheduler:

    def __init__(self,
                 black_list: List[int],
                 port_managers: List[BasePortManager],
                 date_port_base: int,
                 timezone_utc: int,
                 cur_port_path: Union[str, None] = None,
                 init_port: Union[int, None] = None,
                 logger: Union[None, str, logging.Logger] = None):
        """
        Args:
            period (float):
                Port refresh period in hours.
            black_list (List[int]):
                Black list of ports. Ports in this list will not be
                used.
            port_managers (List[BasePortManager]):
                Config dicts of port managers to manage ports.
            cur_port_path (Union[str, None], optional):
                Path to save current port.
                If None, will not be saved.
            init_port (Union[int, None], optional):
                Initial port, will be removed at its
                first run. Defaults to None.
            logger (Union[None, str, logging.Logger]):
                None for root logger. Besides, pass name of the
                logger or the logger itself.
                Defaults to None.
        """
        self.logger = get_logger(logger)
        self.last_port = init_port
        self.black_list = black_list
        self.manager_list = []
        for manager_cfg in port_managers:
            manager_cfg['logger'] = self.logger
            manager = build_port_manager(manager_cfg)
            self.manager_list.append(manager)
        self.base_manager = BasePortManager(
            name='base_manager_for_list', logger=self.logger)
        self.cur_port_path = cur_port_path
        self.date_port_base = date_port_base
        self.timezone_utc = timezone_utc
        # last time in hours
        self.last_date = None

    def run(self) -> None:
        while True:
            cur_datetime = get_datetime_utc(self.timezone_utc)
            date_str = f'{cur_datetime.month:02d}{cur_datetime.day:02d}'
            # The date has already been used, skip it
            if self.last_date is not None and date_str == self.last_date:
                dayend_datetime = datetime(
                    year=cur_datetime.year,
                    month=cur_datetime.month,
                    day=cur_datetime.day,
                    hour=23,
                    minute=59,
                    second=59)
                diff_datetime = \
                    dayend_datetime.replace(tzinfo=None) - \
                    cur_datetime.replace(tzinfo=None)
                time_to_sleep = diff_datetime.total_seconds() + 1
                time.sleep(time_to_sleep)
                continue
            port_info = self.base_manager.list_ports()
            self.last_date = date_str
            date_port = self.date_port_base + int(date_str)
            # date_port is occupied, use a random port
            if str(date_port) in port_info:
                while True:
                    random_port = random.randint(10000, 50000)
                    if random_port in self.black_list or \
                            str(random_port) in port_info:
                        continue
                    else:
                        break
                new_port = random_port
            else:
                new_port = date_port
            for manager in self.manager_list:
                if self.last_port is not None:
                    manager.remove_port(self.last_port)
                manager.add_port(new_port)
            if self.cur_port_path is not None:
                with open(self.cur_port_path, 'w') as f_write:
                    f_write.write(str(new_port))
            self.last_port = new_port
