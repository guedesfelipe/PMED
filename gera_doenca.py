import json
import typer
from utils.fila import Fila
from time import sleep
from faker import Faker


class Doenca(object):
    def __init__(self, nome=None):
        self.nome = nome
        # Cria a fila de pessoas doentes caso não exista ainda
        self.fila_pessoas_doentes = Fila(
            host='localhost',
            fila='pessoas_doentes'
        )
        self.qtde_pessoas_infectadas = 0

        print(45*'-')
        print(f' 🦠 {self.nome} criado e pronto para infectar...')
        print(45*'-')

    def infecta_pessoa(self):
        # Cria uma pessoa aleatória para ser infectada
        self._cria_pessoa()

        # Coloca uma pessoa na fila de pessoas doentes
        self.fila_pessoas_doentes.inclui(
            json.dumps(self.pessoa, ensure_ascii=False)
        )

        # Incrementa o contador de pessoas infectadas
        self.qtde_pessoas_infectadas += 1

    def _cria_pessoa(self):
        _pessoa_fake = Faker(['pt_BR'])

        self.pessoa = {
            'cpf': _pessoa_fake.cpf(),
            'nome': _pessoa_fake.name(),
            'doenca': self.nome
        }

    def get_total_pessoas_infectadas(self):
        return self.qtde_pessoas_infectadas


def main(nome_doenca: str, taxa_infec_seg: int = 1):
    doenca = Doenca(nome_doenca)

    while 1:
        doenca.infecta_pessoa()
        sleep(taxa_infec_seg)


if __name__ == '__main__':
    typer.run(main)
