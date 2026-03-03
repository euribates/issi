 #!/usr/bin/env python3

from collections import OrderedDict
from dataclasses import dataclass
from html import escape
from typing import Iterable
import math

from django.template.loader import get_template

from comun.colors import Color
from comun.colors import Palette


DEFAULT_WIDTH = 250
DEFAULT_HEIGHT = 250


@dataclass()
class Axis:
    name: str
    label: str
    values: list

    def __init__(self, name: str, label: str|None):
        self.name = name
        self.label = label or name
        self.values = []


@dataclass(frozen=True)
class Serie:
    values: tuple
    label: str
    color: Color


class PolarChart:

    def __init__(self, title, **kwargs):
        self.title = title
        self.width = kwargs.pop('width', DEFAULT_WIDTH)
        self.height = kwargs.pop('height', DEFAULT_HEIGHT)
        self.max_value = kwargs.pop('max_value', 100)
        palette = kwargs.pop('palette', 'default')
        self.palette = Palette[palette]
        self.radio = 100
        self.series = []
        self.axis = OrderedDict({})  # Es importante que el diccionario 

    def scale(self, v: float) -> float:
        return v * self.radio / self.max_value

    def polar_to_coord(self, value, angle):
        angle = angle - (math.tau / 3.)
        value = self.scale(value)
        return (
            str(round(math.cos(angle) * value, 2)),
            str(round(math.sin(angle) * value, 2)),
            )

    def add_axis(self, name, label=None):
        """Añade un eje al diagrama.
        """
        self.axis[name] = Axis(name, label)

    def add_serie(self, values: Iterable, label='', color=None):
        assert len(values) == len(self.axis)
        num_series = len(self.series)
        label = label or f'Serie {num_series + 1}'
        color = color or self.palette[num_series]
        for axis_name, value in zip(self.axis.keys(), values):
            if value > self.max_value:
                raise ValueError(
                    'Se ha definido el gráfico polar con un '
                    f' valor máximo de {self.max_value}'
                    f' pero se ha pasado el valor {escape(value)}'
                    ' que inclumple este criterio.'
                    )
            self.axis[axis_name].values.append(value)
        self.series.append(Serie(tuple(values), label, color))

    def as_svg(self) -> str:
        angle = math.tau / len(self.axis)
        template = get_template('comun/charts/polar.svg')
        coords = [
            tuple([
                axis_name,
                *self.polar_to_coord(self.max_value, angle * i),
                ])
            for i, axis_name in enumerate(self.axis)
            ]
        polygons = []
        for index, serie in enumerate(self.series):
            l_points = [
                tuple([
                    *self.polar_to_coord(value, angle * i),
                    value,
                    ])
                for i, value in enumerate(serie.values)
                ]
            l_points.append(l_points[0])  # Close the polygon
            s_points = ' '.join([f'{x},{y}' for x, y, _ in l_points])
            stroke_color = Color(serie.color)
            fill_color = stroke_color.change(alpha=160)
            polygons.append(
                '<g scale="0 0">'    
                f' <animateTransform attributeName="transform"'
                '    type="scale"'
                '    from="0 0"'
                '    to="1 1"'
                f'    begin="{index}s"'
                '    dur="1.2s"'
                '    />\n'
                f'<polygon scale="0 0"'
                f' points="{s_points}"'
                f' fill="{fill_color}" stroke="{stroke_color}">\n'
                '</polygon>\n'
                )
            for (x, y, v) in l_points[0:-1]:
                polygons.append(
                    f'<circle cx="{x}" cy="{y}" r="3"'
                    f' fill="{stroke_color}">'
                    f'<title>{v}</title>'
                    '</circle>'
                    )
            polygons.append('</g>')
        context = {
            'chart': self,
            'angle': angle,
            'data': self.axis.items(),
            'coords': coords,
            'polygons': polygons,
            }
        return template.render(context)
