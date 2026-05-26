FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP=wsgi.py
ENV PYTHONPATH=/app
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh
CMD ["/wait-for-db.sh"]
