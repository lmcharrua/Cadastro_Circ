FROM python:3.13.2alpine3.21

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requiements.txt .

RUN pip install --upgrade pip
RUN pip install -r requiements.txt

COPY . .

EXPOSE 8000

CMD [ "python" , "manage.py" , "runserver" , "0.0.0.0:8000"]

