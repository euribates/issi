#!/usr/bin/env python3

import csv


def _responsables(sistema, cometido):
    return ', '.join([
        _perfil.usuario.abreviado() 
        for _perfil in sistema.perfiles.filter(cometido=cometido)
        ])

def _normativa(sistema):
    result = ''
    if sistema.normativa.exists():
        result = ', '.join([
            str(_.num_juriscan)
            for _ in sistema.normativa.all()
            ])
    return result


def sistemas_a_csv(sistemas, stream):
    _cvs = csv.writer(stream, delimiter=',', quotechar='"')
    _cvs.writerow([
        'Nombre',
        'Código Identificativo Interno (CII)',
        'Finalidad',
        'Materia competencial',
        'DIR3 (centro directivo)',
        'UID de la persona responsable tecnológica',
        'UID de la persona responsable funcional',
        'Normativa (Juriscan)',
        'Observaciones',
        'UUID',
        ])
    for sistema in sistemas:
        _cvs.writerow([
            sistema.nombre_sistema,
            sistema.codigo,
            sistema.proposito,
            sistema.tema.pk,
            sistema.organismo.dir3 if sistema.organismo else '',
            _responsables(sistema, 'TEC'),
            _responsables(sistema, 'FUN'),
            _normativa(sistema),
            sistema.observaciones,
            sistema.uuid,
            ])
