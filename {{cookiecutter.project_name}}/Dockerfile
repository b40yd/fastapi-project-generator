FROM python:3.7
ENV TZ=Asia/Shanghai
COPY ./ /app

WORKDIR /app

RUN sed -i 's#http://deb.debian.org#http://mirrors.163.com#g' /etc/apt/sources.list
RUN echo $(apt-get update > /dev/null)
RUN apt-get install libmariadb-dev redis-server supervisor tzdata -y
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
RUN cp -rfv /app/conf/supervisor-app.conf /etc/supervisor/conf.d/

VOLUME ["/var/lib/redis"]

EXPOSE 80


CMD ["/bin/bash", "/app/scripts/start.sh"]
