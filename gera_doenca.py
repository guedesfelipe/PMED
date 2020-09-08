import time
import sys
import argparse
from utils.utils import Fila
from utils.utils import GeraLog


def main(arguments):
    ''' Main '''

    parser = argparse.ArgumentParser(
        description='Script de apresentacao para geracao de pessoas doentes',
        add_help=True)

    # Quantidade de pessoas infectadas
    parser.add_argument(
        '--qtde_infct',
        '-q',
        action='store',
        type=int,
        default=1,
        help='Quantidade de pessoas infectadas')

    # Intervalo de tempo em segundos para infectar X pessoas
    parser.add_argument(
        '--interv_tempo',
        '-t',
        action='store',
        type=int,
        default=2,
        help='Intervalo de tempo (Em segundos) para infectar X pessoas')

    # Parser versão deste script
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    res_args = parser.parse_args(arguments)

    # Criando o log
    log = GeraLog(False, './log/doenca.log')

    try:
        fila_de_pessoas_doentes = Fila()
        fila_de_pessoas_doentes.cria_fila()

        qtde_pessoas_infect = 0

        while True:

            for i in range(res_args.qtde_infct):
                qtde_pessoas_infect += 1

                nome = 'Pessoa {}'.format(qtde_pessoas_infect)
                fila_de_pessoas_doentes.coloca_na_fila(nome)
                log.logger.info(' [-] {} infectada'.format(nome))
                time.sleep(0.001)

            time.sleep(res_args.interv_tempo)

    finally:
        fila_de_pessoas_doentes.desconecta()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
