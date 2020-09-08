import time
from utils.utils import Fila
from utils.utils import GeraLog


log = None


def callback(ch, method, properties, body):
    ''' Callback '''

    global log

    log.logger.info(' [x] {} chegou ao Hospital'.format(body.decode()))
    time.sleep(3)
    log.logger.info(' [x] {} tratada!!'.format(body.decode()))
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    ''' Main '''

    global log

    fila_pessoas_doentes = Fila()
    fila_pessoas_doentes.cria_fila()

    # Criando o log
    log = GeraLog(False, './log/hospital.log')

    log.logger.info(
        ' [*] Esperando pessoas no Hospital. Aperte CTRL+C para sair')

    fila_pessoas_doentes.canal.basic_qos(prefetch_count=1)
    fila_pessoas_doentes.canal.basic_consume(
        queue='pessoas_doentes', on_message_callback=callback)
    fila_pessoas_doentes.canal.start_consuming()


if __name__ == '__main__':
    main()
