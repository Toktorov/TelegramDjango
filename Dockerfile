# pull official base image
FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# create the appropriate directories
WORKDIR /code

# install dependencies
COPY requirements.txt /code
RUN pip install -r /code/requirements.txt

# copy project
COPY . /code

EXPOSE 7000