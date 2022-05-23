FROM ubuntu:22.04
COPY ./docker/worker/sources.list /etc/apt/sources.list
RUN apt-get update && apt-get install -y --force-yes  python3  python3-pip git && \
    apt-get install -y --force-yes python3-venv
COPY ./app /app
RUN cd /app && python3 -m venv venv && ./venv/bin/pip install -r requirements.txt  -i https://mirrors.aliyun.com/pypi/simple/
WORKDIR /app
RUN ./venv/bin/python app.py install
CMD [ "./venv/bin/python", "./app.py", "worker" ]