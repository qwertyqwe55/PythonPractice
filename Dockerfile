FROM python:3.10-buster
RUN mkdir /fastapi_app
WORKDIR /fastapi_app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
