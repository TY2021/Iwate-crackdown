FROM python:3.5.2

# Install Libraries
RUN mkdir -p /var/lib/data_lab
WORKDIR /var/lib/data_lab
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Copy Sources
COPY ./src/ ./src/
