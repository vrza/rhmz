import math
import os

import wcwidth
from frontend.lib.tabulate.tabulate import tabulate


ART_BOX_WIDTH = 15
MAX_ART_HEIGHT = 5


def get_ascii_art_cond(code):
    codes = {
        'CodeUnknown': [
            "    .-.      ",
            "     __)     ",
            "    (        ",
            "     `-᾿     ",
            "      •      ",
        ],
        'CodeCloudy': [
            "             ",
            "\033[38;5;250m     .--.    \033[0m",
            "\033[38;5;250m  .-(    ).  \033[0m",
            "\033[38;5;250m (___.__)__) \033[0m",
            "             ",
        ],
        'CodeFog': [
            "             ",
            "\033[38;5;251m _ - _ - _ - \033[0m",
            "\033[38;5;251m  _ - _ - _  \033[0m",
            "\033[38;5;251m _ - _ - _ - \033[0m",
            "             ",
        ],
        'CodeHeavyRain': [
            "\033[38;5;240;1m     .-.     \033[0m",
            "\033[38;5;240;1m    (   ).   \033[0m",
            "\033[38;5;240;1m   (___(__)  \033[0m",
            "\033[38;5;21;1m  ‚ʻ‚ʻ‚ʻ‚ʻ   \033[0m",
            "\033[38;5;21;1m  ‚ʻ‚ʻ‚ʻ‚ʻ   \033[0m",
        ],
        'CodeHeavyShowers': [
            "\033[38;5;226m _`/\"\"\033[38;5;240;1m.-.    \033[0m",
            "\033[38;5;226m  ,\\_\033[38;5;240;1m(   ).  \033[0m",
            "\033[38;5;226m   /\033[38;5;240;1m(___(__) \033[0m",
            "\033[38;5;21;1m   ‚ʻ‚ʻ‚ʻ‚ʻ  \033[0m",
            "\033[38;5;21;1m   ‚ʻ‚ʻ‚ʻ‚ʻ  \033[0m",
        ],
        'CodeHeavySnow': [
            "\033[38;5;240;1m     .-.     \033[0m",
            "\033[38;5;240;1m    (   ).   \033[0m",
            "\033[38;5;240;1m   (___(__)  \033[0m",
            "\033[38;5;255;1m   * * * *   \033[0m",
            "\033[38;5;255;1m  * * * *    \033[0m",
        ],
        'CodeHeavySnowShowers': [
            "\033[38;5;226m _`/\"\"\033[38;5;240;1m.-.    \033[0m",
            "\033[38;5;226m  ,\\_\033[38;5;240;1m(   ).  \033[0m",
            "\033[38;5;226m   /\033[38;5;240;1m(___(__) \033[0m",
            "\033[38;5;255;1m    * * * *  \033[0m",
            "\033[38;5;255;1m   * * * *   \033[0m",
        ],
        'CodeLightRain': [
            "\033[38;5;250m     .-.     \033[0m",
            "\033[38;5;250m    (   ).   \033[0m",
            "\033[38;5;250m   (___(__)  \033[0m",
            "\033[38;5;111m    ʻ ʻ ʻ ʻ  \033[0m",
            "\033[38;5;111m   ʻ ʻ ʻ ʻ   \033[0m",
        ],
        'CodeLightShowers': [
            "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
            "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
            "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
            "\033[38;5;111m     ʻ ʻ ʻ ʻ \033[0m",
            "\033[38;5;111m    ʻ ʻ ʻ ʻ  \033[0m",
        ],
        'CodeLightSleet': [
            "\033[38;5;250m     .-.     \033[0m",
            "\033[38;5;250m    (   ).   \033[0m",
            "\033[38;5;250m   (___(__)  \033[0m",
            "\033[38;5;111m    ʻ \033[38;5;255m*\033[38;5;111m ʻ \033[38;5;255m*  \033[0m",
            "\033[38;5;255m   *\033[38;5;111m ʻ \033[38;5;255m*\033[38;5;111m ʻ   \033[0m",
        ],
        'CodeLightSleetShowers': [
            "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
            "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
            "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
            "\033[38;5;111m     ʻ \033[38;5;255m*\033[38;5;111m ʻ \033[38;5;255m* \033[0m",
            "\033[38;5;255m    *\033[38;5;111m ʻ \033[38;5;255m*\033[38;5;111m ʻ  \033[0m",
        ],
        'CodeLightSnow': [
            "\033[38;5;250m     .-.     \033[0m",
            "\033[38;5;250m    (   ).   \033[0m",
            "\033[38;5;250m   (___(__)  \033[0m",
            "\033[38;5;255m    *  *  *  \033[0m",
            "\033[38;5;255m   *  *  *   \033[0m",
        ],
        'CodeLightSnowShowers': [
            "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
            "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
            "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
            "\033[38;5;255m     *  *  * \033[0m",
            "\033[38;5;255m    *  *  *  \033[0m",
        ],
        'CodeMostlyCloudy': [
            "\033[38;5;226m   \\  /\033[0m      ",
            "\033[38;5;226m _ /\"\033[38;5;250m.--.    \033[0m",
            "\033[38;5;226m   \\\033[38;5;250m(    ).  \033[0m",
            "\033[38;5;250m   (__._(__) \033[0m",
            "             ",
        ],
        'CodeMostlySunny': [
            "\033[38;5;226m    \\   /    \033[0m",
            "\033[38;5;226m     .-.     \033[0m",
            "\033[38;5;226m  ‒ (   ) ‒  \033[0m",
            "\033[38;5;226m     `-᾿\033[0m.",
            "\033[38;5;226m    / \033[0m (_)",
        ],
        'CodePartlyCloudy': [
            "\033[38;5;226m   \\  /\033[0m      ",
            "\033[38;5;226m _ /\"\"\033[38;5;250m.-.    \033[0m",
            "\033[38;5;226m   \\_\033[38;5;250m(   ).  \033[0m",
            "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
            "             ",
        ],
        'CodeSunny': [
            "\033[38;5;226m    \\   /    \033[0m",
            "\033[38;5;226m     .-.     \033[0m",
            "\033[38;5;226m  ‒ (   ) ‒  \033[0m",
            "\033[38;5;226m     `-᾿     \033[0m",
            "\033[38;5;226m    /   \\    \033[0m",
        ],
        'CodeThunderyHeavyRain': [
            "\033[38;5;240;1m     .-.     \033[0m",
            "\033[38;5;240;1m    (   ).   \033[0m",
            "\033[38;5;240;1m   (___(__)  \033[0m",
            "\033[38;5;21;1m  ‚ʻ\033[38;5;228;5m⚡\033[38;5;21;25mʻ‚\033[38;5;228;5m⚡\033[38;5;21;25m‚ʻ   \033[0m",
            "\033[38;5;21;1m  ‚ʻ‚ʻ\033[38;5;228;5m⚡\033[38;5;21;25mʻ‚ʻ   \033[0m",
        ],
        'CodeThunderyShowers': [
            "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
            "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
            "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
            "\033[38;5;228;5m    ⚡\033[38;5;111;25mʻ ʻ\033[38;5;228;5m⚡\033[38;5;111;25mʻ ʻ \033[0m",
            "\033[38;5;111m    ʻ ʻ ʻ ʻ  \033[0m",
        ],
        'CodeThunderySnowShowers': [
            "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
            "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
            "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
            "\033[38;5;255m     *\033[38;5;228;5m⚡\033[38;5;255;25m *\033[38;5;228;5m⚡\033[38;5;255;25m * \033[0m",
            "\033[38;5;255m    *  *  *  \033[0m",
        ],
        'CodeVeryCloudy': [
            "             ",
            "\033[38;5;240;1m     .--.    \033[0m",
            "\033[38;5;240;1m  .-(    ).  \033[0m",
            "\033[38;5;240;1m (___.__)__) \033[0m",
            "             ",
        ]
    }
    return codes[code]


