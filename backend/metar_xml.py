#!/usr/bin/env python3

import json
import sys

import lxml.etree
import requests


MODULE_NAME = 'metar_xml'

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
    ids = set(map(lambda x: x.upper(), stations))
    url = 'https://www.aviationweather.gov/adds/dataserver_current/httpparam?datasource=metars&requestType=retrieve&format=xml&mostRecentForEachStation=constraint&hoursBeforeNow=2'
    if ids:
        url += '&stationString=' + ','.join(ids)
    response = requests.get(url)
    if response.status_code == 400:
        print('Could not retrieve data from METAR XML API (400 Bad request)', file=sys.stderr)
        print('> GET %s' % url, file=sys.stderr)
        print(response.text, file=sys.stderr)
        if ids and len(ids) > 1000:
            print('Number of stations requested (%s) might be over the GET request size limit' % len(ids), file=sys.stderr)
        exit(EXIT_BAD_REQUEST)
    return response


def parse_xml(content):
    tree = lxml.etree.XML(content)
    reports = []
    for element in tree.xpath('//METAR'):
        report = {'data': []}
        station_id = element.xpath('.//station_id//text()')
        if station_id:
            report['id'] = station_id[0]
            ident = ('Station', station_id[0], '')
            report['data'].append(ident)
        observation_time = element.xpath('.//observation_time//text()')
        if observation_time:
            obs_time = ('Obs. time', observation_time[0], '')
            report['data'].append(obs_time)
        temp_c = element.xpath('.//temp_c//text()')
        if temp_c:
            temp = ('Temperature', temp_c[0], '°C')
            report['data'].append(temp)
        dewpoint_c = element.xpath('.//dewpoint_c//text()')
        if dewpoint_c:
            dewpoint = ('Dew point', dewpoint_c[0], '°C')
            report['data'].append(dewpoint)
        wind_dir_degrees = element.xpath('.//wind_dir_degrees//text()')
        if wind_dir_degrees:
            wind_dir = ('Wind direction', wind_dir_degrees[0], '°')
            report['data'].append(wind_dir)
        wind_speed_kt = element.xpath('.//wind_speed_kt//text()')
        if wind_speed_kt:
            wind_speed = ('Wind speed', wind_speed_kt[0], 'kn')
            report['data'].append(wind_speed)
        sky_condition = element.xpath('.//sky_condition[1]')
        if sky_condition:
            sky_cover = sky_condition[0].xpath('.//@sky_cover')
            if sky_cover:
                cover = sky_cover[0]
                report['condition'] = get_condition_code(cover)
                cloud_base_ft_agl = sky_condition[0].xpath('.//@cloud_base_ft_agl')
                if cloud_base_ft_agl:
                    cover += ' at %s ft' % cloud_base_ft_agl[0]
                condition = ('Sky cover', cover, '')
                report['data'].append(condition)
        reports.append(report)
    return reports


def fetch(stations):
    try:
        response = get_xml(stations)
    except Exception:
        print("Failed to call METAR XML API:", sys.exc_info()[1], file=sys.stderr)
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
    stations = [] if args.all else args.station
    return MODULE_NAME, stations
