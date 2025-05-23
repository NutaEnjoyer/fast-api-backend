FROM python:3-11-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", '-m', "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]