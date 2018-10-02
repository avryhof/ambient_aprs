# ambient_aprs
Wrapper for ambient_api to allow sending APRS packets to CWOP

# Goal
* Class that can be initialized with a AmbientWeatherStation object from ambient_api
* Function that can be called with APRS receiver credentials, that will just send the Weather Station's most recent data 
directly to the APRS receiver.

# Why?
I want to send data from my own Weather Station to CWOP without needing to pay for another piece of software.