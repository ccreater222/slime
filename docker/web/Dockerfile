FROM ubuntu:22.04
COPY ./docker/worker/sources.list /etc/apt/sources.list
RUN apt-get update && apt-get install -y --force-yes  python3  python3-pip git && \
    apt-get install -y --force-yes python3-venv
COPY ./app /app
RUN cd /app && python3 -m venv venv && ./venv/bin/pip install -r requirements.txt  -i https://mirrors.aliyun.com/pypi/simple/
WORKDIR /app
RUN ./venv/bin/python app.py install
RUN apt-get install -y --force-yes nginx
COPY ./docker/web/start.sh /start.sh
COPY ./docker/web/nginx.conf /etc/nginx/sites-available/default 
COPY ./docker/web/htpasswd /etc/apache2/htpasswd
COPY ./frontend/dist /var/www/html
RUN chmod 744 /etc/apache2/htpasswd
CMD [ "/bin/bash", "/start.sh" ]