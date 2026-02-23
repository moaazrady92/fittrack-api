# use offically python image

FROM python:3.11-slim

# setting enviroment variables
ENV PYTHONDONTWRITEBYTECODE = 1
ENV PYTHONUNBUFFERED = 1
ENV DJANGO_SETTINGS_MODULE =config.settings

# setting work directory
WORKDIR /app

# installing system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# installing python dependencies \
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy project
COPY . .

# collection static files for production
#RUN python manage.py collectstatic --noinput

# Running django devolopment mode
CMD ["python","manage.py","runserver","0.0.0.0:8000"]