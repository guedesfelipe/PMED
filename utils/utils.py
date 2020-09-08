import pika
import logging
import logging.handlers


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                MetaSingleton, cls).__call__(
                *args, **kwargs)
        return cls._instances[cls]


class Fila(metaclass=MetaSingleton):

    def __init__(self, conexao=None):
        self.conexao = conexao
        self.canal = self.conecta()

    def conecta(self):
        if self.conexao is None:
            self.conexao = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost'))
            self.canal = self.conexao.channel()
        return self.canal

    def desconecta(self):
        if not self.conexao.is_closed:
            self.conexao.close()

    def cria_fila(self):
        self.canal.queue_declare(queue='pessoas_doentes', durable=True)

    def coloca_na_fila(self, texto):
        self.canal.basic_publish(
            exchange='',
            routing_key='pessoas_doentes',
            body=texto,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Fazendo a mensagem ficar persistente
            ))
        print(' [x] {} entrou na fila de pessoas doentes'.format(texto))


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
