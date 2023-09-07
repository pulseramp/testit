FROM python:3.10-bullseye
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD [ "python","manage.py","runserver","0.0.0.0:8000 " ]