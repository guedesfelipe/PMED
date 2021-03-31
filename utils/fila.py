import pika
from utils.metaclass import MetaSingleton


class Fila(metaclass=MetaSingleton):

    def __init__(self, host=None, fila=None):
        self.conexao = None
        self.host = host
        self.fila = fila
        self.canal = self.conecta()
        self.cria_fila()

    def conecta(self, host=None):

        if self.conexao is None:
            self.conexao = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=host if host else self.host
                )
            )

            self.canal = self.conexao.channel()
        return self.canal

    def desconecta(self):
        if not self.conexao.is_closed:
            self.conexao.close()

    def cria_fila(self):
        self.res = self.canal.queue_declare(
            queue=self.fila,
            durable=True
        )

    def inclui(self, texto):
        self.canal.basic_publish(
            exchange='',
            routing_key=self.fila,
            body=texto,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Fazendo a mensagem ficar persistente
            ))
        print(f' 😷 {texto} entrou na fila de {self.fila}')

    def total(self):
        return self.res.method.message_count
