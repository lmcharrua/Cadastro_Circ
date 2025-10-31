sudo systemctl stop nginx.service
sudo systemctl stop gunicorn.service
git pull origin main
source .venv/bin/activate
python manage.py migrate
python manage.py collectstatic <yes
deactivate
sudo systemctl start gunicorn.service
sudo systemctl start nginx.service
sudo systemctl status gunicorn.service