def vertical_pad_art(art, height):
    diff = height - len(art)
    if diff < 0:
        return art[0:height]
    top_pad = math.floor(diff / 2)
    bottom_pad = math.ceil(diff / 2)
    return ['']*top_pad + art + ['']*bottom_pad


def get_art_for_data(weather_data):
    cond_code = weather_data['condition'] if 'condition' in weather_data else 'CodeUnknown'
    return get_ascii_art_cond(cond_code)


def render_table(weather_data, height_pad, label_pad, value_pad):
    unpadded_art = get_art_for_data(weather_data)
    ascii_art = vertical_pad_art(unpadded_art, height_pad)
    tbl = []
    for i in range(height_pad):
        ascii_art_row = ascii_art[i].ljust(ART_BOX_WIDTH)
        if i < len(weather_data['data']):
            label, value, unit = weather_data['data'][i]
            value_row = f'{value} {unit}'.ljust(value_pad)
            label_row = label.ljust(label_pad)
        else:
            value_row = label_row = ''
        tbl.append([ascii_art_row, label_row, value_row])
    table = tabulate(tbl, tablefmt='fancy_outline', preserve_whitespace=True)
    return table.splitlines()


def terminal_size():
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(rows), int(columns)


def table_padding(reports):
    max_label_width = 0
    max_value_width = 0
    max_height = MAX_ART_HEIGHT
    for report in reports:
        data = report['data']
        if len(data) > max_height:
            max_height = len(data)
        for item in data:
            label, value, unit = item
            label_width = wcwidth.wcswidth(label)
            if label_width > max_label_width:
                max_label_width = label_width
            value_width = wcwidth.wcswidth(f'{value} {unit}')
            if value_width > max_value_width:
                max_value_width = value_width

    return max_height, max_label_width, max_value_width


def render_tables(reports):
    height_pad, label_pad, value_pad = table_padding(reports)
    return list(map(lambda x: render_table(x, height_pad, label_pad, value_pad), reports))


def max_table_width(tables):
    max_width = 0
    for table in tables:
        if table:
            line = table[0]
            if wcwidth.wcswidth(line) > max_width:
                max_width = wcwidth.wcswidth(line)
    return max_width


def cells_in_row(total_cells, cells_per_row, row):
    num_rows = math.ceil(total_cells / cells_per_row)
    cells_in_last_row = total_cells - cells_per_row * (num_rows - 1)
    return cells_per_row if row < num_rows - 1 else cells_in_last_row


def output_tables(tables):
    width_of_table = max_table_width(tables)
    if width_of_table == 0:
        return
    _, terminal_columns = terminal_size()
    num_tables = len(tables)
    tables_per_row = math.floor(terminal_columns / width_of_table)
    num_rows = math.ceil(num_tables / tables_per_row)
    lines_per_table = len(tables[0])
    for row_index in range(num_rows):
        for line_index in range(lines_per_table):
            for cell_offset in range(cells_in_row(num_tables, tables_per_row, row_index)):
                table_index = row_index * tables_per_row + cell_offset
                print(tables[table_index][line_index], end='')
            print()


def render_and_output(reports, header):
    tables = render_tables(reports)
    if header:
        print(header)
    output_tables(tables)
