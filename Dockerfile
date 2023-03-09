FROM python:3.8.10
RUN pip3 install Flask==2.2.2
RUN pip3 install requests==2.22.0
RUN pip3 install xmltodict==0.13.0
RUN pip install GeoPy==2.3.0
RUN pip install pyyaml==6.0

COPY iss_tracker.py /iss_tracker.py

CMD ["python", "iss_tracker.py"]

