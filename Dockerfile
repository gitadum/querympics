FROM python:3.8
RUN pip3 install -r requirements.txt
COPY ./app /app
CMD ["uvicorn", "app.api:app", "--host", "127.0.0.1", "--port", "8000"]