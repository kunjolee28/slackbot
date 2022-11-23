# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.7-slim-buster

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME

# Update apt-get packages
RUN apt-get update && apt-get install -y wget curl
RUN rm -rf /var/lib/apt/lists/*

# Install dependencies.
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# # Clean up apt-get installs
RUN apt-get -y autoremove

# Run the web service on container startup.
COPY . ./

CMD exec gunicorn --timeout 900 --bind :8080 main:app