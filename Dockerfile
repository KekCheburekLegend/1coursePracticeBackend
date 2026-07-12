FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requrements.txt

CMD ["python", "main.py"]
