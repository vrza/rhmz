#!/usr/bin/env python3

import json
import sys

import requests


MODULE_NAME = 'metar_json'

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
    #print(response.text)
    return response


def parse_json(content):
    weather = json.loads(content)
    reports = []
    for feature in weather['features']:
        report = {'data': []}
        properties = feature['properties']
        if 'site' in properties:
            report['site'] = properties['site']
            site = ('Site', properties['site'], '')
            report['data'].append(site)
        if 'id' in properties:
            report['id'] = properties['id']
            ident = ('IATA id', properties['id'], '')
            report['data'].append(ident)
        if 'obsTime' in properties:
            obs_time = ('Obs. time', properties['obsTime'], '')
            report['data'].append(obs_time)
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
        if 'cover' in properties:
            report['condition'] = get_condition_code(properties['cover'])
            condition = ('Cloud cover', properties['cover'], '')
            report['data'].append(condition)
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
    return MODULE_NAME, args.station
