FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt -v

COPY my_app.py .
COPY templates/ templates/

EXPOSE 5000

CMD ["python", "my_app.py"]