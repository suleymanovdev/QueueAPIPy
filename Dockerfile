FROM python:3.9-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY app.py /app/
COPY consumer.py /app/
COPY rabbitmq_methods.py /app/
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN useradd -m myuser
USER myuser
EXPOSE 1234
CMD ["bash", "-c", "python consumer.py & uvicorn app:app --host 0.0.0.0 --port 1234"]
