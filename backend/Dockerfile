FROM python:3.11

RUN pip3 install --upgrade pip && pip3 install poetry

WORKDIR /backend

COPY poetry.lock pyproject.toml entrypoint.sh ./

RUN poetry config virtualenvs.create false && poetry install --without test --no-interaction --no-ansi

#RUN apt-get update && apt-get install -y wkhtmltopdf

COPY cash_machine /backend

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

CMD ["gunicorn", "cash_machine.wsgi:application", "--bind", "0:8000" ]

LABEL author='leenominai' version='cash_machine v1.05' broken_keyboards=1
