FROM python:3.14-slim
RUN mkdir /app
RUN mkdir /app/logs
WORKDIR /app

RUN apt-get update && apt-get upgrade
RUN apk add unzip vim vim-docs vim-scripts sqlite3 -y

# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 
 
# Upgrade pip
RUN pip install --upgrade pip 
 
# Copy the Django project  and install dependencies
COPY requirements.txt  /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY requirements-dev.txt  /app/
RUN pip install --no-cache-dir -r /app/requirements-dev.txt

# Copy the Django project to the container
COPY . /app/
RUN python3 manage.py migrate
RUN python3 manage.py loaddata directorio/fixtures/directorio.json
RUN python3 manage.py loaddata normativa/fixtures/normativa.json
RUN python3 manage.py loaddata glosario/fixtures/glosario.json
RUN python3 manage.py loaddata juriscan/fixtures/juriscan.json
RUN python3 manage.py loaddata sistemas/fixtures/sistemas.json
RUN unzip -ul uploads.zip -d uploads/
RUN python3 manage.py collectstatic --noinput

# Expose the Django port
EXPOSE 8801
 
# Run Django’s development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8801"]
