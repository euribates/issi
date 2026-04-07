#!/usr/bin/env bash

./manage.py loaddata fixtures/auth.json
./manage.py loaddata fixtures/auth.json --database test_default

./manage.py loaddata fixtures/admin.json
./manage.py loaddata fixtures/admin.json --database test_default

./manage.py loaddata fixtures/contenttypes.json
./manage.py loaddata fixtures/contenttypes.json --database test_default

./manage.py loaddata fixtures/directorio.json
./manage.py loaddata fixtures/directorio.json --database test_default

./manage.py loaddata fixtures/normativa.json
./manage.py loaddata fixtures/normativa.json --database test_default

./manage.py loaddata fixtures/glosario.json
./manage.py loaddata fixtures/glosario.json --database test_default

./manage.py loaddata fixtures/juriscan.json
./manage.py loaddata fixtures/juriscan.json --database test_default

./manage.py loaddata fixtures/sistemas.json
./manage.py loaddata fixtures/sistemas.json --database test_default

./manage.py loaddata fixtures/plan.json
./manage.py loaddata fixtures/plan.json --database test_default

./manage.py loaddata fixtures/omnibus.json
./manage.py loaddata fixtures/omnibus.json --database test_default

# zip  -r uploads.zip uploads/
