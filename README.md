[![PyPI](https://img.shields.io/pypi/v/ambient_aprs.svg?maxAge=2592000)](https://pypi.python.org/pypi/ambient_aprs) 
[![Build Status](https://travis-ci.org/avryhof/ambient_aprs.svg?branch=master)](https://travis-ci.org/avryhof/ambient_aprs) 
[![codecov](https://codecov.io/gh/avryhof/ambient_aprs/branch/master/graph/badge.svg)](https://codecov.io/gh/avryhof/ambient_aprs)
<a href="https://www.codefactor.io/repository/github/avryhof/ambient_aprs"><img alt="CodeFactor" src=
   "https://www.codefactor.io/repository/github/avryhof/ambient_aprs/badge"/></a>

# ambient_aprs
Wrapper for ambient_api to allow sending APRS packets to CWOP

## Installation

```bash
pip install ambient_aprs
```

##### Environmental Variables
```bash
AMBIENT_ENDPOINT=https://api.ambientweather.net/v1
AMBIENT_API_KEY='your-api-key-here'
AMBIENT_APPLICATION_KEY='your-application-key-here'
```
Get these values by following [these instructions](https://ambientweather.docs.apiary.io/#introduction/authentication).

## Classes
There is one class implemented in this module.

##### AmbientAPRS
This is the base Class that you initialize in your code.

```python
from ambient_aprs.ambient_aprs import AmbientAPRS

aprs = AmbientAPRS(
    station_id='<your-station-id>',
    latitude=43.131258,
    longitude=-76.155028
)

aprs.get_weather_data()
aprs.build_packet()
result = aprs.send_packet()
``` 

You can also initialize the Class with the following keyword arguments
* send_id - In case you want your software to identify itself as something other than "Ambient APRS"
* host - The server you want to send your APRS packet to. (default is cwop.aprs.net)
* port - The port you want to send your APRS packet on. (default is 14580) 
   * *This non-standard port is blocked on some networks*.

get_weather_data() and build_packet() will also return the data they generate to a variable if specified.

```python
weather_data = aprs.get_weather_data()
my_packet = aprs.build_packet()
```

The send_packet() method can also send a manually constructed APRS packet by passing it into the function.
```python
aprs.send_packet('MY PACKET DATA')
```

# Why?
I want to send data from my own Weather Station to CWOP without needing to pay for another piece of software.