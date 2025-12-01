from html import escape
import re
import uuid

from directorio.models import Organismo
from sistemas.models import Tema
from sistemas.models import Sistema


DEFAULT_DOMAIN = 'gobiernodecanarias.org'

pat_username = re.compile(r"[a-zA-Z0-9_.+-]+$")
pat_email = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
pat_full = re.compile(r"(.+)\s+<(.+)>$")


def parse_codigo_interno(n_linea: int, codigo: str):
    codigo = codigo.strip()
    if not codigo:
        raise ValueError(
            f"En la linea {n_linea},"
            ' no se ha definido el código interno'
            )
    pat_codigo_interno = re.compile(r'[A-Z_][0-9A-Z_][0-9A-Z_]+$')
    _match = pat_codigo_interno.match(codigo)
    if not _match:
        raise ValueError(
            f"En la linea {n_linea},"
            ' el formato del código interno no es válido.'
            ' Solo son válidos los caracteres desde la A'
            ' hasta la Z, sin minúsculas, los dígitos desde'
            ' el cero hasta el nueve, y el caracter subrayado.'
            ' Además, no puede empezar por un dígito, y debe'
            ' tener tres o más caracteres. El valor suministrado'
            f' {escape(codigo)} no sigue el formato.'
            )
    return codigo



def parse_dir3(n_linea, dir3):
    dir3 = dir3.strip()
    if not dir3:
        return None
    organismo = Organismo.load_organismo_using_dir3(dir3)
    if not organismo:
        raise ValueError(
            f'En la fila {n_linea},'
            f' el DIR3 indicado: {escape(dir3)}'
            ' no parece correcto.'
            )
    return organismo


def parse_materia_competencial(n_linea: int, materia: str) -> Tema|None:
    materia = materia.strip()
    if not materia:
        return Tema.load_tema('UNK')
    tema = Tema.load_tema(materia)
    if not tema:
        tema = Tema.load_tema_por_nombre(materia)
        if not tema:
            raise ValueError(
                f'En la fila {n_linea},'
                f' el tema indicado: {escape(materia)}'
                ' no existe.'
                )
    return tema


def parse_users(n_linea: int, txt: str) -> set[dict]:
    result = []
    txt = txt.strip()
    if not txt:
        return result
    if ',' in txt:
        for item in pat_comma.split(txt):
            values = parse_users(item)
            if values:
                result.extend(values)
        return result
    match = pat_full.match(txt)
    if match:
        name = match.group(1)
        email = match.group(2)
        if pat_email.match(email):
            login = email.split('@', 1)[0]
            return [{
                'name': name,
                'login': login,
                'email': email,
    }]
    match = pat_email.match(txt)
    if match:
        login = txt.split('@', 1)[0]
        return [{
            'name': None,
            'login': login,
            'email': txt,
            }]
    match = pat_username.search(txt)
    if match:
        return [{
            'name': None,
            'login': txt,
            'email': f'{txt}@{DEFAULT_DOMAIN}'
            }]
    raise ValueError(
        f'En la linea {n_linea},'    
        f' no puedo interpretar "{escape(txt)}"'
        ' como un usuario válido.'
        )

pat_integer = re.compile(r'\d+$')
pat_comma = re.compile(r'\s*,\s*')
pat_url_juriscan = re.compile(
    r'https?://www\d?\.gobiernodecanarias\.org/juriscan/ficha\.jsp\?id=(\d+)'
    )


def parse_juriscan(n_linea: int, txt: str) -> list[int]:
    result = []
    txt = txt.strip()
    match = pat_integer.match(txt)
    if match:
        result.append(int(match.group(0)))
        return result
    if ',' in txt:
        for item in pat_comma.split(txt):
            values = parse_juriscan(n_linea, item)
            if values:
                result.extend(values)
        return result
    for match in pat_url_juriscan.finditer(txt):
        result.append(int(match.group(1)))
    return result


PAT_UUID = re.compile(r'[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)


def parse_uuid(n_linea: int, txt: str) -> uuid.UUID|None:
    txt = txt.strip()
    if txt == '':
        return None
    match = PAT_UUID.match(txt)
    if match:
        return uuid.UUID(txt)
    raise ValueError(
        f'En la línea {n_linea},'
        f' esperaba un UUID, pero el dato {escape(txt)}'
        ' no tiene el formato adecuado.'
        )


def parse_row(n_linea, tupla):
    n_cols = len(tupla)
    errors = []
    nombre_sistema = tupla[0]
    codigo = None
    try:
        codigo = parse_codigo_interno(n_linea, tupla[1])
    except ValueError as err:
        errors.append(err)
    finalidad = tupla[2]
    proposito = finalidad
    descripcion = ''
    if finalidad:
        sublines = finalidad.splitlines()
        if len(sublines) == 0:
            proposito = ''
        if len(sublines) == 1:
            proposito = sublines[0]
        else:
            proposito = sublines[0]
            descripcion = '\n\n'.join(sublines[1:])
    try:
        tema = parse_materia_competencial(n_linea, tupla[3])
    except ValueError as err:
        errors.append(err)

    organismo = None
    try:
        organismo = parse_dir3(n_linea, tupla[4])
    except ValueError as err:
        errors.append(err)

    try:
        responsables_tecnologicos = parse_users(n_linea, tupla[5])
    except ValueError as err:
        errors.append(err)

    try:
        responsables_funcionales =  parse_users(n_linea, tupla[6])
    except ValueError as err:
        errors.append(err)

    try:
        juriscan = parse_juriscan(n_linea, tupla[7])
    except ValueError as err:
        errors.append(err)

    comentarios = f'{tupla[8]}\n\n{tupla[7]}'

    id_sistema = None
    uuid_sistema = None
    if n_cols == 10:
        uuid_sistema = parse_uuid(n_linea, tupla[9])
        if uuid_sistema:
            sistema = Sistema.load_sistema_por_uuid(uuid_sistema)
            if sistema:
                id_sistema = sistema.pk
    payload = {
        'id_sistema': id_sistema,
        'uuid': uuid_sistema,
        'nombre_sistema': nombre_sistema,
        'organismo': organismo,
        'codigo': codigo,
        'proposito': proposito,
        'descripcion': descripcion,
        'observaciones': comentarios,
        'tema': tema,
        'juriscan': juriscan,
        'responsables_tecnologicos': responsables_tecnologicos,
        'responsables_funcionales': responsables_funcionales,
        }
    return errors, payload
