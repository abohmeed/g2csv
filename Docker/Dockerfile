FROM nginx
RUN rm -f /etc/nginx/conf.d/default.conf
COPY ./flask.conf /etc/nginx/conf.d/flask.conf
RUN apt update && apt install python-pip -y && pip install flask requests beautifulsoup4 boto3
COPY app.py /
RUN python /app.py &