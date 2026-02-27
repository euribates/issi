#!/usr/bin/env python3

import re


pat_color = re.compile(
    r'#([0-9A-F]{2})([0-9A-F]{2})([0-9A-F]{2})',
    re.IGNORECASE,
    )

pat_color_alpha = re.compile(
    r'#([0-9A-F]{2})([0-9A-F]{2})([0-9A-F]{2})([0-9A-F]{2})',
    re.IGNORECASE,
    )

NAMED_COLORS = {
    'aliceblue': (240, 248, 255),
    'antiquewhite': (250, 235, 215),
    'aqua': (0, 255, 255),
    'aquamarine': (127, 255, 212),
    'azure': (240, 255, 255),
    'beige': (245, 245, 220),
    'bisque': (255, 228, 196),
    'black': (0, 0, 0),
    'blanchedalmond': (255, 235, 205),
    'blue': (0, 0, 255),
    'blueviolet': (138, 43, 226),
    'brown': (165, 42, 42),
    'burlywood': (222, 184, 135),
    'cadetblue': (95, 158, 160),
    'chartreuse': (127, 255, 0),
    'chocolate': (210, 105, 30),
    'coral': (255, 127, 80),
    'cornflowerblue': (100, 149, 237),
    'cornsilk': (255, 248, 220),
    'crimson': (220, 20, 60),
    'cyan': (0, 255, 255),
    'darkblue': (0, 0, 139),
    'darkcyan': (0, 139, 139),
    'darkgoldenrod': (184, 134, 11),
    'darkgray': (169, 169, 169),
    'darkgrey': (169, 169, 169),
    'darkgreen': (0, 100, 0),
    'darkkhaki': (189, 183, 107),
    'darkmagenta': (139, 0, 139),
    'darkolivegreen': (85, 107, 47),
    'darkorange': (255, 140, 0),
    'darkorchid': (153, 50, 204),
    'darkred': (139, 0, 0),
    'darksalmon': (233, 150, 122),
    'darkseagreen': (143, 188, 143),
    'darkslateblue': (72, 61, 139),
    'darkslategray': (47, 79, 79),
    'darkslategrey': (47, 79, 79),
    'darkturquoise': (0, 206, 209),
    'darkviolet': (148, 0, 211),
    'deeppink': (255, 20, 147),
    'deepskyblue': (0, 191, 255),
    'dimgray': (105, 105, 105),
    'dimgrey': (105, 105, 105),
    'dodgerblue': (30, 144, 255),
    'firebrick': (178, 34, 34),
    'floralwhite': (255, 250, 240),
    'forestgreen': (34, 139, 34),
    'fuchsia': (255, 0, 255),
    'gainsboro': (220, 220, 220),
    'ghostwhite': (248, 248, 255),
    'gold': (255, 215, 0),
    'goldenrod': (218, 165, 32),
    'gray': (128, 128, 128),
    'grey': (128, 128, 128),
    'green': (0, 128, 0),
    'greenyellow': (173, 255, 47),
    'honeydew': (240, 255, 240),
    'hotpink': (255, 105, 180),
    'indianred': (205, 92, 92),
    'indigo': (75, 0, 130),
    'ivory': (255, 255, 240),
    'khaki': (240, 230, 140),
    'lavender': (230, 230, 250),
    'lavenderblush': (255, 240, 245),
    'lawngreen': (124, 252, 0),
    'lemonchiffon': (255, 250, 205),
    'lightblue': (173, 216, 230),
    'lightcoral': (240, 128, 128),
    'lightcyan': (224, 255, 255),
    'lightgoldenrodyellow': (250, 250, 210),
    'lightgray': (211, 211, 211),
    'lightgreen': (144, 238, 144),
    'lightpink': (255, 182, 193),
    'lightsalmon': (255, 160, 122),
    'lightseagreen': (32, 178, 170),
    'lightskyblue': (135, 206, 250),
    'lightslategray': (119, 136, 153),
    'lightslategrey': (119, 136, 153),
    'lightsteelblue': (176, 196, 222),
    'lightyellow': (255, 255, 224),
    'lime': (0, 255, 0),
    'limegreen': (50, 205, 50),
    'linen': (250, 240, 230),
    'magenta': (255, 0, 255),
    'maroon': (128, 0, 0),
    'mediumaquamarine': (102, 205, 170),
    'mediumblue': (0, 0, 205),
    'mediumorchid': (186, 85, 211),
    'mediumpurple': (147, 112, 219),
    'mediumseagreen': (60, 179, 113),
    'mediumslateblue': (123, 104, 238),
    'mediumspringgreen': (0, 250, 154),
    'mediumturquoise': (72, 209, 204),
    'mediumvioletred': (199, 21, 133),
    'midnightblue': (25, 25, 112),
    'mintcream': (245, 255, 250),
    'mistyrose': (255, 228, 225),
    'moccasin': (255, 228, 181),
    'navajowhite': (255, 222, 173),
    'navy': (0, 0, 128),
    'oldlace': (253, 245, 230),
    'olive': (128, 128, 0),
    'olivedrab': (107, 142, 35),
    'orange': (255, 165, 0),
    'orangered': (255, 69, 0),
    'orchid': (218, 112, 214),
    'palegoldenrod': (238, 232, 170),
    'palegreen': (152, 251, 152),
    'paleturquoise': (175, 238, 238),
    'palevioletred': (219, 112, 147),
    'papayawhip': (255, 239, 213),
    'peachpuff': (255, 218, 185),
    'peru': (205, 133, 63),
    'pink': (255, 192, 203),
    'plum': (221, 160, 221),
    'powderblue': (176, 224, 230),
    'purple': (128, 0, 128),
    'red': (255, 0, 0),
    'rosybrown': (188, 143, 143),
    'royalblue': (65, 105, 225),
    'saddlebrown': (139, 69, 19),
    'salmon': (250, 128, 114),
    'sandybrown': (244, 164, 96),
    'seagreen': (46, 139, 87),
    'seashell': (255, 245, 238),
    'sienna': (160, 82, 45),
    'silver': (192, 192, 192),
    'skyblue': (135, 206, 235),
    'slateblue': (106, 90, 205),
    'slategray': (112, 128, 144),
    'slategrey': (112, 128, 144),
    'snow': (255, 250, 250),
    'springgreen': (0, 255, 127),
    'steelblue': (70, 130, 180),
    'tan': (210, 180, 140),
    'teal': (0, 128, 128),
    'thistle': (216, 191, 216),
    'tomato': (255, 99, 71),
    'turquoise': (64, 224, 208),
    'violet': (238, 130, 238),
    'wheat': (245, 222, 179),
    'white': (255, 255, 255),
    'whitesmoke': (245, 245, 245),
    'yellow': (255, 255, 0),
    'yellowgreen': (154, 205, 50),
    }


