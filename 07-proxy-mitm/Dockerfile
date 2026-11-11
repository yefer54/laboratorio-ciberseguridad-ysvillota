FROM python:alpine

# Forzar a Python a volcar todos los prints a la consola sin esperar
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY app.py /app/app.py

RUN pip install --no-cache-dir flask requests

CMD ["python", "app.py"]
