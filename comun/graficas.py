 #!/usr/bin/env python3

from collections import OrderedDict
from dataclasses import dataclass
from html import escape
from typing import Iterable
import math

from django.template.loader import get_template
from django.utils.safestring import mark_safe

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



PIE_COORDS = [
    (0, 0.0, -40.0), (0, 2.51, -39.92), (0, 5.01, -39.68), (0, 7.5, -39.29),
    (0, 9.95, -38.74), (0, 12.36, -38.04), (0, 14.72, -37.19), (0, 17.03, -36.19),
    (0, 19.27, -35.05), (0, 21.43, -33.77), (0, 23.51, -32.36), (0, 25.5, -30.82),
    (0, 27.38, -29.16), (0, 29.16, -27.38), (0, 30.82, -25.5), (0, 32.36, -23.51),
    (0, 33.77, -21.43), (0, 35.05, -19.27), (0, 36.19, -17.03), (0, 37.19, -14.72),
    (0, 38.04, -12.36), (0, 38.74, -9.95), (0, 39.29, -7.5), (0, 39.68, -5.01),
    (0, 39.92, -2.51), (0, 40.0, -0.0), (0, 39.92, 2.51), (0, 39.68, 5.01),
    (0, 39.29, 7.5), (0, 38.74, 9.95), (0, 38.04, 12.36), (0, 37.19, 14.72),
    (0, 36.19, 17.03), (0, 35.05, 19.27), (0, 33.77, 21.43), (0, 32.36, 23.51),
    (0, 30.82, 25.5), (0, 29.16, 27.38), (0, 27.38, 29.16), (0, 25.5, 30.82),
    (0, 23.51, 32.36), (0, 21.43, 33.77), (0, 19.27, 35.05), (0, 17.03, 36.19),
    (0, 14.72, 37.19), (0, 12.36, 38.04), (0, 9.95, 38.74), (0, 7.5, 39.29),
    (0, 5.01, 39.68), (0, 2.51, 39.92), (1, 0.0, 40.0), (1, -2.51, 39.92),
    (1, -5.01, 39.68), (1, -7.5, 39.29), (1, -9.95, 38.74), (1, -12.36, 38.04),
    (1, -14.72, 37.19), (1, -17.03, 36.19), (1, -19.27, 35.05), (1, -21.43, 33.77),
    (1, -23.51, 32.36), (1, -25.5, 30.82), (1, -27.38, 29.16), (1, -29.16, 27.38),
    (1, -30.82, 25.5), (1, -32.36, 23.51), (1, -33.77, 21.43), (1, -35.05, 19.27),
    (1, -36.19, 17.03), (1, -37.19, 14.72), (1, -38.04, 12.36), (1, -38.74, 9.95),
    (1, -39.29, 7.5), (1, -39.68, 5.01), (1, -39.92, 2.51), (1, -40.0, 0.0),
    (1, -39.92, -2.51), (1, -39.68, -5.01), (1, -39.29, -7.5), (1, -38.74, -9.95),
    (1, -38.04, -12.36), (1, -37.19, -14.72), (1, -36.19, -17.03), (1, -35.05, -19.27),
    (1, -33.77, -21.43), (1, -32.36, -23.51), (1, -30.82, -25.5), (1, -29.16, -27.38),
    (1, -27.38, -29.16), (1, -25.5, -30.82), (1, -23.51, -32.36), (1, -21.43, -33.77),
    (1, -19.27, -35.05), (1, -17.03, -36.19), (1, -14.72, -37.19), (1, -12.36, -38.04),
    (1, -9.95, -38.74), (1, -7.5, -39.29), (1, -5.01, -39.68), (1, -2.51, -39.92),
    (1, -0.01, -40.0)
    ]


class Doughnut:

    def __init__(self, good=33, regular=33, bad=33, width=256, height=256):
        self.good = good
        self.regular = regular
        self.bad = bad
        self.width = width
        self.height = height

    def url(self):
        return "/comun/charts/doughnut/?g={g}&r={r}&b={b}".format(
            g=self.good,
            r=self.regular,
            b=self.bad,
            )

    def as_html(self):
        return mark_safe(
            '<img'
            f' width="{self.width}" height="self.height"'
            f' src="{self.url()}">'
            )

    def _make_chart(self, percent, color='Lime') -> str:
        buff = [
            f'<path stroke="{color}" stroke-width="16" fill="none">',
            ' <animate attributeName="d" calcMode="spline" values="',
            ]
        for counter, coord in enumerate(PIE_COORDS):
            flag, x, y = coord
            buff.append(f'M 0,-40 A 40,40 0 {flag} 1 {x:.2f},{y:.2f};')
            if counter >= percent:
                break
        buff.append('" dur="0.8s" repeatCount="1" fill="freeze" />')
        buff.append('</path>\n')
        return ''.join(buff)


    def as_svg(self):
        total = self.bad + self.regular + self.good
        red_percent = int(round(self.bad * 100.0 / total))
        yellow_percent = int(round((self.bad+self.regular) * 100.0 / total))
        green_percent = 100
        template = get_template('comun/charts/doughnut.svg')
        return template.render({
            'width': self.width,
            'height': self.height,
            'bad': self.bad,
            'regular': self.regular,
            'good': self.good,
            'total': total,
            'green_chart': self._make_chart(percent=green_percent, color="#00a443"),
            'yellow_chart': self._make_chart(percent=yellow_percent, color="#f5d80a"),
            'red_chart': self._make_chart(percent=red_percent, color="#e40405"),
            })
