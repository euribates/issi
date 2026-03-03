#!/usr/bin/env python3

from django import template

register = template.Library()


class MapNode(template.Node):

    def __init__(self, object_name, index_name, output_var):
        self.object_name = object_name
        self.index_name = index_name
        self.output_var = output_var

    def render(self, context, renderer=None):
        if '.' in self.object_name:
            items = self.object_name.split('.')
            var = context[items[0]]
            for nodo in items[1:]:
                var = getattr(var, nodo)
        else:
            var = context[self.object_name]

        if '.' in self.index_name:
            items = self.index_name.split('.')
            index = context[items[0]]
            for nodo in items[1:]:
                if isinstance(index, dict):
                    index = index[nodo]
                else:
                    index = getattr(index, nodo)
        else:
            index = context[self.index_name]
        if callable(var):
            context[self.output_var] = var(index)
        elif hasattr(var, '__getitem__'):
            context[self.output_var] = var[index]
        else:
            context[self.output_var] = (
                '<p>ERROR: No puedo acceder a {} en variable {}</p>'.format(
                    self.index_name,
                    self.object_name
                ))
        return ''


@register.tag(name='map')
def tag_map(_parser, token):
    """Para usar el tag hay que 
        Si suponemos una variable `data` (por ejemplo, un
        diccionario), y una clave `key` (por ejemplo, un texto), ambos
        accesibles en el contexto pasado a la plantilla, haríamos:

            {% map d using k as v %}
    
        Esto incluiría en el contexto el valor de d[k].

        Funciona para más cosas que diccionarios:

        - Si `data` es un objeto con un *callable* `key`, que
          acepta un único parámetro, el valor introducido
          en el contexto es `data(key)`

        - Si `data` es un objeto con un atributo `key`
          el valor introducido en el contexto es `data.key`

        - Si `data` es una lista o una tupla, y `key` es un
          número entero, se introduce en el contexto `data[key]`.

        - Si `data` es un diccionario, y `key` es una clave
          del mismo, se introduce en el contexto `data[key]`.
    """   
    try:
        (tag_name,
            object_name,
            _using_text_literal,
            index_name,
            _as_text_literal,
            output_var
            ) = token.split_contents()
        assert tag_name == 'map'
        assert _using_text_literal == 'using'
        assert _as_text_literal == 'as'
    except ValueError as err:
        raise template.TemplateSyntaxError(
            "Al tag {} le falta un parametro".format(token)
            ) from err
    return MapNode(object_name, index_name, output_var)
