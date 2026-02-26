 #!/usr/bin/env python3

from typing import Iterable

from comun.colors import Color
from comun.colors import BLACK, WHITE


class Serie:

    def __init__(self, label, values: Sequence, **kwargs):
        self.label = label
        self.values = list(value)
        self.fg_color = kwargs.get('fg_color', Color('AliceBLue'))
        self.bg_color = kwargs.get('fg_color', BLACK)


class Radar():

    def __init__(self, title, fill=True):
        self.title = title
        self.axis = []
        self.series = []
        self.fill = fill

    def add_axis(self, axis_name: str):
        self.axis.append(axis_name)
        
    def add_series(self, label: str, values: Iterable, **kwargs):
        assert len(values) == len(self.axis)
        self.series.append(Serie(label, values, **kwargs))

    def _as_data(self):
        result = {}
        result['labels'] = self.axis
        result['datasets'] = []
        for serie in self.series:
            result['datasets'].append({
                'label': serie.label,
                'data': serie.values,
                'fill': self.fill,
                'backgroundColor': str(Color(255, 99, 132, 0.2)),
                'borderColor': str(Color(255, 99, 132)),
                'pointBackgroundColor': str(Color(255, 99, 132)),
                'pointBorderColor': str(Color(0, 0, 0)),
                'pointHoverBackgroundColor': str(Color('white')),
                'pointHoverBorderColor': str(Color(255, 99, 132)),    
                })
        return json.dumps(result, indent=4)

    def _as_config(self):
        return ('\n'.join([
            "{",
            "  'type': 'radar',",
            "  'data': data,",
            "  'options': {",
            "    'elements': {",
            "      'line': {",
            "        'borderWidth': 3",
            "      }",
            "    }",
            "  },",
            "}"
            ]))

    def as_javascript(self):
        return ('\n'.join([
            '<script>',
            'const data = {self._as_data()};'
            'const config = {self._as_config()};' 
            'var ctx = document.getElementById("Chart");',
            'var chart = new Chart(ctx, config);',
            '</script>',
            ]))
