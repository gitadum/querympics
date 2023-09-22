FROM python:3.8
COPY requirements.txt requirements.txt 
RUN pip3 install -r requirements.txt
COPY ./querympics /querympics
COPY ./setup.py setup.py
COPY ./README.md README.md
RUN pip3 install -e .
#RUN python3 querympics/data/load.py
CMD ["uvicorn", "querympics.api:app", "--host", "0.0.0.0", "--port", "15400"]