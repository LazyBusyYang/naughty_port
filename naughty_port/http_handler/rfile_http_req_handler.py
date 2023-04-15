# yapf: disable
import http.server
from xrprimer.utils.path_utils import Existence, check_path_existence

from naughty_port.utils.date_utils import (
    get_datetime_local, get_str_from_datetime,
)

# yapf: enable


class ReadFileHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Read file and return its content as response."""
    _FILE_PATH = ''

    def do_GET(self):
        """Handle GET request."""
        file_path = self.__class__._FILE_PATH
        if check_path_existence(file_path) == Existence.FileExist:
            with open(file_path, 'r') as f:
                port = f.read().strip()
            self.send_response(200)
        else:
            self.send_response(404)
            raise FileNotFoundError(f'File {file_path} does not exist')
        self.end_headers()
        datetime = get_datetime_local()
        time_str = get_str_from_datetime(datetime)
        message = f'Current date and time: {time_str}\n\n'
        message += f'Query result:\n{port}'
        self.wfile.write(bytes(message, 'utf8'))
