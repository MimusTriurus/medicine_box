FROM python:3.10.4-slim

WORKDIR /app

COPY .. .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install -r requirements.txt

RUN chmod +x run.sh

CMD [ "./run.sh" ]
