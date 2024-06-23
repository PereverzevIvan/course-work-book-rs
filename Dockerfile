# pull official base image
FROM python:3.12

# set work directory
WORKDIR /usr/src/app

# Копируем содержимое проекта в контейнер
COPY . /usr/src/app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Открывает порт для взаимодействия с веб-сервером
EXPOSE 8000

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
