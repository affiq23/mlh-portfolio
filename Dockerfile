FROM python:3.9-slim-buster 

COPY requirements.txt /myportfolio/requirements.txt

WORKDIR /myportfolio

RUN pip3 install -r requirements.txt

COPY . /myportfolio

CMD ["python3", "app/__init__.py"]

EXPOSE 5000