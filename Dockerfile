FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

COPY entrypoint.sh /app/

RUN chmod +x /app/entrypoint.sh

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]