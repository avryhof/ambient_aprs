# Script from https://raspberrypiandstuff.wordpress.com/2017/08/07/uploading-aprscwop-weather-data/
import pprint
import sys
from datetime import datetime
# from socket import *
from socket import socket, AF_INET, SOCK_STREAM

from ambient_api.ambientapi import AmbientAPI

from ambient_aprs.ambient_aprs import AmbientAPRS

station_id = 'KD2OTL'

serverHost = 'cwop.aprs.net'
serverPort = 14580
address = '%s>APRS,TCPIP*:' % station_id

# Attention, format of the location is bit special. Although there is a dot, the values are in degrees, minutes and seconds!
# COORDS: N 43.13132 W 76.15509   ---- 43.131258 -76.155028 -- 4307.53N  07609.18W
# Elevation in Meters: 	128
# Elevation in Feet: 	419.95
position = '4307.53N/07609.18W_'

aa = AmbientAPRS()
print(aa.convert_latitude(43.131258))
print(aa.convert_longitude(-76.155028))

def hg_to_mbar(hg_val):
    """
    Convert inches of mercury (inHg to tenths of millibars/tenths of hPascals (mbar/hPa)
    :param hg_val: The value in inHg
    :return:
    """
    return (hg_val / 0.029529983071445) / 10


def str_or_dots(number, length):
    # If parameter is None, fill with dots, otherwise pad with zero
    if not number:
        return '.' * length
    else:
        format_type = {
            'int': 'd',
            'float': '.0f',
        }[type(number).__name__]
        return ''.join(('%0', str(length), format_type)) % number


def send_packet():
    # here is where the big change happens.... rather than using rrdtool, we will just use the API
    amb_api = AmbientAPI()
    devices = amb_api.get_devices()
    device = devices[0]
    weather = device.last_data

    # Prepare the data, which will be sent
    wx_data = make_aprs_wx(
        wind_dir=weather.get('winddir'),
        wind_speed=float(weather.get('windspeedmph')),
        wind_gust=float(weather.get('windgustmph')),
        temperature=weather.get('tempf'),
        rain_last_hr=weather.get('hourlyrainin'),
        rain_last_24_hrs=None,
        rain_since_midnight=weather.get('dailyrainin'),
        humidity=weather.get('humidity'),
        # Attention, barometric pressure in tenths of millibars/tenths of hPascal!
        pressure=hg_to_mbar(weather.get('baromabsin'))
    )

    print(wx_data)
    # Use UTC
    utc_datetime = datetime.now()
    packet_data = address + '@' + utc_datetime.strftime("%d%H%M") + 'z' + position + wx_data + 'Ambient APRS\n'
    print(packet_data)
    # Create socket and connect to server
    sSock = socket(AF_INET, SOCK_STREAM)
    sSock.connect((serverHost, serverPort))
    # Log on
    sSock.send('user %s pass -1 vers Python\n' % station_id)
    # Send packet
    sSock.send(packet_data)
    # Close socket, must be closed to avoid buffer overflow
    sSock.shutdown(0)
    sSock.close()


def make_aprs_wx(**kwargs):
    wind_dir = kwargs.get('wind_dir', None)
    wind_speed = kwargs.get('wind_speed', None)
    wind_gust = kwargs.get('wind_gust', None)
    temperature = kwargs.get('temperature', None)
    rain_last_hr = kwargs.get('rain_last_hr', None)
    rain_last_24_hrs = kwargs.get('rain_last_24_hrs', None)
    rain_since_midnight = kwargs.get('rain_since_midnight', None)
    humidity = kwargs.get('humidity', None)
    pressure = kwargs.get('pressure', None)

    # Assemble the weather data of the APRS packet
    return '%s/%sg%st%sr%sp%sP%sh%sb%s' % (
        str_or_dots(wind_dir, 3),
        str_or_dots(wind_speed, 3),
        str_or_dots(wind_gust, 3),
        str_or_dots(temperature, 3),
        str_or_dots(rain_last_hr, 3),
        str_or_dots(rain_last_24_hrs, 3),
        str_or_dots(rain_since_midnight, 3),
        str_or_dots(humidity, 2),
        str_or_dots(pressure, 5),
    )


try:
    send_packet()
except:
    sys.exit(-1)
