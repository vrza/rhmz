# rhmz

A weather report in your terminal.

![screenshot](https://raw.githubusercontent.com/vrza/rhmz/master/screenshot.png)

## Synopsis

    rhmz [-h] {hidmet,metar_xml,metar_json} ...

## Backends

backend | description
---- | ----
`hidmet` | hidmet.gov.rs backend
`metar_xml` | aviationweather.gov METAR XML backend, supports thousands of sites
`metar_json` | aviationweather.gov METAR JSON backend

`rhmz <backend> -h` shows help for a particular backend
