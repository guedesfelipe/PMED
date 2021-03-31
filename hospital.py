import json
from utils.fila import Fila
from time import sleep


class Hospital(object):
    def __init__(self, nome=None):
        self.nome = nome

        # Cria a fila de pessoas doentes caso não exista ainda
        self.fila_pessoas_doentes = Fila(
            host='localhost',
            fila='pessoas_doentes'
        )
        self.qtde_pessoas_tratadas = 0

        print(45*'-')
        print(f' 🏥 Esperando pessoas no Hospital {self.nome}')
        print(45*'-')
        print(str(self.fila_pessoas_doentes.total()))

        self.fila_pessoas_doentes.canal.basic_qos(prefetch_count=1)
        self.fila_pessoas_doentes.canal.basic_consume(
            queue='pessoas_doentes',
            on_message_callback=self._recebe_pessoa_doente
        )
        self.fila_pessoas_doentes.canal.start_consuming()

    def _trata_pessoa(self, ch, method):
        print(f' 💉 {self.pessoa} sendo tratada...')
        sleep(2)
        print(f' 😃 {self.pessoa} tratada!\n')
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def _recebe_pessoa_doente(self, ch, method, properties, body):
        self.pessoa = json.loads(body.decode())
        print(f' 😷 {self.pessoa} chegou ao Hospital {self.nome}')
        self._trata_pessoa(ch, method)


def main():
    Hospital('Unimed')


if __name__ == '__main__':
    main()
