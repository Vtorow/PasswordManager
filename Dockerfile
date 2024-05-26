FROM python:3.11-alpine

WORKDIR /passman

RUN pip install --upgrade pip
RUN pip install poetry && poetry config virtualenvs.create false

RUN mkdir passman

COPY ./poetry.lock ./pyproject.toml /passman/

RUN poetry install --no-interaction

COPY ./passman /passman/passman

CMD ["uvicorn", "passman.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]