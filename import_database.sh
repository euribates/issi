#!/usr/bin/env bash

./manage.py loaddata directorio/fixtures/directorio.json
./manage.py loaddata directorio/fixtures/directorio.json --database test_default

./manage.py loaddata normativa/fixtures/normativa.json
./manage.py loaddata normativa/fixtures/normativa.json --database test_default

./manage.py loaddata glosario/fixtures/glosario.json
./manage.py loaddata glosario/fixtures/glosario.json --database test_default

./manage.py loaddata juriscan/fixtures/juriscan.json
./manage.py loaddata juriscan/fixtures/juriscan.json --database test_default

./manage.py loaddata sistemas/fixtures/sistemas.json
./manage.py loaddata sistemas/fixtures/sistemas.json --database test_default

./manage.py loaddata plan/fixtures/plan.json
./manage.py loaddata plan/fixtures/plan.json --database test_default

./manage.py loaddata omnibus/fixtures/omnibus.json
./manage.py loaddata omnibus/fixtures/omnibus.json --database test_default

# zip  -r uploads.zip uploads/
