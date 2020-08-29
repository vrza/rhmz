#!/usr/bin/env python3

import json
import requests


HEADER = 'METAR'


def get_condition_code(cover):
    mapping = {
        'CLR': 'CodeSunny',
        'SKC': 'CodeSunny',
        'FEW': 'CodeMostlySunny',
        'SCT': 'CodePartlyCloudy',
        'BKN': 'CodeMostlyCloudy',
        'OVC': 'CodeCloudy',
        'FOG': 'CodeFog',
    }
    return mapping[cover]


def get_json():
    url = 'https://www.aviationweather.gov//cgi-bin/json/MetarJSON.php'
    response = requests.get(url)
    return response


def parse_json(content):
    weather = json.loads(content)
    reports = []
    for feature in weather['features']:
        report = {'data': []}
        properties = feature['properties']
        if 'cover' in properties:
            report['condition'] = get_condition_code(properties['cover'])
        if 'site' in properties:
            site = ('Site', properties['site'], '')
            report['data'].append(site)
        if 'id' in properties:
            ident = ('IATA id', properties['id'], '')
            report['data'].append(ident)
        if 'obsTime' in properties:
            ident = ('Obs. time', properties['obsTime'], '')
            report['data'].append(ident)
        if 'temp' in properties:
            temp = ('Temperature', properties['temp'], '°C')
            report['data'].append(temp)
        if 'dewp' in properties:
            dewp = ('Dew point', properties['dewp'], '°C')
            report['data'].append(dewp)
        if 'wspd' in properties:
            wspd = ('Wind speed', properties['wspd'], 'km/h')
            report['data'].append(wspd)
        if 'wdir' in properties:
            wdir = ('Wind direction', properties['wdir'], '°')
            report['data'].append(wdir)
        # sanity check
        if 'temp' in properties:
            reports.append(report)
    return reports


def parse_args(_args):
    return 'metar', []
