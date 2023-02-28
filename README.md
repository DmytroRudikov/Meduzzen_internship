# FastAPI project

## to run tests from Meduzzen_internship repository
    
    python -m pytest


## to run the app from Meduzzen_internship repository

    python app/main.py

## to run the app from Docker

    docker start fastapipet

## to run tests from Docker, once container is running with the command above

    docker exec fastapipet python -m pytest

## to make a migration

    docker-compose run web alembic revision --autogenerate -m "First migration"

## to run a migration

    docker-compose run web alembic upgrade head