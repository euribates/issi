#!/usr/bin/env python3

import json


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
            'amimation': True,
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
            'data': {
                'datasets': self.datasets,
                }
            }
        if self.labels:
            result['data']['labels'] = self.labels
        if self.colors:
            result['data']['backgroundColors'] = self.colors
        return json.dumps(result)
    

def main():
    result = BarChart()
    result.add_value(37, 'rojo', '#F23A20')
    result.add_value(137, 'verde', '#3AF220')
    result.add_value(37, 'verde', '#3F22FA')
    print(result.as_json())


if __name__ == "__main__":
    main()
