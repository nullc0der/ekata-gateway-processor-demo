FROM python:3.8
LABEL maintainer Prasanta Kakati <prasantakakati@ekata.social>
RUN apt-get update && \
    apt-get install --yes curl
RUN mkdir /ekata-gateway-processor-demo
WORKDIR /ekata-gateway-processor-demo
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
COPY pyproject.toml poetry.lock /ekata-gateway-processor-demo/
RUN . $HOME/.poetry/env && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev
COPY . /ekata-gateway-processor-demo
CMD [ "sh", "start.sh" ]
