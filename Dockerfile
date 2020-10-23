# set baseimage to alpine linux
FROM python:3.9.0-slim

# set the working directory
WORKDIR /code

# Updates the image
RUN apt-get update -y

# Upgrades the image
RUN apt-get upgrade -y

# Installs CURL
RUN apt-get install -y curl

# Downloads the rust install script
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs > rust.sh

# Runs the rust install script
RUN sh rust.sh -y

# Removes the rust install script after run
RUN rm rust.sh

# Upgrades pip
RUN  pip install --upgrade pip

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . .

# command to run on container start
CMD ["/usr/local/bin/uvicorn","arduino_backend.main:app","--host","0.0.0.0"]
