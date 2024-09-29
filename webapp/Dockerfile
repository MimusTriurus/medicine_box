FROM python:3.10.4-slim

WORKDIR /app

COPY .. .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install -r requirements.txt

CMD [ "./run.sh" ]
