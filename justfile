set export

DATABASE := "default"

# Abrir una shell de python/Django
shell:
    python ./manage.py shell_plus


# Ejecutar test (Omitiendo los lentos)
test *args='.': clean check
    python smoke_test.py
    python -m pytest -m "not slow" -x --reuse-db --no-migrations --failed-first {{ args }}

# Tests rápidos
quicktest:
    python -m pytest -m "not slow" -x --reuse-db --no-migrations --failed-first dc2
    python -m pytest -m "not slow" -x --reuse-db --no-migrations --failed-first consultas


# Mostrar versiones del software instalado
versions:
    python --version
    python -c "import django; print('Django', django.__version__)"
    psql --version


# Acceder a una shell de la base de datos
dbshell:
    python ./manage.py dbshell

# Muestra información del S.O., arquitectura, software y hardware
@info:
    echo "OS: {{os()}} / {{os_family()}}"
    echo "Arch: This is an {{arch()}} machine"
    python -c "import sys; print('Python:', sys.version.split()[0])"
    python -c "import django; print('Django:', django.__version__)"
    echo "Uptime:" `uptime`


# Ejecutar django check
check:
    python ./manage.py check


# Ejecutar django collectstatic
static:
    python ./manage.py collectstatic --no-input


# Ejecutar un run server en modo desarrollo
rundev: check static 
    python ./manage.py runserver 0.0.0.0:8800 


# Borrar ficheros compilados de python
clean:
    sudo find . -type d -name "__pycache__" -exec rm -rf "{}" +
    sudo find . -type d -name ".mypy_cache" -exec rm -rf "{}" +
    sudo find . -type d -name ".ruff_cache" -exec rm -rf "{}" +
    sudo find . -type f -name "*.pyc" -delete
    sudo find . -type f -name "*.pyo" -delete


# Mostrar migraciones Django
showmigrations $APP='': check
    python manage.py showmigrations {{APP}}

alias sm := showmigrations

# Crear nuevas migraciones Django
makemigrations $APP='': check
    python manage.py makemigrations {{APP}}

alias mm := makemigrations

# Ejecutar migraciones Django
migrate $APP='': check
    python manage.py migrate {{APP}} --database $DATABASE

# Generar imágenes para la documentación de los modelos
docs:
    python ./manage.py graph_models -g -o docs/dc2_models.png

# Actualiza en caliente contenidos estaticos js/css/png/svg
[unix]
watch: static
    # termtitle Watch
    watchmedo shell-command  --patterns "*.css;*.js;*.png;*.jpg;*.webp;*.svg" --recursive --command "just static"


# Genera el fichero de tags
tags:
    cd {{justfile_directory()}} && ctags -R  --exclude=media/*  --exclude=*/static/* --exclude=static/* .
