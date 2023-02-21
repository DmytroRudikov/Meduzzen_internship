# FastAPI project

## to run tests from Meduzzen_internship repository
    
    python -m pytest


## to run the app from Meduzzen_internship repository

    python app/main.py

## to run the app from Docker

    docker start fastapipet

## another way to run the app from Docker

    docker run --hostname=3253eae4ca45 --env=PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin --env=LANG=C.UTF-8 --env=GPG_KEY=E3FF2839C048B25C084DEBE9B26995E310250568 --env=PYTHON_VERSION=3.9.16 --env=PYTHON_PIP_VERSION=22.0.4 --env=PYTHON_SETUPTOOLS_VERSION=58.1.0 --env=PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/1a96dc5acd0303c4700e02655aefd3bc68c78958/public/get-pip.py --env=PYTHON_GET_PIP_SHA256=d1d09b0f9e745610657a528689ba3ea44a73bd19c60f4c954271b790c71c2653 --workdir=/code -p 80:80 --restart=no --runtime=runc -d myimage

## to run tests from Docker, once container is running with the command above

    docker exec fastapipet python -m pytest