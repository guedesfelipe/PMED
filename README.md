# ✨ **Projeto de microserviço escalável com Docker** 🐳

Neste projeto visamos entender os conceitos aplicáveis de um projeto feito com microserviços que aumentam a performance e a escalabiladade dos negócios.

Este projeto é composto por um gerenciador de fila que será o `rabbitmq` onde tera **N´s** aplicações consumindo o conteúdo desta fila (Que neste exemplo será o `hospital`) e **N´s** aplicações colocando conteúdo na fila (Que neste exemplo será a `doenca`)

## 📥 **Baixando o Projeto**

Para baixar o projeto basta realizar um `git clone https://github.com/guedesfelipe/PMED.git` deste projeto ou realizar o download manualmente.

## 🔧 **Preparando o Ambiente**

## :whale2: [Docker](https://www.docker.com/)

### :penguin: Linux

<details><p><summary>Guia de instalação para distribuições Debian &#10549;</p></summary>

1. Instalando o curl caso não tenha instalado na máquina ainda:

    ~~~sh
    sudo apt install curl
    ~~~

1. Download do instalador docker:

    ~~~sh
    curl -fsSL https://get.docker.com -o get-docker.sh
    ~~~

1. Executando o script do instalador baixado acima:

    ~~~sh
    sudo sh get-docker.sh
    ~~~

1. Verificando se foi instalado corretamente e qual a versão que instalamos:

    ~~~sh
    sudo docker --version
    ~~~

1. Agora vamos ver se o docker consegue subir um container com o comando abaixo:

    ~~~sh
    sudo docker run --rm hello-world
    ~~~

    > :loudspeaker: Este comando irá baixar uma imagem docker de hello world, e o parâmetro `--rm` significa que irá excluir este container assim que terminar a execução. Para mais detalhes digite: `sudo docker run --help` que irá mostrar mais detalhadamente todos os parâmetros, inclusive o `--rm`.

1. Para conseguirmos executar o docker sem precisar do `sudo`:

    ~~~sh
    sudo usermod -aG docker $USER
    ~~~

    ~~~sh
    newgrp docker
    ~~~

1. Para testar e listar os containers ativos:

    ~~~sh
    docker ps
    ~~~

1. Listando todos os containers (Ativos e Inativos):

    ~~~sh
    docker ps -a
    ~~~

</details>

### :computer: Windows

<details><p><summary>Guia de instalação para Windowns &#10549;</p></summary>

[Manual oficial de instalação do docker para Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows)

[Clique aqui para baixar o instalador do docker para Windows](https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe)

</details>

### :apple: Mac

<details><p><summary>Guia de instalação para Mac &#10549;</p></summary>

[Manual oficial de instalação do docker para Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac)

[Clique aqui para baixar o instalador do docker para Mac](https://desktop.docker.com/mac/stable/Docker.dmg)

</details>

## 🚀 **Rodando a Aplicação**

Precisamos criar um container do `rabbitmq` para gerenciar nossa fila:

Para criar um container do rabbitmq (Caso não tenha a imagem do rabbitmq ele vai
baixar):

    docker run -d --hostname my-rabbit --name rabbitMQ -p 8080:15672 -p 5672:5672 -p 25676:25676 rabbitmq:3-management

> ⚠️ Pode ser necessário acesso root

Criando uma virtual env na raiz do projeto:

    python3 -m venv venv

Ativar a virtual env criada:

    source venv/bin/activate

Instalando dependencias do python:

    pip install -r requirements.txt

Após isto na pasta raiz do projeto, execute o seguinte comando para criar uma imagem no docker do `hospital`:

### 📜 controla_containers.py

    python controla_containers.py build hospital

### 🐳

    docker build -t hospital -f docker/hospital/Dockerfile .

Após a criação da imagem do `hospital` vamos criar a imagem no docker de `doenca`:

### 📜 controla_containers.py

    python controla_containers.py build doenca

### 🐳

    docker build -t doenca -f docker/doenca/Dockerfile .


Com as duas imagens criadas agora podemos subir quantos containers quisermos de cada imagem

* Exemplo de como criar um container da imagem do `hospital`:

### 📜 controla_containers.py

    python controla_containers.py run hospital NOME_HOSPITAL

### 🐳

        docker run -it -d --name hospital_1 --entrypoint python --network host hospital:latest gera_hospital.py

> ⚠️ Trocar a variável ***PATH_DO_PROJETO*** para a pasta onde o projeto foi salvo em sua máquina

* Exemplo de como criar um container da imagem de `doenca`: 

### 📜 controla_containers.py

    python controla_containers.py run doenca NOME_DOENCA TAXA_INFEC_SEG


### 🐳

        docker run -it -d --name COVID --entrypoint python --network host doenca:latest gera_doenca.py --taxa-infec-seg 1

> ⚠️ Trocar a variável ***PATH_DO_PROJETO*** para a pasta onde o projeto foi salvo em sua máquina

## 📜 controla_containers.py

Para verificar todos os comandos basta digitar:

    python controla_containers.py --help
