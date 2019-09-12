from ambient_aprs.ambient_aprs import AmbientAPRS

aa = AmbientAPRS(
    host='rotate.aprs.net',
    use_passcode=True,
    station_id='KD2OTL',
    latitude=43.131258,
    longitude=-76.155028
)

print(aa.get_weather_data())
print(aa.build_packet())
if aa.send_packet():
    print('Sent')
else:
    print('Failed')
