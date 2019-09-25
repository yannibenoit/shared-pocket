FROM python:3.6.5


RUN mkdir -p /project/app
COPY requirements.txt /project/app/

RUN pip install --upgrade pip
RUN pip install -r /project/app/requirements.txt

COPY . /project/app
WORKDIR /project/app

ENV PYTHONPATH=/project
ENV PYTHONUNBUFFERED=TRUE

EXPOSE 5000

WORKDIR /project

ENTRYPOINT [ "python" ]

CMD [ "app/app.py" ]

# CMD [ "/bin/bash" ]


