# pull official base image
FROM python:3.9.6

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


# copy project
COPY . .

RUN sed -i 's/\r$//g' /usr/src/app/docker-entrypoint.sh
RUN chmod +x /usr/src/app/docker-entrypoint.sh
RUN chmod +x ./docker-entrypoint.sh

EXPOSE 8000
CMD [ "python", "manage.py", "runserver" ]