FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install Flask pymongo kafka-python
CMD ["python", "app.py"]
