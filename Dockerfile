FROM python:3.12-slim

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r /app/requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 3002
CMD ["python", "main.py"]
