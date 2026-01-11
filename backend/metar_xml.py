#!/usr/bin/env python3

import sys

import lxml.etree
import requests


EXIT_SUCCESS = 0
EXIT_NETWORK_ERROR = 2
EXIT_BAD_REQUEST = 3


def get_condition_code(cover):
    mapping = {
        'CLR': 'CodeSunny',
        'SKC': 'CodeSunny',
        'CAVOK': 'CodeSunny',
        'FEW': 'CodeMostlySunny',
        'SCT': 'CodePartlyCloudy',
        'BKN': 'CodeMostlyCloudy',
        'OVC': 'CodeCloudy',
        'OVX': 'CodeVeryCloudy',
        'FOG': 'CodeFog',
    }
    return mapping[cover]


def get_xml(stations):
    url = 'https://www.aviationweather.gov/adds/dataserver_current/httpparam?datasource=metars&requestType=retrieve&format=xml&mostRecentForEachStation=constraint&hoursBeforeNow=2'
    if stations:
        url += '&stationString=' + ','.join(stations)
    response = requests.get(url)
    if response.status_code >= 400:
        print('Could not retrieve data from METAR XML API (status code %s)' % response.status_code, file=sys.stderr)
        print('> GET %s' % url, file=sys.stderr)
        print(response.text, file=sys.stderr)
        if stations and len(stations) > 1000:
            print('Number of stations requested (%s) might be over the GET request size limit' % len(stations),
                  file=sys.stderr)
        sys.exit(EXIT_BAD_REQUEST)
    return response


def parse_xml(content):
    tree = lxml.etree.XML(content)
    reports = []
    for element in tree.xpath('//METAR'):
        report = {'data': []}
        station_id = element.xpath('.//station_id//text()')
        if station_id:
            report['id'] = station_id[0]
            report['data'].append(('ICAO code', station_id[0], ''))
        observation_time = element.xpath('.//observation_time//text()')
        if observation_time:
            report['data'].append(('Obs. time', observation_time[0], ''))
        temp_c = element.xpath('.//temp_c//text()')
        if temp_c:
            report['data'].append(('Temperature', temp_c[0], '°C'))
        dewpoint_c = element.xpath('.//dewpoint_c//text()')
        if dewpoint_c:
            report['data'].append(('Dew point', dewpoint_c[0], '°C'))
        wind_dir_degrees = element.xpath('.//wind_dir_degrees//text()')
        if wind_dir_degrees:
            report['data'].append(('Wind dir.', wind_dir_degrees[0], '°'))
        wind_speed_kt = element.xpath('.//wind_speed_kt//text()')
        if wind_speed_kt:
            report['data'].append(('Wind speed', wind_speed_kt[0], 'kn'))
        sky_condition = element.xpath('.//sky_condition[1]')
        if sky_condition:
            sky_cover = sky_condition[0].xpath('.//@sky_cover')
            if sky_cover:
                cover = sky_cover[0]
                report['condition'] = get_condition_code(cover)
                cloud_base_ft_agl = sky_condition[0].xpath('.//@cloud_base_ft_agl')
                if cloud_base_ft_agl:
                    cover += ' at %s ft' % cloud_base_ft_agl[0]
                report['data'].append(('Sky cover', cover, ''))
        reports.append(report)
    return reports


def fetch(stations):
    try:
        response = get_xml(stations)
    except Exception:
        print('Call to METAR XML API failed:', sys.exc_info()[1], file=sys.stderr)
        sys.exit(EXIT_NETWORK_ERROR)

    reports = parse_xml(response.content)

    return reports, ''


def print_stations_list():
    reports = parse_xml(get_xml([]).content)
    idents = set(map(lambda x: x['id'], reports))
    for ident in idents:
        print(ident)


def parse_args(args):
    if args.list:
        print_stations_list()
        sys.exit(EXIT_SUCCESS)
    module_name = vars(sys.modules[__name__])['__name__']
    stations = set(map(lambda x: x.upper(), args.station))
    return module_name, stations
