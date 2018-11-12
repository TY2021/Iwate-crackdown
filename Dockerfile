FROM python:latest

RUN apt-get update
RUN apt-get install -y cron

ADD Read_iwate_crackdown.py /
ADD today_crackdown.txt /
ADD crackdown_statistics.csv /
ADD requirements.txt /

RUN pip install -r requirements.txt
RUN pip install --upgrade pip

ADD python-cron /etc/cron.d/python-cron
RUN chmod 0644 /etc/cron.d/python-cron

ADD ./ /
RUN chmod +x /script.sh

CMD cron && touch /etc/cron.d/simple-cron && tail -f /dev/null
