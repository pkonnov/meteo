FROM python:3.9.1-slim-buster

# install system requirements
RUN set -x \
    && apt update && apt-get install -qq \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# install project requirements
RUN pip install --upgrade pip
COPY ./etc/requirements.txt /tmp
COPY ./src /tmp
WORKDIR /tmp
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]

EXPOSE 8000
