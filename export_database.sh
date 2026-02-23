#!/usr/bin/env bash

python -Xutf8 ./manage.py dumpdata glosario --indent 4 > glosario/fixtures/glosario.json
python -Xutf8 ./manage.py dumpdata normativa --indent 4 > normativa/fixtures/normativa.json
python -Xutf8 ./manage.py dumpdata directorio --indent 4 > directorio/fixtures/directorio.json

python -Xutf8 ./manage.py dumpdata sistemas --indent 4 > sistemas/fixtures/sistemas.json
python -Xutf8 ./manage.py dumpdata juriscan --indent 4 > juriscan/fixtures/juriscan.json
zip  -r uploads.zip uploads/
