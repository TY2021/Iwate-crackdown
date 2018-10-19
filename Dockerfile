FROM python:3.5.2
ADD Iwate_crackdown_read.py /
ADD crackdown_statistics.csv /
ADD requirements.txt /
RUN pip install -r requirements.txt
RUN pip install --upgrade pip
