import json
import typer
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

        self.fila_pessoas_doentes.canal.basic_qos(prefetch_count=1)
        self.fila_pessoas_doentes.canal.basic_consume(
            queue='pessoas_doentes',
            on_message_callback=self._recebe_pessoa_doente
        )
        self.fila_pessoas_doentes.canal.start_consuming()

    def _atende_pessoa(self):
        print(f' 🩺 {self.nome_pessoa} sendo atendida(o)...')
        sleep(0.25)
        self._examina_pessoa()

    def _examina_pessoa(self):
        self.doenca = self.pessoa['doenca']
        print(f' 🔬 {self.nome_pessoa} doença detectada: {self.doenca}')
        sleep(0.5)
        self._trata_pessoa()

    def _trata_pessoa(self):
        print(f' 💉 {self.nome_pessoa} sendo tratada(o)...')
        sleep(1)
        print(f' 😃 {self.nome_pessoa} tratada(o)!\n')
        self._ch.basic_ack(delivery_tag=self.method.delivery_tag)

    def _recebe_pessoa_doente(self, ch, method, properties, body):
        self.pessoa = json.loads(body.decode())
        self.nome_pessoa = self.pessoa['nome']
        self.cpf_pessoa = self.pessoa['cpf']

        self._ch = ch
        self.method = method

        print((f' 😷 {self.nome_pessoa} CPF: {self.cpf_pessoa} chegou ao '
               f'Hospital {self.nome}'))
        sleep(0.25)
        self._atende_pessoa()


def main(nome_hospital: str):
    Hospital(nome_hospital)


if __name__ == '__main__':
    typer.run(main)
