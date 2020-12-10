# fastapi generator project
An Fast generator fastapi project

# Usage
## create
    ```
    cookiecutter https://github.com/7ym0n/fastapi-project-generator.git
    ```
## database create
    <font color="red">Notes:</font>
    change databse **alembic.ini** `sqlalchemy.url = ` your drive.

    exec:
    ```
    alembic revision --autogenerate -m "init"
    alembic upgrade head
    ```

## run
    ```
    cd $(your_project) && uvicorn app.main:app --reload

    ```
