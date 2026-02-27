 #!/usr/bin/env python3

import json
from typing import Iterable

from django.utils.safestring import mark_safe

from comun.colors import Color
from comun.colors import BLACK, WHITE


class Serie:

    def __init__(self, label, values: Iterable, **kwargs):
        self.label = label
        self.values = list(values)
        self.fill = kwargs.get('fill', True)
        self.background_color = str(kwargs.get('background_color', Color('Coral')))
        self.border_color = str(kwargs.get('border_color', Color('AliceBLue')))
        self.point_background_color = str(Color(255, 99, 132))
        self.point_border_color = str(BLACK)
        self.point_hover_background_color = str(WHITE)
        self.point_hover_border_color = str(Color(255, 99, 132))


class PolarArea:

    def __init__(self, title):
        self.title = title
        self.items = []

    def add_value(self, label, value, color):
        self.items.append({
            'label': label,
            'value': value,
            'color': color,
            })

    def _as_data(self):
        result = {}
        result['labels'] = [_['label'] for _ in self.items]
        result['datasets'] = [{
            'label': self.title,
            'data': [_['value'] for _ in self.items],
            'backgroundColor': [_['color'] for _ in self.items],
            }]
        return json.dumps(result, indent=4)

    def _as_config(self):
        return ('\n'.join([
            "{",
            "  'type': 'polarArea',",
            "  'data': data,",
            "  'options': {",
            "     scales: {",
            "       r: {",
            "           beginAtZero: true,",
            "           min: 0,",
            "           max: 80",
            "         }",
            "       },",
            "    'elements': {",
            "      'line': {",
            "        'borderWidth': 2",
            "      }",
            "    }",
            "  },",
            "}"
            ]))

    def as_javascript(self):
        return mark_safe('\n'.join([
            '<script type="text/javascript">',
            f'const data = {self._as_data()};'
            f'const config = {self._as_config()};' 
            'var ctx = document.getElementById("Chart");',
            'var chart = new Chart(ctx, config);',
            '</script>',
            ]))



class Radar:

    def __init__(self, title):
        self.title = title
        self.axis = []
        self.series = []

    def add_axis(self, axis_name: str):
        self.axis.append(axis_name)
        
    def add_series(self, label: str, values: Iterable, **kwargs):
        assert len(values) == len(self.axis)
        self.series.append(Serie(label, list(values), **kwargs))

    def _as_data(self):
        result = {}
        result['labels'] = self.axis
        result['datasets'] = []
        for serie in self.series:
            result['datasets'].append({
                'label': serie.label,
                'data': serie.values,
                'fill': serie.fill,
                'backgroundColor': serie.background_color,
                'borderColor': serie.border_color,
                'pointBackgroundColor': serie.point_background_color,
                'pointBorderColor': serie.point_border_color,
                'pointHoverBackgroundColor': serie.point_hover_background_color,
                'pointHoverBorderColor': serie.point_hover_border_color,    
                })
        return json.dumps(result, indent=4)

    def _as_config(self):
        return ('\n'.join([
            "{",
            "  'type': 'radar',",
            "  'data': data,",
            "  'options': {",
            "     scales: {",
            "       r: {",
            "           angleLines: {",
            "               display: true",
            "           },",
            "           min: 0,",
            "           max: 20",
            "         }",
            "       },",
            "    'elements': {",
            "      'line': {",
            "        'borderWidth': 2",
            "      }",
            "    }",
            "  },",
            "}"
            ]))

    def as_javascript(self):
        return mark_safe('\n'.join([
            '<script type="text/javascript">',
            f'const data = {self._as_data()};'
            f'const config = {self._as_config()};' 
            'var ctx = document.getElementById("Chart");',
            'var chart = new Chart(ctx, config);',
            '</script>',
            ]))
