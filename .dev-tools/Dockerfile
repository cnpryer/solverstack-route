FROM python:3.8-slim

COPY requirements*.txt /app/

WORKDIR /app

RUN python -m pip install -r requirements.txt

RUN python -m pip install -r requirements-dev.txt

COPY . /app

ENTRYPOINT [ "python" ]

# flask dev (remove for prod)
ENV FLASK_APP app
ENV FLASK_ENV development
ENV DEBUG 1

# Set and expose port
ENV PORT 5000
EXPOSE 5000