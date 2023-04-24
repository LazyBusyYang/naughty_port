## Introduction
The main purpose of this project is to update the ports of a series of services regularly, to avoid being tracked or blocked.

## Installation
```bash
pip install git+https://github.com/LazyBusyYang/naughty_port.git
```

## Set period
Edit `configs/nginx_hour_scheduler.py` and set `period` value in hours. It will write
the current port in use to the file defined by `cur_port_path`.

## Start naughty_port
```bash
python tools/run_scheduler.py --config_path configs/nginx_hour_scheduler.py
```

## Show port
Start an http server and show the current port in use.
```bash
python tools/run_query_server.py --port_path logs/cur_port.txt --port_number 80
```

## Supported services
CentOS firewall, nginx.
