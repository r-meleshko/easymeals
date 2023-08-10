# base image
FROM python:3.9-bullseye

#Prevents Python from writing pyc files to dis
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /mealprep
COPY ./mealprep /mealprep/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
