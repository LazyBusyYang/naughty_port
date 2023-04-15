from naughty_port.utils.registry import Registry
from .hour_scheduler import HourScheduler

SCHEDULERS = Registry('schedulers')

SCHEDULERS.register_module(name='HourScheduler', module=HourScheduler)


def build_scheduler(cfg) -> HourScheduler:
    """Build scheduler."""
    return SCHEDULERS.build(cfg)
