import math
import os

import prettytable


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


def render_table(weather_data, label_pad, value_pad):
    # prepare table
    tbl = prettytable.PrettyTable()
    tbl.field_names = ['ascii', 'name', 'value']
    tbl.header = False
    tbl.align['ascii'] = 'l'
    tbl.align['name'] = 'l'
    tbl.align['value'] = 'l'
    # fill table
    ascii_art = [''] + get_ascii_art_cond(weather_data['condition'])
    for i in range(len(weather_data['data'])):
        label, value, unit = weather_data['data'][i]
        ascii_art_row = ascii_art[i] if i < len(ascii_art) else ''
        value_row = f'{value} {unit}'.ljust(value_pad)
        label_row = label.ljust(label_pad)
        tbl.add_row([ascii_art_row, label_row, value_row])
    return tbl.get_string().splitlines()


def terminal_size():
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(rows), int(columns)


def max_table_column_widths(reports):
    max_label_width = 0
    max_value_width = 0
    for report in reports:
        for item in report['data']:
            label, value, unit = item
            label_width = len(label)
            if label_width > max_label_width:
                max_label_width = label_width
            value_width = len(f'{value} {unit}')
            if value_width > max_value_width:
                max_value_width = value_width
    return max_label_width, max_value_width


def render_tables(reports):
    label_pad, value_pad = max_table_column_widths(reports)
    return list(map(lambda x: render_table(x, label_pad, value_pad), reports))


def max_table_width(tables):
    max_width = 0
    for table in tables:
        line = table[0]
        if len(line) > max_width:
            max_width = len(line)
    return max_width


def output_tables(tables):
    if len(tables) == 0 or max_table_width(tables) == 0:
        return
    _, term_columns = terminal_size()
    tables_per_row = math.floor(term_columns / max_table_width(tables))
    num_rows = math.ceil(len(tables) / tables_per_row)
    lines_per_table = len(tables[0])
    for row_index in range(num_rows):
        for line_index in range(lines_per_table):
            for cell_offset in range(tables_per_row):
                table_index = row_index * tables_per_row + cell_offset
                if table_index < len(tables):
                    print(tables[table_index][line_index], end='')
            print()
