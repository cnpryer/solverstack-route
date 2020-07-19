FROM python:3.8-slim

COPY requirements*.txt /app/

WORKDIR /app

RUN python -m pip install -r requirements.txt

RUN python -m pip install -r requirements-dev.txt

COPY . /app

ENTRYPOINT [ "python" ]

# Set and expose port
ENV PORT 5000
EXPOSE 5000