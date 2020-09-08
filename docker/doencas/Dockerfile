FROM python:3.6

WORKDIR doenca/

COPY utils ./utils
COPY ./gera_doenca.py ./requirements.txt ./

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir log

CMD ["/bin/bash"]
