from datetime import datetime
from socket import socket, AF_INET, SOCK_STREAM

from ambient_api.ambientapi import AmbientAPI


class AmbientAPRS:
    send_id = 'Ambient APRS'

    station_id = None

    server_host = 'cwop.aprs.net'
    server_port = 14580
    address = None

    position = None

    wx_data = None
    packet_data = None

    def __init__(self, **kwargs):
        self.send_id = kwargs.get('send_id', 'Ambient APRS')

        self.station_id = kwargs.get('station_id', None)
        self.server_host = kwargs.get('host', 'cwop.aprs.net')
        self.server_port = kwargs.get('port', 14580)

        self.latitude = kwargs.get('latitude', None)
        self.longitude = kwargs.get('longitude', None)

        if self.latitude and self.longitude:
            self.position = '%s/%s_' % (self.convert_latitude(self.latitude), self.convert_longitude(self.longitude))

        if self.station_id:
            self.address = '%s>APRS,TCPIP*:' % self.station_id

    def decdeg2dms(self, degrees_decimal):
        is_positive = degrees_decimal >= 0
        degrees_decimal = abs(degrees_decimal)
        minutes, seconds = divmod(degrees_decimal * 3600, 60)
        degrees, minutes = divmod(minutes, 60)
        degrees = degrees if is_positive else -degrees

        degrees = str(int(degrees)).zfill(2).replace('-', '0')
        minutes = str(int(minutes)).zfill(2).replace('-', '0')
        seconds = str(int(round(seconds * .01, 2) * 100)).zfill(2)

        return {'degrees': degrees, 'minutes': minutes, 'seconds': seconds}

    def decdeg2dmm_m(self, degrees_decimal):
        is_positive = degrees_decimal >= 0
        degrees_decimal = abs(degrees_decimal)
        minutes, seconds = divmod(degrees_decimal * 3600, 60)
        degrees, minutes = divmod(minutes, 60)
        degrees = degrees if is_positive else -degrees

        degrees = str(int(degrees)).zfill(2).replace('-', '0')
        minutes = str(round(minutes + (seconds / 60), 2)).zfill(5)

        return {'degrees': degrees, 'minutes': minutes}

    def convert_latitude(self, degrees_decimal):
        det = self.decdeg2dmm_m(degrees_decimal)
        if degrees_decimal > 0:
            direction = 'N'
        else:
            direction = 'S'

        degrees = det.get('degrees')
        minutes = det.get('minutes')

        lat = '%s%s%s' % (degrees, str(minutes), direction)

        return lat

    def convert_longitude(self, degrees_decimal):
        det = self.decdeg2dmm_m(degrees_decimal)
        if degrees_decimal > 0:
            direction = 'E'
        else:
            direction = 'W'

        degrees = det.get('degrees')
        minutes = det.get('minutes')

        lon = '%s%s%s' % (degrees, str(minutes), direction)

        return lon

    def hg_to_mbar(self, hg_val):
        """
        Convert inches of mercury (inHg to tenths of millibars/tenths of hPascals (mbar/hPa)
        :param hg_val: The value in inHg
        :return:
        """
        mbar = (hg_val / 0.029530) * 10

        return mbar

    def str_or_dots(self, number, length):
        # If parameter is None, fill with dots, otherwise pad with zero
        retn_value = number

        if not number:
            retn_value = '.' * length

        else:
            format_type = {
                'int': 'd',
                'float': '.0f',
            }[type(number).__name__]

            retn_value = ''.join(('%0', str(length), format_type)) % number

        return retn_value

    def make_aprs_wx(self, **kwargs):
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
            self.str_or_dots(wind_dir, 3),
            self.str_or_dots(wind_speed, 3),
            self.str_or_dots(wind_gust, 3),
            self.str_or_dots(temperature, 3),
            self.str_or_dots(rain_last_hr, 3),
            self.str_or_dots(rain_last_24_hrs, 3),
            self.str_or_dots(rain_since_midnight, 3),
            self.str_or_dots(humidity, 2),
            self.str_or_dots(pressure, 5),
        )

    def get_weather_data(self):
        amb_api = AmbientAPI()
        devices = amb_api.get_devices()
        if len(devices) > 0:
            device = devices[0]
            weather = device.last_data

            # Prepare the data, which will be sent
            self.wx_data = self.make_aprs_wx(
                wind_dir=weather.get('winddir'),
                wind_speed=float(weather.get('windspeedmph')),
                wind_gust=float(weather.get('windgustmph')),
                temperature=weather.get('tempf'),
                rain_last_hr=weather.get('hourlyrainin'),
                rain_last_24_hrs=None,
                rain_since_midnight=weather.get('dailyrainin'),
                humidity=weather.get('humidity'),
                # Attention, barometric pressure in tenths of millibars/tenths of hPascal!
                pressure=self.hg_to_mbar(weather.get('baromabsin'))
            )

        return self.wx_data

    def build_packet(self):
        if self.address and self.position and self.wx_data:
            utc_datetime = datetime.now()
            self.packet_data = '%s@%sz%s%s%s' % (
                self.address,
                utc_datetime.strftime("%d%H%M"),
                self.position,
                self.wx_data,
                self.send_id)

        return self.packet_data

    def send_packet(self, packet=None):
        if packet or self.packet_data:
            try:
                # Create socket and connect to server
                sSock = socket(AF_INET, SOCK_STREAM)
                sSock.connect((self.server_host, self.server_port))
                # Log on
                login = 'user %s pass -1 vers Python\n' % self.station_id
                sSock.send(login.encode('utf-8'))
                # Send packet
                if packet:
                    sSock.send(packet.encode('utf-8'))
                elif self.packet_data:
                    sSock.send(self.packet_data.encode('utf-8'))
                # Close socket, must be closed to avoid buffer overflow
                sSock.shutdown(0)
                sSock.close()
            except Exception as e:
                return False

            else:
                return True

        else:
            return False
