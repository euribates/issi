#!/usr/bin/env bash

./manage.py loaddata directorio/fixtures/directorio.json
./manage.py loaddata normativa/fixtures/normativa.json
./manage.py loaddata glosario/fixtures/glosario.json
./manage.py loaddata juriscan/fixtures/juriscan.json
./manage.py loaddata sistemas/fixtures/sistemas.json
./manage.py loaddata antecedentes/fixtures/antecedentes.json
# zip  -r uploads.zip uploads/
