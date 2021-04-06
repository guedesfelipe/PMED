import logging
import logging.handlers


class GeraLog(object):

    def __init__(self, debug=False, path=None):
        self.debug = debug
        self.path = path

        formatter = logging.Formatter(
            '%(process)s - %(asctime)s | %(levelname)s - %(message)s',
            datefmt='%d-%m-%Y %H:%M:%S')
        self.logger = logging.getLogger('logger')
        self.logger.setLevel(logging.INFO)

        if not self.debug:
            rotation_handler = logging.handlers.TimedRotatingFileHandler(
                self.path,
                when='midnight', backupCount=7)
            rotation_handler.setFormatter(formatter)
            self.logger.addHandler(rotation_handler)
        else:
            console_debug = logging.StreamHandler()
            console_debug.setFormatter(formatter)
            self.logger.addHandler(console_debug)
