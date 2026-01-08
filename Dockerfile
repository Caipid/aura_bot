FROM python:3.15
WORKDIR /app
COPY requirements.txt .
COPY . /app
RUN pip install -r requirements.txt --no-cache-dir

CMD ["/app/entrypoint.sh"]