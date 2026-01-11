#!/usr/bin/env python3
import zoneinfo
from datetime import datetime
import json
import sys

import requests


EXIT_SUCCESS = 0
EXIT_NETWORK_ERROR = 2
EXIT_BAD_REQUEST = 3


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
        'CAVOK': 'CodeSunny'
    }
    return mapping[cover]


def get_json(stations):
    url = 'https://www.aviationweather.gov/api/data/metar?format=json'
    if stations:
        url += "&ids=" + ",".join(stations)
    response = requests.get(url)
    if response.status_code >= 400:
        print('Could not retrieve data from METAR JSON API (status code %s)' % response.status_code, file=sys.stderr)
        print('> GET %s' % url, file=sys.stderr)
        print(response.text, file=sys.stderr)
        if stations and len(stations) > 1000:
            print('Number of stations requested (%s) might be over the GET request size limit' % len(stations), file=sys.stderr)
        sys.exit(EXIT_BAD_REQUEST)
    return response


def parse_json(content: str) -> list:
    weather = json.loads(content)
    reports = []
    for station in weather:
        print(station)
        report = {'data': []}
        if 'name' in station:
            report['site'] = station['name']
            report['data'].append(('Site', station['name'], ''))
        if 'icaoId' in station:
            report['id'] = station['icaoId']
            report['data'].append(('ICAO code', station['icaoId'], ''))
        if 'obsTime' in station:
            report['data'].append(('Obs. time', unix_timestamp_to_string(station['obsTime']), ''))
        if 'temp' in station:
            report['data'].append(('Temperature', station['temp'], '°C'))
        if 'dewp' in station:
            report['data'].append(('Dew point', station['dewp'], '°C'))
        if 'wspd' in station:
            report['data'].append(('Wind speed', station['wspd'], 'km/h'))
        if 'wdir' in station:
            report['data'].append(('Wind direction', station['wdir'], '°'))
        if 'cover' in station:
            report['condition'] = get_condition_code(station['cover'])
            report['data'].append(('Cloud cover', station['cover'], ''))
        if 'visib' in station:
            report['visibility'] = station['visib']
            report['data'].append(('Visibility', station['visib'], ''))
        # sanity check
        if 'temp' in station:
            reports.append(report)
    return reports


def unix_timestamp_to_string(timestamp: int) -> str:
    local_zone = datetime.now().astimezone().tzinfo
    dt = datetime.fromtimestamp(timestamp, tz=local_zone)
    return dt.strftime('%c %Z')


def filter_reports(all_reports, stations):
    report_set = set(map(lambda x: x['id'], all_reports))
    unavailable_stations = stations.difference(report_set)
    if unavailable_stations:
        print("Some stations you requested are not available via this backend: %s"
              % ",".join(unavailable_stations), file=sys.stderr)
    return list(filter(lambda x: x['id'] in stations, all_reports)) if stations \
        else all_reports


def fetch(stations):
    try:
        response = get_json(stations)
    except Exception:
        print('Call to METAR JSON API failed:', sys.exc_info()[1], file=sys.stderr)
        sys.exit(EXIT_NETWORK_ERROR)

    all_reports = parse_json(response.content)
    reports = filter_reports(all_reports, stations)

    return reports, ''


def print_stations_list():
    reports = parse_json(get_json(stations).content)
    for report in reports:
        print(report['id'] + '\t' + report['site'])


def parse_args(args):
    if args.list:
        print_stations_list()
        sys.exit(EXIT_SUCCESS)
    module_name = vars(sys.modules[__name__])['__name__']
    stations = set(map(lambda x: x.upper(), args.station))
    return module_name, stations
