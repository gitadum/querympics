FROM python:3.8
ENV PYTHONPATH "${PYTHONPATH}:/app/"
RUN pip3 install fastapi uvicorn tortoise-orm databases asyncpg
COPY ./app /app
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "15400"]