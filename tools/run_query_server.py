# yapf: disable
import argparse
import socketserver

from naughty_port.http_handler.rfile_http_req_handler import (
    ReadFileHttpRequestHandler,
)

# yapf: enable


def main(args):
    port = args.port_number
    Handler = ReadFileHttpRequestHandler
    Handler._FILE_PATH = args.port_path

    with socketserver.TCPServer(('0.0.0.0', port),
                                Handler,
                                bind_and_activate=False) as httpd:
        httpd.allow_reuse_address = True
        httpd.server_bind()
        httpd.server_activate()
        httpd.timeout = 1
        print('Serving at port', port)
        httpd.serve_forever()


def setup_parser():
    parser = argparse.ArgumentParser()
    # input args
    parser.add_argument(
        '--port_path',
        type=str,
        help='Path to port file.',
        default='logs/cur_port.txt')
    # server args
    parser.add_argument(
        '--port_number',
        type=int,
        help='Port number for http service.',
        default=8082)
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
