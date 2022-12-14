import math

def num_to_rgb(val, max_val=1):
    i = (val * 255 / max_val);
    r = round(math.sin(0.024 * i + 0) * 127 + 128);
    g = round(math.sin(0.024 * i + 2) * 127 + 128);
    b = round(math.sin(0.024 * i + 4) * 127 + 128);
    return (r,g,b)


color_map = {
    'red': '#ECECEC',
    'orange':'#CDE0FF',
    'yellow':'#AAC3F3',
    'pale-green':'#6192F3',
    'green':'#4982F3'
}

def number_2_color(num):
    if num < 0.2:
        return color_map['red']
    if num < 0.4:
        return color_map['orange']
    if num < 0.6:
        return color_map['yellow']
    if num < 0.8:
        return color_map['pale-green']
    return color_map['green']