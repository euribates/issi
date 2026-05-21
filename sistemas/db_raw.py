#!/usr/bin/env python3

from dataclasses import dataclass

from django.db import connection

@dataclass(frozen=True, slots=True)
class EntesData:
    ente: str
    id_organismo: int
    nombre_organismo: str
    num_sistemas: int


def db_entes():
    sql = """
SELECT ente.id_ente as ente,
       org.id_organismo,
       org.nombre_organismo,
       count(si.id_sistema) as num_sistemas
  FROM sistemas_ente ente
  LEFT JOIN directorio_organismo org ON ente.organismo_id = org.id_organismo
  LEFT JOIN sistemas_sistema si ON si.ente = ente.id_ente
 GROUP by ente.id_ente, org.nombre_organismo
 ORDER by ente.id_ente;
"""
    with connection.cursor() as cursor:
        cursor.execute(sql)
        for row in cursor.fetchall():
            yield EntesData(*row)
