FROM python:3
WORKDIR /code
RUN pip install Django mysqlclient mysql-connector-python cryptography django-cors-middleware
COPY ./src /code/

COPY ./wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

CMD /wait-for-it.sh db_serverapp:3306 && python POC/manage.py runserver 0.0.0.0:8000
