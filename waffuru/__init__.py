from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from waffuru.utils import WaffuruLogger
import waffuru.browser as browser

logger = WaffuruLogger.get_logger()

class WindowSize:
    def __init__(self, w, h):
        self.w = w
        self.h = h

class WindowPosition:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class ClientAgent:
    def __init__(self, waffuru):
        self._waffuru = waffuru

    def __getattr__(self, name):
        def wrapper():
            pass

        return wrapper

class Waffuru:
    def __init__(self,
                 mode="chrome",
                 host="localhost",
                 port=8000,
                 size=WindowSize(800, 600),
                 position=WindowPosition(0, 0),
                 close_callback=None,
                 app_mode= True):
        self.mode = mode
        self.host = host
        self.port = port
        self.size = size
        self.position = position
        self.close_callback = close_callback
        self.app_mode = app_mode

        self._exposed_functions = {}

        self.app = Flask("Waffuru")
        self.app.config['SECRET_KEY'] = 'secret!'
        self.socketio = SocketIO(self.app)

        self.app.route("/")(self.index)
        self.socketio.on("my event")(self.test_message)


    def expose(self, name, func):
        if name in self._exposed_functions:
            logger.warning("{} is existing".format(name))

        self._exposed_functions[name] = func

    def get_agent(self):
        pass

    def index(self):
        return "Hello World"

    def test_message(self, message):
        emit('my response', {'data': 'got it!'})


if __name__ == '__main__':
    browser.open(["/"], {
        'mode': 'chrome',
        'host': 'localhost',
        'port': 5000,
        'app_mode': True,
        'cmdline_args': ['--disable-http-cache']
    })

