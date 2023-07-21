#!/bin/sh

echo "En attente de la base de donnée"
#./wait-for db:5432

echo "Execution des migrations"
python manage.py migrate

echo "Execution de collectstatic"
python manage.py collectstatic --noinput

echo "Demarrage du serveur"
python manage.py runserver 0.0.0.0:8000