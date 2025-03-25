# Instala o python
FROM python:3.13.2-slim-bookworm

#
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requiements.txt

COPY . .

EXPOSE 8000

CMD [ "python" , "manage.py" , "runserver" , "0.0.0.0:8000"]




FROM python:3.12-slim-bookworm

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"



#------
# Copy the project into the image
ADD . /app

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app
RUN uv sync --frozen


COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]


#-- ficheiro
#!/bin/sh

# collect all static files to the root directory
python manage.py collectstatic --no-input

# start the gunicorn worker processws at the defined port
gunicorn ecommerce_project.wsgi:application --bind 0.0.0.0:8000 &

wait
#--fim ficheiro

# -- config nginx
upstream django {
 server django_ecommerce_project:8000;
}

server {
 listen 80;

 location / {
  proxy_pass http://django;
 }

 location /static/ {
  alias /static/;
 }
}
#--- fim nginx

#-- Dokcer file for nginx
# Second stage: build the Nginx server
FROM nginx:1.23-alpine

# Copying our .conf files
COPY ./default.conf /etc/nginx/conf.d/default.conf 

# remove the log files in order to remove symlink between nginx logs & container log paths to ensure logs are available in default nginx log path
RUN rm -f /var/log/nginx/* 



