FROM python:3.14
RUN mkdir /app
WORKDIR /app
RUN apt-get install unzip vim

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
RUN python manage.py migrate
RUN python manage.py loaddata directorio/fixtures/directorio.json
RUN python manage.py loaddata normativa/fixtures/normativa.json
RUN python manage.py loaddata glosario/fixtures/glosario.json
RUN python manage.py loaddata sistemas/fixtures/sistemas.json
RUN unzip -ul uploads.zip -d uploads/

# Expose the Django port
EXPOSE 8801
 
# Run Django’s development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8801"]
