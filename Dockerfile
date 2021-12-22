FROM python:3.9

WORKDIR /usr/src/app

RUN pip3 install Flask
RUN pip3 install requests
RUN pip3 install Jinja2
RUN pip3 install python-dotenv
RUN pip3 install gevent

COPY . .

EXPOSE 5000

CMD [ "python", "./app.py" ]