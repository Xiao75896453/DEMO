# DEMO
> This monorepo contains DEMO projects

[TOC]

---
# Projects
## account_password_management
[![My Skills](https://skillicons.dev/icons?i=python,fastapi,postgresql&theme=light)](https://skillicons.dev)

- Backend Framework : [FastAPI](https://fastapi.tiangolo.com/) (async)
- [Unit Test](https://github.com/Xiao75896453/DEMO/tree/develop/projects/account_password_management/tests) : [pytest](https://docs.pytest.org/en/stable/)
- [GitHub Actions](https://github.com/Xiao75896453/DEMO/actions) : lint、test
- ORM : [SQLAlchemy](https://www.sqlalchemy.org/)
- [DB Migration](https://github.com/Xiao75896453/DEMO/tree/develop/projects/account_password_management/alembic) : [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- lint : [ruff](https://github.com/astral-sh/ruff)、[isort](https://pycqa.github.io/isort/index.html)
- [Git Hook](https://github.com/Xiao75896453/DEMO/blob/develop/.pre-commit-config.yaml) : [pre-commit](https://pre-commit.com/)

### Requirements
- python 3.11+
- poetry

### Building from source and running with docker-compose
1. Clone the repo
    ```bash
    git clone git@github.com:Xiao75896453/DEMO.git
    ```
2. Create `.env` `.env.prod` `.env.docker` file in `projects/account_password_management` and set value.

    `.env` example
    ```.env
    STAGE="stg"
    SERVICE_PORT=3000

    DB_HOST="localhost"
    DB_PORT="5432"
    DB_USER="postgres"
    DB_PASSWORD="password"
    DB_DATABASE="account_password_management"
    DB_POOL_SIZE=10
    DB_MAX_OVERFLOW=5
    DB_POOL_RECYCLE=300
    ```
    
    `.env.prod`
    ```.env
    # override .env if you need
    ```
    
    `.env.docker`
    ```.env
    PROJECT_PATH="projects/account_password_management"
    PROJECT_IMAGE_NAME="account-password-management"
    DOCKER_HOST_DB_PORT=5432
    ```

3. Startup the services
    ```bash
    docker compose -f docker-compose.postgresql.yml -f projects/account_password_management/docker-compose.yml --env-file projects/account_password_management/.env --env-file projects/account_password_management/.env.docker -f docker-compose.prod.yml --env-file projects/account_password_management/.env.prod up
    ```

### API Document
1. Startup the services
2. Open a browser to http://localhost:3000/docs#

### Installation
1. Clone the repo
    ```bash
    git clone
    ```
1. Install Python packages
    ```bash
    poetry install
    ```
1. Install PostgreSQL
1. Set PostgreSQL account
1. Create DB
1. Create `.env` `.env.prod` `.env.docker` file in `projects/account_password_management` and set value.

    `.env` example
    ```.env
    STAGE="stg"
    SERVICE_PORT=3000

    DB_HOST="localhost"
    DB_PORT="5432"
    DB_USER="postgres"
    DB_PASSWORD="password"
    DB_DATABASE="account_password_management"
    DB_POOL_SIZE=10
    DB_MAX_OVERFLOW=5
    DB_POOL_RECYCLE=300
    ```
    
    `.env.prod`
    ```.env
    # override .env if you need
    ```
    
    `.env.docker`
    ```.env
    PROJECT_PATH="projects/account_password_management"
    PROJECT_IMAGE_NAME="account-password-management"
    DOCKER_HOST_DB_PORT=5432
    ```
3. Create DB schema
    1. migration
        ```bash
        alembic -c 'projects/account_password_management/alembic.ini' upgrade head
        ```

### Usage
- Startup the services
    ```bash
    python projects/account_password_management/app.py
    ```

- Test
    ```bash
    pytest projects/account_password_management
    ```

---
# Contributing
1. Fork the Project
1. Create New Issue (Optional)
1. Create your Feature Branch ```git checkout -b {project}/{type}/{description}```
1. Commit your Changes ```git commit``` (use .gitmessage.txt as format template for commit)
1. Push to the Branch ```git push origin {your feature branch}```
1. Open a Pull Request
1. Wait for review and merge

---
# Contact
TingYi Xiao - a75896453@gmail.com

---
# Acknowledgments
- [FastAPI](https://fastapi.tiangolo.com/)
- [Poetry](https://python-poetry.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [PostgreSQL](https://www.postgresql.org/)
- [README](https://github.com/othneildrew/Best-README-Template)
- [Semantic Versioning](https://semver.org/lang/zh-TW/)
