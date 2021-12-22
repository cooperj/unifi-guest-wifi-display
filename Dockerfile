FROM python:3.9

WORKDIR /usr/src/app

RUN pip3 install Flask
RUN pip3 install requests
RUN pip3 install Jinja2
RUN pip3 install python-dotenv
RUN pip3 install gevent
RUN pip3 install ping3

COPY . .

EXPOSE 5000

HEALTHCHECK CMD curl --fail http://localhost:5000/heartbeat || exit 1

CMD [ "python", "./app.py" ]