<!-- [![PyPI](https://img.shields.io/pypi/v/ambient_aprs.svg?maxAge=2592000)](https://pypi.python.org/pypi/ambient_aprs) --> 
[![Build Status](https://travis-ci.org/avryhof/ambient_aprs.svg?branch=master)](https://travis-ci.org/avryhof/ambient_aprs) 
[![codecov](https://codecov.io/gh/avryhof/ambient_aprs/branch/master/graph/badge.svg)](https://codecov.io/gh/avryhof/ambient_aprs)
<a href="https://www.codefactor.io/repository/github/avryhof/ambient_aprs"><img alt="CodeFactor" src=
   "https://www.codefactor.io/repository/github/avryhof/ambient_aprs/badge"/></a>

# ambient_aprs
Wrapper for ambient_api to allow sending APRS packets to CWOP

# Goal
* Class that can be initialized with a AmbientWeatherStation object from ambient_api
* Function that can be called with APRS receiver credentials, that will just send the Weather Station's most recent data 
directly to the APRS receiver.

# Why?
I want to send data from my own Weather Station to CWOP without needing to pay for another piece of software.