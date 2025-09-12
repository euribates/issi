#!/usr/bin/env bash

./manage.py dumpdata glosario --indent 4 > glosario/fixtures/glosario.json
./manage.py dumpdata sistemas --indent 4 > sistemas/fixtures/sistemas.json
./manage.py dumpdata normativa --indent 4 > normativa/fixtures/normativa.json
./manage.py dumpdata directorio --indent 4 > directorio/fixtures/directorio.json
zip  -r uploads.zip uploads/
