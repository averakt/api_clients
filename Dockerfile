# Dockerfile
FROM python:3.8
WORKDIR /minibank
COPY . /minibank
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["./docker-entrypoint.sh"]
