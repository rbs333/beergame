#!/usr/bin/env bash


if [[ "${FLASK_ENV}" == "development" ]]
then 
  echo "starting in ${FLASK_ENV} mode"
  exec python app.py
elif [[ "${FLASK_ENV}" == "production" ]]
then
  echo "starting in ${FLASK_ENV} mode"
  exec uwsgi --ini config/uwsgi.ini
else
  echo "FLASK_ENV must be either development or production"
fi