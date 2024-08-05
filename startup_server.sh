#!/bin/sh

if [ "$STAGE" = "dev" ] || [ "$STAGE" = "stg" ]; then
    alembic -c /app/$PROJECT_PATH/alembic.ini upgrade head
fi

# python /app/$PROJECT_PATH/app.py
gunicorn --chdir /app/$PROJECT_PATH src.main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$SERVICE_PORT
