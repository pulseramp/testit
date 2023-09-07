FROM python:3.10-bullseye
COPY . /app
WORKDIR /app
EXPOSE 8000
RUN pip install -r requirements.txt
CMD [ "python","manage.py","runserver" ]