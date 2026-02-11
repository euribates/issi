#!/usr/bin/env python3

import pytest
from uuid import UUID

from comun.funcop import first

from sistemas import parsers
from sistemas.models import Usuario
from sistemas.models import Tema
from juriscan.models import Juriscan
from directorio.models import Organismo


# -------------------------------------------------[ Nombre sistema ]--

def test_parse_nombre_sistema_vacio():
    rs = parsers.parse_nombre_sistema('')
    assert rs.is_failure()


def test_parse_nombre_sistema_nulo():
    rs = parsers.parse_nombre_sistema(None)
    assert rs.is_failure()


def test_parse_nombre_sistema_demasiado_corto():
    rs = parsers.parse_nombre_sistema('Sic')
    assert rs.is_failure()


def test_parse_nombre_sistema_se_elimina_punto_filal():
    rs = parsers.parse_nombre_sistema('Sistema Ocho.')
    assert rs.is_success()
    assert rs.value == 'Sistema Ocho'


@pytest.mark.django_db
def test_parse_users_single_username():
    expected = Usuario.load_usuario('jrodleo')
    result = parsers.parse_users('jrodleo')
    assert result.is_success()
    users = result.value
    assert type(users) is set
    assert len(users) == 1
    assert first(users) == expected


@pytest.mark.django_db
def test_parse_users_double_username():
    expected = set([
        Usuario.load_usuario('jrodleo'),
        Usuario.load_usuario('malosua'),
        ])
    rs = parsers.parse_users('malosua, jrodleo')
    assert rs.is_success()
    assert rs.value == expected


@pytest.mark.django_db
def test_parse_users_single_email():
    expected = set([Usuario.load_usuario('jrodleo')])
    rs = parsers.parse_users('jrodleo@gobiernodecanarias.org')
    assert rs.is_success()
    assert rs.value == expected


@pytest.mark.django_db
def test_parse_user_full_email():
    expected = set([Usuario.load_usuario('jrodleo')])
    rs = parsers.parse_users('Juan Ignacio <jrodleo@gobiernodecanarias.org>')
    assert rs.is_success()
    assert rs.value == expected


@pytest.mark.django_db
def test_parse_users_bad_input():
    rs = parsers.parse_users("I'm Bad! Bad! (Really, really bad)")
    assert rs.is_failure()


@pytest.mark.django_db
def test_parse_users_void_input():
    expected = set([])
    rs = parsers.parse_users('')
    assert rs.is_success()
    assert rs.value == expected


@pytest.mark.django_db
def test_parse_juriscan_single_number():
    rs = parsers.parse_juriscan('5559')
    assert rs.is_success()
    assert type(rs.value) is set
    ficha = first(rs.value)
    assert ficha.titulo == 'Ley 2/1984, 11 abril, de Premios Canarias'


@pytest.mark.django_db
def test_parse_juriscan_double_number():
    expected = set([
        Juriscan.load_or_create(5559),
        Juriscan.load_or_create(79558),
        ])
    rs = parsers.parse_juriscan('79558, 5559')
    from icecream import ic; ic(rs)
    from icecream import ic; ic(rs.value)
    assert rs.is_success()
    assert rs.value == expected

    rs = parsers.parse_juriscan('79558; 5559')
    assert rs.is_success()
    assert rs.value == expected



@pytest.mark.django_db
def test_parse_juriscan_en_diferentes_lineas():
    expected = set([
        Juriscan.load_or_create(5559),
        Juriscan.load_or_create(79558),
        ])
    rs = parsers.parse_juriscan('79558\n5559')
    assert rs.is_success()
    assert rs.value == expected


@pytest.mark.django_db
def test_parse_juriscan_link():
    expected = Juriscan.load_or_create(5559)
    url = 'https://www3.gobiernodecanarias.org/juriscan/ficha.jsp?id=5559'
    rs = parsers.parse_juriscan(url)
    assert rs.is_success()
    assert first(rs.value) == expected


@pytest.mark.django_db
def test_parse_juriscan_multiples_enlaces():
    expected = set([
        Juriscan.load_or_create(5559),
        Juriscan.load_or_create(79558),
        ])
    urls = (
        'https://www3.gobiernodecanarias.org/juriscan/ficha.jsp?id=5559\n'
        'https://www3.gobiernodecanarias.org/juriscan/ficha.jsp?id=79558&from=0&nreg=25&materiasop=AND&materias1=*&materias2=*&rango1=*&rango2=*&titulo=internet&desdeemi=&hastaemi=&ordendesc=IdRango&orden=asc&numdisp=0&tituloAux=internet.'
        )
    rs = parsers.parse_juriscan(urls)
    assert rs.is_success()
    assert rs.value == expected


def test_parse_juriscan_empty():
    rs = parsers.parse_juriscan('')
    assert rs.is_success()
    assert rs.value == set()


# -------------------------------------------[ Tests para parse_uuid ]--


def test_parse_uuid_empty():
    assert parsers.parse_uuid('').is_success()


def test_parse_uuid_bad():
    assert parsers.parse_uuid('María tenía un corderito').is_failure()


def test_parse_uuid():
    expected = UUID('20f5484b-88ae-49b0-8af0-3a389b4917dd')
    r = parsers.parse_uuid('20f5484b-88ae-49b0-8af0-3a389b4917dd')
    assert r.is_success() and r.value == expected


# ---------------------------[ Tests para parse_materia_competencial ]--


@pytest.mark.django_db
def test_parse_materia_competencial_codigo():
    hacienda = Tema.load_tema('HAC')
    rs = parsers.parse_materia_competencial('HAC')
    assert rs.is_success() and rs.value == hacienda


@pytest.mark.django_db
def test_parse_materia_competencial_descripcion():
    hacienda = Tema.load_tema('HAC')
    rs = parsers.parse_materia_competencial('Hacienda')
    assert rs.is_success() and rs.value == hacienda


@pytest.mark.django_db
def test_parse_materia_competencial_empty():
    expected = Tema.load_tema('UNK')
    rs = parsers.parse_materia_competencial('')
    assert rs.is_success() and rs.value == expected


@pytest.mark.django_db
def test_parse_materia_competencial_none():
    expected = Tema.load_tema('UNK')
    rs = parsers.parse_materia_competencial(None)
    assert rs.is_success() and rs.value == expected


@pytest.mark.django_db
def test_parse_materia_competencial_failure():
    rs = parsers.parse_materia_competencial(r'¯\_(ツ)_/¯')
    assert rs.is_failure()


@pytest.mark.django_db
def test_parse_row():
    jrodleo = Usuario.load_usuario('jrodleo')
    malosua = Usuario.load_usuario('malosua')
    juriscan_5559 = Juriscan.load_or_create(5559)
    hacienda = Tema.load_tema('HAC')
    row = (
        "Nombre del sistema",                   # Nombre
        'CODIGO',                               # Código
        "Esta es la finalidad",                 # Finalidad
        'HAC',                                  # Materia compotencial
        'A05003248',                            # DIR3
        'jrodleo, malosua',                     # Resp. tecnológico
        'malosua',                              # Resp. funcional
        '5559',                                 # Normativa
        'Este es el comentario',                # Comentarios
        '2b4c67ad-cf08-11f0-bdf7-38d5470ea667', # uuid
        )
    data = parsers.parse_row(row)
    assert data['nombre_sistema'].value == 'Nombre del sistema'
    assert data['codigo'].value == 'CODIGO'
    assert data['finalidad'].value == 'Esta es la finalidad'
    assert data['descripcion'].value == ''
    assert data['tema'].value == hacienda
    assert data['organismo'].value == Organismo.load_organismo(42093)
    assert data['responsables_tecnologicos'].value == set([jrodleo, malosua])
    assert data['responsables_funcionales'].value == set([malosua])
    assert data['juriscan'].value == set([juriscan_5559])
    assert data['comentarios'].value == 'Este es el comentario'
    assert data['uuid'].value == UUID('2b4c67ad-cf08-11f0-bdf7-38d5470ea667')


if __name__ == '__main__':
    pytest.main()
