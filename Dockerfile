FROM grpc/python:1.0

WORKDIR /var/www/html/application

COPY  requirements.txt /var/www/html/application/requirements.txt
RUN pip install -r requirements.txt
COPY . /var/www/html/application/

CMD ["python", "/var/www/html/application/main.py"]
