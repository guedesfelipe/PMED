import os
import requests
from time import sleep
from datetime import datetime


def main():

    while 1:
        os.system('clear')

        response = requests.get(
            'http://guest:guest@localhost:8080/api/queues/%2f/pessoas_doentes')
        data = response.json()

        now = datetime.now()
        hora = '(' + str(now.hour) + ':' + str(now.minute) + ':' + str(
            now.second) + ')'
        print('📊', hora, 'Total de pessoas doentes: {0}'.format(data['messages']))
        sleep(5)


if __name__ == '__main__':
    main()
