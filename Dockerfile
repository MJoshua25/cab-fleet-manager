# pull official base image
FROM python:3.12.2-slim

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# ensure entrypoint is executable and Unix-formatted
RUN sed -i 's/\r$//g' /usr/src/app/docker-entrypoint.sh && \
    chmod +x /usr/src/app/docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]