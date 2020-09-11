# set baseimage to alpine linux
FROM python:rc-alpine

# update the image
RUN apk update && apk upgrade

# install dependencies
RUN apk add gcc musl-dev make

# set the working directory
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# remove dependencies after install
RUN apk del gcc musl-dev make

# copy the content of the local src directory to the working directory
COPY src/ .

# command to run on container start
CMD python3 -m uvicorn main:app --host 0.0.0.0