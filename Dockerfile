FROM python:3.8
#ENV PYTHONPATH "${PYTHONPATH}:/app/"
COPY requirements.txt requirements.txt 
RUN pip3 install -r requirements.txt
COPY ./querympics /querympics
RUN python querympics.data.load.py
CMD ["uvicorn", "querympics.api:app", "--host", "0.0.0.0", "--port", "15400"]