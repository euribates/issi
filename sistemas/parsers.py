from html import escape
import re
import uuid

DEFAULT_DOMAIN = 'gobiernodecanarias.org'

pat_username = re.compile(r"[a-zA-Z0-9_.+-]+$")
pat_email = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
pat_full = re.compile(r"(.+)\s+<(.+)>$")


def parse_users(txt: str) -> set[dict]:
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
        f'No puedo interpretar "{escape(txt)}" como un usuario válido.'
        )

pat_integer = re.compile('\d+$')
pat_comma = re.compile('\s*,\s*')
pat_url_juriscan = re.compile(
    'https?://www\d?\.gobiernodecanarias\.org/juriscan/ficha\.jsp\?id=(\d+)'
    )

def parse_juriscan(txt: str) -> list[int]:
    result = []
    txt = txt.strip()
    match = pat_integer.match(txt)
    if match:
        result.append(int(match.group(0)))
        return result
    if ',' in txt:
        for item in pat_comma.split(txt):
            values = parse_juriscan(item)
            if values:
                result.extend(values)
        return result
    for match in pat_url_juriscan.finditer(txt):
        result.append(int(match.group(1)))
    return result


PAT_UUID = re.compile(r'[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)

def parse_uuid(txt: str) -> uuid.UUID|None:
    txt = txt.strip()
    if txt == '':
        return None
    match = PAT_UUID.match(txt)
    if match:
        return uuid.UUID(txt)
    raise ValueError(
        'Esperaba un UUID, pero el dato {escape(txt)}'
        ' no tiene el formato adecuado'
        )
