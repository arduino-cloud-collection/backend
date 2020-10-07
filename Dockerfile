# set baseimage to alpine linux
FROM python:3.8-slim

# set the working directory
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . .

# command to run on container start
CMD ["/usr/local/bin/uvicorn","arduino_backend.main:app","--host","0.0.0.0"]
