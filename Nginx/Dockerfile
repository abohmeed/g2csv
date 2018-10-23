FROM nginx
RUN rm -f /etc/nginx/conf.d/default.conf
COPY ./flask.conf /etc/nginx/conf.d/flask.conf
COPY ./index.html /usr/src/app/g2csv/index.html