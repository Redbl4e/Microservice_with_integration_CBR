FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN python -m venv venv

RUN /bin/bash -c "source venv/bin/activate"

RUN pip install -r requirements.txt

COPY  . .

CMD gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000