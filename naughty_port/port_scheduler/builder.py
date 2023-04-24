from naughty_port.utils.registry import Registry
from .day_scheduler import DayScheduler
from .hour_scheduler import HourScheduler

SCHEDULERS = Registry('schedulers')

SCHEDULERS.register_module(name='HourScheduler', module=HourScheduler)
SCHEDULERS.register_module(name='DayScheduler', module=DayScheduler)


def build_scheduler(cfg) -> HourScheduler:
    """Build scheduler."""
    return SCHEDULERS.build(cfg)
