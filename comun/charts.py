#!/usr/bin/env python3

import json
from django.db.models import Count
# from django.views.decorators.cache import cache_page
from django.shortcuts import render


DEFAULT_COLORS = [
    '#003f5c',
    '#2f4b7c',
    '#665191',
    '#a05195',
    '#d45087',
    '#f95d6a',
    '#ff7c43',
    '#ffa600',
    ]

class BarChart:

    def __init__(self):
        self.set_index = 0
        self.datasets = [{'data' : []}]
        self.labels = list()
        self.colors = list()
        self.options = {
            'responsive': True,
            'maintainAspectRatio': False,
            'animation': {
                'duration': 1500,
                'easing': 'easeOutQuart',
                'loop': False,
                },
            'plugins': {
                'legend': False,
                'title': {
                    'display': True,
                    'text': 'Sistemas de información identificados por ente',
                    },
                }    
            }

    def add_value(self, value, label='', color=''):
        self.datasets[self.set_index]['data'].append(value)
        self.labels.append(label if label else str(value))
        self.datasets[self.set_index].setdefault('backgroundColor', list()).append(
            color if color else DEFAULT_COLORS[self.set_index]
            )

    def as_json(self):
        result = {
            'type': 'bar',
            'options': self.options,
            'data': {
                'datasets': self.datasets,
                },
            }
        if self.labels:
            result['data']['labels'] = self.labels
        if self.colors:
            result['data']['backgroundColors'] = self.colors
        return json.dumps(result, indent=4)
    

def main():
    result = BarChart()
    result.add_value(37, 'rojo', '#F23A20')
    result.add_value(137, 'verde', '#3AF220')
    result.add_value(37, 'verde', '#3F22FA')
    print(result.as_json())


def lab(request):
    return render(request, 'comun/lab.html', {
        'titulo': 'Charts labs',
        })


# @cache_page(60 * 15)
def organismos(request):
    import pygal
    from sistemas.models import Sistema
    from django.http import HttpResponse

    style = pygal.style.Style(
        transition='1400ms ease-in',
        colors=['#323298', '#ffebcd', '#daa520', '#9BC850', '#ffeb44', '#ff00ff'],
        )
    config = pygal.Config()
    config.show_legend = True
    config.x_label_rotation=-90
    config.human_readable = True
    config.fill = True
    config.show_y_guides = False
    config.width = 620
    config.height = 200
    chart = pygal.Bar(config, style=style)
    chart.title = 'Sistemas por organismo estudiado'
    qs = (
        Sistema.objects
        .values('ente')
        .annotate(num_sistemas=Count('pk'))
        )
    labels = []
    values = []
    for item in qs.all():
        label = item['ente']
        value = item['num_sistemas']
        labels.append(label)
        values.append(value)
    chart.add('N. sistemas', values)
    chart.x_labels = labels
    chart.show_legend = False
    return HttpResponse(
        chart.render(),
        content_type='image/svg+xml',
        )



if __name__ == "__main__":
    main()
