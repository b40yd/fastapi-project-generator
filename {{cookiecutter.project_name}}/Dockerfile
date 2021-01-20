FROM python:3.7
ENV TZ=Asia/Shanghai
COPY ./ /app

WORKDIR /app

RUN sed -i 's#http://deb.debian.org#http://mirrors.163.com#g' /etc/apt/sources.list
RUN apt-get update && apt-get install libmariadb-dev supervisor tzdata -y
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
RUN cp -rfv /app/conf/supervisor-app.conf /etc/supervisor/conf.d/

EXPOSE 80


CMD ["/bin/bash", "/app/scripts/start.sh"]
