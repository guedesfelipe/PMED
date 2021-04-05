FROM python:3.6

WORKDIR hospital/

COPY utils ./utils
COPY ./hospital.py ./requirements.txt ./

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["/bin/bash"]
