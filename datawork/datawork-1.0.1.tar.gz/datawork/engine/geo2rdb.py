import rethinkdb as r

def geojson2rethinkjson(content):
    """
    content is a GeoJson object must be converted to a RethinkDB JSON object....
    """

    try:
        # print("Content...:%s"%content['properties'])
        time = content['properties']['time']
        dt0 = content['properties']['dt']
        #print("Datetime Original %s" %dt0)
        c_datetime = dt0.isoformat()
        #print("Fecha y tiempo %s" %dt0.isoformat())
        dt = r.iso8601(dt0.isoformat())
        dt_gen = content['properties']['DT_GEN']
    except Exception as ex:
        print("Error en calcular fecha tiempo %s" % ex)
        raise ex
    new_value = dict(
        source="DataWork",
        station_name=content['properties']['station'],
        DT_GEN=dt_gen,
        timestamp=time,
        data={
            'N': {
                'value': content['features'][0]['geometry']['coordinates'][0],
                'error': content['properties']['NError'],
                'min': content['features'][0]['geometry']['coordinates'][0]-content['properties']['NError'],
                'max': content['features'][0]['geometry']['coordinates'][0]+content['properties']['NError']
            },
            'E': {
                'value': content['features'][0]['geometry']['coordinates'][1],
                'error': content['properties']['EError'],
                'min': content['features'][0]['geometry']['coordinates'][1]-content['properties']['EError'],
                'max': content['features'][0]['geometry']['coordinates'][1]+content['properties']['EError']

            },
            'U': {
                'value': content['features'][0]['geometry']['coordinates'][2],
                'error': content['properties']['UError'],
                'min': content['features'][0]['geometry']['coordinates'][2]-content['properties']['UError'],
                'max': content['features'][0]['geometry']['coordinates'][2]+content['properties']['UError']
            },
        }
        # last_update=datetime.utcnow()
    )

    return new_value
