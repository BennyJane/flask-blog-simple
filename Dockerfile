FROM python:3.6
# 远程主机的项目路径
WORKDIR home/www/flask-blog-v1

RUN mkdir -p /var/log/blogdog && touch /var/log/blogdog/server.log

COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple &&\
        pip install psycopg2-binary==2.8.4 -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN apt-get update
RUN apt-get install -y supervisor --fix-missing

RUN mkdir -p /etc/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY . .
EXPOSE 8001 22 80
# 利用 gunicorn
# CMD ["gunicorn", "wsgi:app", "-c", "./gunicorn.conf.py"]
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
