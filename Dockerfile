# Stage 1: Build
FROM python:3.11 AS build
WORKDIR /app
COPY ./src/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src /app

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /app /app
CMD ["sh", "-c", "python api_server.py & python client_server.py"]
