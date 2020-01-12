FROM python:3.6
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app
COPY Pip* /usr/src/app/
RUN pip install --upgrade pip && \
  pip install pipenv && \
  pipenv install --dev --deploy --ignore-pipfile

COPY . /usr/src/app

CMD ["pipenv", "run", "python", "/app/manage.py", "runserver","0.0.0.0:3000"]