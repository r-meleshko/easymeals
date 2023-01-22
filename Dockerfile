# base image
FROM python:3.9-bullseye


#Prevents Python from writing pyc files to dis
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# switch to /app directory so that everything runs from here
WORKDIR /mealprep
#/usr/src/app

# copy the app code to image working directory
COPY ./mealprep /mealprep/
#COPY . .

#RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
# let pip install required packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
