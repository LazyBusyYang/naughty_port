import random
import time
from typing import List, Union
from xrprimer.utils.log_utils import get_logger, logging

from ..port_manager.builder import BasePortManager, build_port_manager


class HourScheduler:

    def __init__(self,
                 period: float,
                 black_list: List[int],
                 port_managers: List[BasePortManager],
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
        # period in hours
        self.period = period
        self.manager_list = []
        for manager_cfg in port_managers:
            manager_cfg['logger'] = self.logger
            manager = build_port_manager(manager_cfg)
            self.manager_list.append(manager)
        self.base_manager = BasePortManager(
            name='base_manager_for_list', logger=self.logger)
        self.cur_port_path = cur_port_path
        # last time in hours
        self.last_time = None

    def run(self) -> None:
        while True:
            cur_time = time.time()
            if self.last_time is not None:
                expect_time_h = self.last_time + self.period
                expect_time_s = _hour_to_second(expect_time_h)
                if cur_time < expect_time_s:
                    time_to_sleep = expect_time_s - cur_time
                    time.sleep(time_to_sleep)
                    continue
            self.last_time = _second_to_hour(cur_time)
            port_info = self.base_manager.list_ports()
            while True:
                random_port = random.randint(10000, 50000)
                if random_port in self.black_list or \
                        str(random_port) in port_info:
                    continue
                else:
                    break
            new_port = random_port
            for manager in self.manager_list:
                if self.last_port is not None:
                    manager.remove_port(self.last_port)
                manager.add_port(new_port)
            if self.cur_port_path is not None:
                with open(self.cur_port_path, 'w') as f_write:
                    f_write.write(str(new_port))
            self.last_port = new_port


def _hour_to_second(hour: float) -> float:
    return hour * 60 * 60


def _second_to_hour(second: float) -> float:
    return second / 60 / 60
