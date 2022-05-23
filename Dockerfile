FROM arquiteturansj/flask:2.0

WORKDIR /var/www/html

COPY . /var/www/html

RUN python3 -m pip install -r /var/www/html/requirements.txt --no-cache-dir

CMD /entrypoint.sh
