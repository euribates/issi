#!/usr/bin/env python

from django import template


register = template.Library()


class CardFooter(template.Node):
    """Nodo para añadir un pie a las cards.
    """

    def __init__(self, body):
        self.body = body

    def render(self, context):
        if 'this_card' in context:
            this_card = context['this_card']
            this_card.footer = self.body.render(context)
        return ''


def card_footer(parser, token):
    """Función que permite añadir un footer al panel.
    """
    args = token.split_contents()
    if len(args) != 1:
        raise ValueError(
            'wrong number of arguments\n'
            'The card_footer requires no arguments'
        )
    body = parser.parse(('end_card_footer',))
    parser.delete_first_token()
    return CardFooter(body)


register.tag('card_footer', card_footer)


class CardNode(template.Node):  # Bootstrap 5
    """
    Clase para declarar un elemento Card. Este template tiene un
    estilo con nombre de clases de boostrap 5. Recibe como parámetros
    opcionales:

    - ``title``: El título que tendrá el panel. Si no indicamos
      nada, no se pondrá ningún título.

    - ``subtitle``: Un subtítulo. Si no indicamos nada, no se
      usará. Nota: Tampoco se usará si **no** se ha definido 
      un título.

    - ``klass``: la clase, usando el parámetro `klass` (por 
      defecto vale `card-default`)

    - ``counter``: Un contador, que se mostrará como
      un _badge_. Por defecto vale `None`, que implica que
      no se mostrará.

    - ``url``: Un enlace. Si se incluye, el título
      del panel redirige a ese enlace. Nota: Si no se define
      el título, no se usará.

    - ``image``: El url a una imagen, que se pondrá en la parte
      superior del ``card``.

    Todo el cuerpo contenido dentro de las etiquetas formará parte
    del cuerdo del card (``card-body``).
    """
    def __init__(self, tag_name, title='', **kwargs):
        self.tag_name = tag_name
        self.title = title
        self.subtitle = kwargs.pop('subtitle', None)
        self.klass = kwargs.pop('klass', None)
        self.counter = kwargs.pop('counter', None)
        self.body = kwargs.pop('body')
        self.url = kwargs.pop('url', '')
        self.image = kwargs.pop('image', '')
        self.footer = None
        self.counter_classes = (
            'badge'
            ' position-absolute top-0 end-0'
            ' rounded-pill text-bg-info'
            ' p-1 m-2'
            )

    def render(self, context):
        """
        Método que añade al panel la información que se quiere
        mostrar en el mismo.
        """
        title = self.title.resolve(context) if self.title else ''
        subtitle = self.subtitle.resolve(context) if self.subtitle else None
        klass = self.klass.resolve(context) if self.klass else 'card-default'
        url = self.url.resolve(context) if self.url else None
        image = self.image.resolve(context) if self.image else None
        counter = self.counter.resolve(context) if self.counter else None
        buff = [
            f'<div class="card mt-2 mb-2" role="navigation"'
            f' aria-label="{title}">\n',
            ]
        context["this_card"] = self

        if image:
            buff.append(f' <img src="{image}" class="card-img-top">')
        if counter is not None:
            buff.append(
                f'<span class="{self.counter_classes}">'
                f'{counter}'
                '</span>'
                )
        if title:
            buff.append(f' <div class="card-header {klass}">')
            buff.append(' <h4 class="card-title">')
            if url:
                buff.append(f'<a href="{url}">{title}</a>')
            else:
                buff.append(str(title))
            buff.append('</h4>')
            if subtitle:
                buff.append(f' <h5 class="card-subtitle">{subtitle}</h5>')
            buff.append('</div>')
        buff.append(self.body_start_tag())
        buff.append(self.body.render(context))
        buff.append(self.body_end_tag())
        if self.footer:
            buff.append(f'<div class="card-footer">')
            buff.append(self.footer)
            buff.append('</div>')
        buff.append('</div>\n')
        return '\n'.join(buff)

    def body_start_tag(self):
        """
        Método para añadir las etiquetas al comienzo del panel
        """
        return {
            'card': ' <div class="card-body">\n',
            'list_card': '  <ul class="list-group">\n',
            'table_card': '  <table class="table table-hover">\n',
            }.get(self.tag_name)

    def body_end_tag(self):
        """
        Método para añadir los cierres de etiqueta del panel
        """
        return {
            'card': ' </div>\n',
            'list_card': ' </ul>\n',
            'table_card': ' </table>\n',
            }.get(self.tag_name)


def card(parser, token):
    """
    Función que permite utilizar el panel y añadirle los argumentos que necesite.
    """
    args = token.split_contents()
    kwargs = {}
    if len(args) == 1:
        tag_name = args[0]
        title = None  # Sin titulo
    elif len(args) == 2:
        tag_name, title = args
    else:
        tag_name, title, *params = args
        for item in params:
            (name, str_value) = item.split('=', 1)
            try:
                value = template.Variable(str_value)
            except TypeError:
                value = str(str_value)
            kwargs[name] = value
    kwargs['body'] = parser.parse(('end_card',))
    parser.delete_first_token()
    return CardNode(
        tag_name,
        template.Variable(title) if title else None,
        **kwargs,
        )


register.tag('card', card)
register.tag('list_card', card)
register.tag('table_card', card)
