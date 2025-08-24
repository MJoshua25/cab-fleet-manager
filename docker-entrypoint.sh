#!/bin/sh

set -e

 echo "Environnement: ${DJANGO_ENV:-$env}"

echo "En attente de la base de donnée"
#./wait-for db:5432

echo "Exécution des migrations"
python manage.py migrate --noinput

echo "Collecte des fichiers statiques"
python manage.py collectstatic --noinput

echo "Démarrage du serveur Gunicorn"
gunicorn --config gunicorn-cfg.py config.wsgi