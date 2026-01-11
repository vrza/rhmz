# rhmz

Show weather reports in your terminal.

![screenshot](https://raw.githubusercontent.com/vrza/rhmz/master/screenshot.png)

- Supports multiple backends, with hundreds of weather stations around the world
- Written in Python 3, clean and flexible codebase
- Easy to add your own custom backend, or a custom frontend / UI

## Installation

- clone this repository
- add a link to `rhmz` to your PATH.

## Synopsis

    rhmz [-h] {hidmet,awc} ...

## Backends

backend | description
---- | ----
`hidmet` | hidmet.gov.rs backend
`awc` | aviationweather.gov METAR backend

`rhmz <backend> -h` shows help for a particular backend

## Which backend should I use?

Try `awc`, it supports thousands of ICAO airport codes.
