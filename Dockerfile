# set baseimage to alpine linux
FROM python:3.8-slim

# Disables Python Buffering
ENV PYTHONUNBUFFERED=1

# set the working directory
WORKDIR /code

# Copy the files
COPY . .

# Installs the dependencies
RUN apt-get update -y \
 && apt-get install -y --no-install-recommends curl \
 && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs > rust.sh \
 && sh rust.sh -y \
 && rm rust.sh \
 && pip install  --no-cache-dir --upgrade pip \
 && pip install  --no-cache-dir -r requirements.txt \
 && /root/.cargo/bin/rustup self uninstall -y \
 && apt-get autoremove -y curl \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# command to run on container start
CMD ["/usr/local/bin/uvicorn","arduino_backend.main:app","--host","192.168.0.1"]
