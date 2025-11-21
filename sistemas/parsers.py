from html import escape
import re

DEFAULT_DOMAIN = 'gobiernodecanarias.org'

pat_username = re.compile(r"[a-zA-Z0-9_.+-]+$")
pat_email = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
pat_full = re.compile(r"(.+)\s+<(.+)>$")


def parse_user(s: str) -> dict|None:
    s = s.strip()
    if not s:
        return None
    match = pat_full.match(s)
    if match:
        name = match.group(1)
        email = match.group(2)
        if pat_email.match(email):
            login = email.split('@', 1)[0]
            return {
                'name': name,
                'login': login,
                'email': email,
                }
    match = pat_email.match(s)
    if match:
        login = s.split('@', 1)[0]
        return {
            'name': None,
            'login': login,
            'email': s,
            }
    match = pat_username.search(s)
    if match:
        return {
            'name': None,
            'login': s,
            'email': f'{s}@{DEFAULT_DOMAIN}'
            }
    raise ValueError(
        f'No puedo interpretar "{escape(s)}" como un usuario válido.'
        )
