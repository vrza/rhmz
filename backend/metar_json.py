#!/usr/bin/env python3

import json
import sys

import requests


EXIT_SUCCESS = 0
EXIT_NETWORK_ERROR = 2


def get_condition_code(cover):
    mapping = {
        'CLR': 'CodeSunny',
        'SKC': 'CodeSunny',
        'FEW': 'CodeMostlySunny',
        'SCT': 'CodePartlyCloudy',
        'BKN': 'CodeMostlyCloudy',
        'OVC': 'CodeCloudy',
        'OVX': 'CodeVeryCloudy',
        'FOG': 'CodeFog',
    }
    return mapping[cover]


def get_json():
    url = 'https://www.aviationweather.gov/cgi-bin/json/MetarJSON.php'
    response = requests.get(url)
    return response


def parse_json(content):
    weather = json.loads(content)
    reports = []
    for feature in weather['features']:
        report = {'data': []}
        properties = feature['properties']
        if 'site' in properties:
            report['site'] = properties['site']
            report['data'].append(('Site', properties['site'], ''))
        if 'id' in properties:
            report['id'] = properties['id']
            report['data'].append(('ICAO code', properties['id'], ''))
        if 'obsTime' in properties:
            report['data'].append(('Obs. time', properties['obsTime'], ''))
        if 'temp' in properties:
            report['data'].append(('Temperature', properties['temp'], '°C'))
        if 'dewp' in properties:
            report['data'].append(('Dew point', properties['dewp'], '°C'))
        if 'wspd' in properties:
            report['data'].append(('Wind speed', properties['wspd'], 'km/h'))
        if 'wdir' in properties:
            report['data'].append(('Wind direction', properties['wdir'], '°'))
        if 'cover' in properties:
            report['condition'] = get_condition_code(properties['cover'])
            report['data'].append(('Cloud cover', properties['cover'], ''))
        # sanity check
        if 'temp' in properties:
            reports.append(report)
    return reports


def filter_reports(all_reports, stations):
    station_set = set(map(lambda x: x.upper(), stations))
    report_set = set(map(lambda x: x['id'], all_reports))
    unavailable_stations = station_set.difference(report_set)
    if unavailable_stations:
        print("Some stations you requested are not available via this backend: %s"
              % ",".join(unavailable_stations), file=sys.stderr)
    return list(filter(lambda x: x['id'] in station_set, all_reports)) if stations \
        else all_reports


def fetch(stations):
    try:
        response = get_json()
    except Exception:
        print('Call to METAR JSON API failed:', sys.exc_info()[1], file=sys.stderr)
        sys.exit(EXIT_NETWORK_ERROR)

    all_reports = parse_json(response.content)
    reports = filter_reports(all_reports, stations)

    return reports, ''


def print_stations_list():
    reports = parse_json(get_json().content)
    for report in reports:
        print(report['id'] + '\t' + report['site'])


def parse_args(args):
    if args.list:
        print_stations_list()
        sys.exit(EXIT_SUCCESS)
    module_name = vars(sys.modules[__name__])['__name__']
    return module_name, args.station