class Color:

    def __init__(self, *args, **kwargs):
        if len(args) == 3:
            self.red = args[0]
            self.green = args[1]
            self.blue = args[2]
            self.alpha = None
        elif len(args) == 4:
            self.red = args[0]
            self.green = args[1]
            self.blue = args[2]
            self.alpha = args[3]
        elif len(kwargs) == 3:
            self.red = kwargs['red']
            self.green = kwargs['green']
            self.blue = kwargs['blue']
            self.alpha = None
        elif len(kwargs) == 4:
            self.red = kwargs['red']
            self.green = kwargs['green']
            self.blue = kwargs['blue']
            self.alpha = kwargs['alpha']
        elif len(args) == 1:
            name_or_code = args[0].lower()
            if name_or_code in NAMED_COLORS:
                self.red, self.green, self.blue = NAMED_COLORS[name_or_code]
                self.alpha = None
            elif _match := pat_color_alpha.match(name_or_code):
                self.red = int(_match.group(1), 16)
                self.green = int(_match.group(2), 16)
                self.blue = int(_match.group(3), 16)
                self.alpha = int(_match.group(4), 16)
            elif _match := pat_color.match(name_or_code):
                self.red = int(_match.group(1), 16)
                self.green = int(_match.group(2), 16)
                self.blue = int(_match.group(3), 16)
                self.alpha = None

    def __str__(self):
        if self.alpha is None:
            return f'#{self.red:02x}{self.green:02x}{self.blue:02x}'.upper()
        return (
            f'#{self.red:02x}'
            f'{self.green:02x}'
            f'{self.blue:02x}'
            f'{self.alpha:02x}'
            f'').upper()


    def to_hsl(self):
        _red = self.red / 255.0
        _green = self.green / 255.0
        _blue = self.blue / 255.0

        c_max = max(_red, _green, _blue)
        c_min = min(_red, _green, _blue)
        delta = c_max - c_min
        lightness = round((c_max + c_min) / 2.0, 2)
        if delta == 0.0:
            hue = 0.0
            saturation = 0.0
            return (hue, saturation, lightness * 100.0)
        if c_max == _red:
            hue = round(60.0 * (((_green - _blue) / delta) % 6), 2)
        elif c_max == _green:
            hue = round(60.0 * (((_blue - _red) / delta) + 2), 2)
        elif c_max == _blue:
            hue = round(60.0 * (((_red - _green) / delta) + 4), 2)
        saturation = round((delta * 100.0)/ (1 - abs(2 * lightness - 1.0)), 2)
        return (hue, saturation, lightness * 100.0)

BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)
