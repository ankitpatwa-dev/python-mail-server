# use the ubuntu base image
FROM ubuntu:20.04


# set the working directory inside container
WORKDIR /app

# Update and install Python and pip3 with --fix-missing flag
RUN apt-get update --fix-missing && \
    apt-get install -y python3 python3-pip && \
    apt-get clean

COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt
