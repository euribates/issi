#!/usr/bin/env python3

import pytest
from uuid import UUID

from comun.funcop import first

from sistemas import parsers
from sistemas.models import Usuario
from sistemas.models import Tema
from juriscan.models import Juriscan
from directorio.models import Organismo


# --------------------------------------------------------[ Fixtures ]--

@pytest.fixture
def jrodleo():
    return Usuario.load_usuario('jrodleo')


@pytest.fixture
def malosua():
    return Usuario.load_usuario('malosua')


@pytest.fixture
def juriscan_5559():
    return Juriscan.load_or_create(5559)


@pytest.fixture
def juriscan_sample():
    return set([
        Juriscan.load_or_create(5559),
        Juriscan.load_or_create(79558),
        ])


@pytest.fixture
def hacienda():
    return Tema.load_tema('HAC')


@pytest.fixture
def materia_desconocida():
    return Tema.load_tema('UNK')


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
def test_parse_users_single_username(jrodleo):
    users = parsers.parse_users('jrodleo')
    assert len(users) == 1
    r = first(users)
    assert r.is_success() and r.value == jrodleo


@pytest.mark.django_db
def test_parse_users_double_username(malosua, jrodleo):
    users = parsers.parse_users('malosua, jrodleo')
    for r in users:
        assert r.is_success()
        user = r.value
        match user.login:
            case 'jrodleo':
                assert user == jrodleo
            case 'malosua':
                assert user == malosua
            case _:
                raise ValueError('No debería pasar nunca, pero aquí estamos...')


@pytest.mark.django_db
def test_parse_users_single_email(jrodleo):
    r = first(parsers.parse_users('jrodleo@gobiernodecanarias.org'))
    assert r.is_success()
    assert r.value == jrodleo


@pytest.mark.django_db
def test_parse_user_full_email(jrodleo):
    r = first(parsers.parse_users('Juan Ignacio <jrodleo@gobiernodecanarias.org>'))
    assert r.is_success()
    assert r.value == jrodleo


@pytest.mark.django_db
def test_parse_users_bad_input():
    users = parsers.parse_users("I'm Bad! Bad! (Really, really bad)")
    assert len(users) == 2
    for r in users:
        assert r.is_failure()


@pytest.mark.django_db
def test_parse_users_void_input():
    assert parsers.parse_users('') == set([])


@pytest.mark.django_db
def test_parse_juriscan_single_number():
    result = first(parsers.parse_juriscan('5559'))
    assert result.is_success()
    assert isinstance(result.value, Juriscan)
    assert result.value.titulo == 'Ley 2/1984, 11 abril, de Premios Canarias'


@pytest.mark.django_db
def test_parse_juriscan_double_number(juriscan_sample):
    expected = juriscan_sample
    for rj in parsers.parse_juriscan('79558, 5559'):
        assert rj.is_success()
        assert rj.value in expected
    for rj in parsers.parse_juriscan('79558; 5559'):
        assert rj.is_success()
        assert rj.value in expected


@pytest.mark.django_db
def test_parse_juriscan_en_diferentes_lineas(juriscan_sample):
    expected = juriscan_sample
    for rj in parsers.parse_juriscan('79558\n5559'):
        assert rj.is_success()
        assert rj.value in expected


@pytest.mark.django_db
def test_parse_juriscan_link(juriscan_sample):
    expected = juriscan_sample
    url = 'https://www3.gobiernodecanarias.org/juriscan/ficha.jsp?id=5559'
    rj = first(parsers.parse_juriscan(url))
    assert rj.is_success()
    assert rj.value in expected


@pytest.mark.django_db
def test_parse_juriscan_multiples_enlaces(juriscan_sample):
    expected = juriscan_sample
    urls = (
        'https://www3.gobiernodecanarias.org/juriscan/ficha.jsp?id=5559\n'
        'https://www3.gobiernodecanarias.org/juriscan/ficha.jsp?id=79558&from=0&nreg=25&materiasop=AND&materias1=*&materias2=*&rango1=*&rango2=*&titulo=internet&desdeemi=&hastaemi=&ordendesc=IdRango&orden=asc&numdisp=0&tituloAux=internet.'
        )
    for rj in parsers.parse_juriscan(urls):
        assert rj.is_success()
        assert rj.value in expected


def test_parse_juriscan_empty():
    assert parsers.parse_juriscan('') == set()


# -------------------------------------------[ Tests para parse_uuid ]--


def test_parse_uuid_empty():
    assert parsers.parse_uuid('').is_failure()


def test_parse_uuid_bad():
    assert parsers.parse_uuid('María tenía un corderito').is_failure()


def test_parse_uuid():
    expected = UUID('20f5484b-88ae-49b0-8af0-3a389b4917dd')
    r = parsers.parse_uuid('20f5484b-88ae-49b0-8af0-3a389b4917dd')
    assert r.is_success() and r.value == expected


# ---------------------------[ Tests para parse_materia_competencial ]--


@pytest.mark.django_db
def test_parse_materia_competencial_codigo(hacienda):
    rs = parsers.parse_materia_competencial('HAC')
    assert rs.is_success() and rs.value == hacienda


@pytest.mark.django_db
def test_parse_materia_competencial_descripcion(hacienda):
    rs = parsers.parse_materia_competencial('Hacienda')
    assert rs.is_success() and rs.value == hacienda


@pytest.mark.django_db
def test_parse_materia_competencial_empty(materia_desconocida):
    rs = parsers.parse_materia_competencial('')
    assert rs.is_success() and rs.value == materia_desconocida


@pytest.mark.django_db
def test_parse_materia_competencial_none(materia_desconocida):
    rs = parsers.parse_materia_competencial(None)
    assert rs.is_success() and rs.value == materia_desconocida


@pytest.mark.django_db
def test_parse_materia_competencial_failure():
    rs = parsers.parse_materia_competencial(r'¯\_(ツ)_/¯')
    assert rs.is_failure()


@pytest.mark.django_db
def test_parse_row(hacienda, jrodleo, malosua, juriscan_5559):
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
    assert data['proposito'].value == 'Esta es la finalidad'
    assert data['descripcion'].value == ''
    assert data['tema'].value == hacienda
    assert data['organismo'].value == Organismo.load_organismo(42093)
    for rs in data['responsables_tecnologicos']:
        assert rs.is_success()
        user = rs.value
        match user.login:
            case 'jrodleo':
                assert user == jrodleo
            case 'malosua':
                assert user == malosua
            case _:
                raise ValueError(f'No se esperaba {user}')
    assert first(data['responsables_funcionales']).value == malosua
    assert first(data['juriscan']).value == juriscan_5559
    assert data['comentarios'].value == 'Este es el comentario'
    assert data['uuid'].value == UUID('2b4c67ad-cf08-11f0-bdf7-38d5470ea667')


if __name__ == '__main__':
    pytest.main()
