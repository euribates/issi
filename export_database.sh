#!/usr/bin/env bash


function dumpdata () {
    echo -n "Dumping $1";
    python -Xutf8 ./manage.py dumpdata --indent 4 $1 > ./fixtures/$1.json;
    echo -e " [\033[1;32mOK\033[0m]";
}


dumpdata "auth"
dumpdata "admin"
dumpdata "contenttypes"
dumpdata "glosario"
dumpdata "normativa"
dumpdata "directorio"
dumpdata "juriscan"
dumpdata "sistemas"
dumpdata "plan"
dumpdata "omnibus"

zip -r fixtures.zip fixtures/
zip -r uploads.zip uploads/
