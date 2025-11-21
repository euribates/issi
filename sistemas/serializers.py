#!/usr/bin/env python3

import csv


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
        ])
    for sistema in sistemas:
        _cvs.writerow([
            sistema.nombre,
            sistema.codigo,
            sistema.proposito,
            sistema.tema.pk,
            sistema.organismo.dir3 if sistema.organismo else '',
            ', '.join([
                _perfil.usuario.abreviado() 
                for _perfil in sistema.perfiles.filter(cometido='TEC')
                ]),
            ', '.join([
                _perfil.usuario.abreviado() 
                for _perfil in sistema.perfiles.filter(cometido='FUN')
                ]),
            '[Falta Normativa]',
            sistema.observaciones,
            ])
