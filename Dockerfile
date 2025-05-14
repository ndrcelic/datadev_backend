FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV APP=run.py
ENV APP_ENV=docker

EXPOSE 5000

CMD ["python", "run.py"]