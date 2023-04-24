# yapf: disable
import argparse
import json
import os
from xrprimer.utils.log_utils import logging, setup_logger

from naughty_port.port_scheduler.builder import build_scheduler
from naughty_port.utils.config_utils import file2dict
from naughty_port.utils.date_utils import (
    get_datetime_local, get_str_from_datetime,
)

# yapf: enable


def main(args):
    # load config
    config = file2dict(args.config_path)
    # setup logger
    if not args.disable_log_file:
        datetime = get_datetime_local()
        time_str = get_str_from_datetime(datetime)
        log_dir = os.path.join('logs', f'run_scheduler_{time_str}')
        os.makedirs(log_dir)
    logger_path = None \
        if args.disable_log_file\
        else os.path.join(log_dir, 'main_log.txt')
    try:
        # XRPrimer 0.7.0+
        # logger for xrmocap
        logger = setup_logger(
            logger_name='run_scheduler',
            file_level=logging.DEBUG,
            console_level=logging.INFO,
            logger_path=logger_path)
    except TypeError:
        # use XRPrimer 0.6.x
        logger = setup_logger(
            logger_name='run_scheduler',
            logger_level=logging.DEBUG,
            logger_path=logger_path)
    logger.info('Main logger starts.')
    # build service
    config_str = json.dumps(config, indent=4)
    logger.debug(f'\nconfig:\n{config_str}')
    config['logger'] = logger
    scheduler = build_scheduler(config)
    scheduler.run()


def setup_parser():
    parser = argparse.ArgumentParser()
    # input args
    parser.add_argument(
        '--config_path',
        type=str,
        help='Path to service config file.',
        default='configs/nginx_scheduler.py')
    # log args
    parser.add_argument(
        '--disable_log_file',
        action='store_true',
        help='If checked, log will not be written as file.',
        default=False)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = setup_parser()
    main(args)
