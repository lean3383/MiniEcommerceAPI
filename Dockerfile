FROM python:3.9-alpine3.14
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY ./backend /app/
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    adduser --disabled-password --no-create-home app && \
    chown -R app:app /app
USER app
