# **Projeto de microserviço escalável com Docker**

Neste projeto visamos entender os conceitos aplicáveis de um projeto feito com microserviços que aumentam a performance e a escalabiladade dos negócios.

Este projeto é composto por um gerenciador de fila que será o `rabbitmq` onde tera **N´s** aplicações consumindo o conteúdo desta fila (Que neste exemplo será os `hospitais`) e **N´s** aplicações colocando conteúdo na fila (Que neste exemplo será as `doencas`)

## **Baixando o Projeto**

Para baixar o projeto basta realizar um `git pull` deste projeto ou realizar o download.

## **Instalando dependências**

Para este projeto você precisará ter instalado no ambiente o docker: https://docs.docker.com/get-docker/

## **Preparando o Ambiente**

Crie um diretório de log dentro da pasta raiz do projeto onde você salvou:

    mkdir log

Precisamos criar um container do rabbitmq para gerenciar nossa fila:

Para baixar a imagem do rabbitmq:

    docker pull rabbitmq

Para criar um container do rabbitmq:

    docker run -d --hostname my-rabbit --name rabbit13 -p 8080:15672 -p 5672:5672 -p 25676:25676 rabbitmq:3-management


Após isto entre na pasta raiz do projeto e execute o seguinte comando para criar uma imagem no docker do `hospital`: 

    docker build -t hospital -f docker/hospital/Dockerfile .

Após a criação da imagem do `hospital` vamos criar a imagem no docker de `doencas`:

    docker build -t doenca -f docker/doencas/Dockerfile .


Com as duas imagens criadas agora podemos subir quantos containers quisermos de cada imagem

* Exemplo de como criar um container da imagem do `hospital`:

        docker run -it -d --name hospital_1 -v PATH_DO_PROJETO/log/hospital_1:/hospital/log --entrypoint python --network host hospital:latest hospital.py

    > Trocar a variável ***PATH_DO_PROJETO*** para a pasta onde o projeto foi salvo em sua máquina

* Exemplo de como criar um container da imagem de `doenca`: 

        docker run -it -d --name COVID -v PATH_DO_PROJETO/log/COVID:/doenca/log --entrypoint python --network host doenca:latest gera_doenca.py -q 2 -t 1

    > Trocar a variável ***PATH_DO_PROJETO*** para a pasta onde o projeto foi salvo em sua máquina
