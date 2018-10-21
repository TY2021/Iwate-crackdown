FROM python:3.5.2
ADD Read_iwate_crackdown.py /
ADD today_crackdown.txt /
ADD crackdown_statistics.csv /
ADD requirements.txt /
RUN pip install -r requirements.txt
RUN pip install --upgrade pip
