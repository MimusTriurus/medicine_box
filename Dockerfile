FROM python:3.10.4-slim

#EXPOSE 8000

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install -r requirements.txt

CMD [ "python", "main.py" ]
