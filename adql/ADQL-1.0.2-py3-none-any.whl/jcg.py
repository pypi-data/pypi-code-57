from adql import ADQL
from spatial_index import SpatialIndex
  
 
# Set up the ADQL statement
 
adql_string = []

adql_string.append("select TOP 100 ave(ra) as ra, ave(declination) as dec from iraspsc where (contains(point('icrs', ra, dec), circle('GALACTIC', 234.56, 34.567, 0.57)) = 1 and dec > 0.) or (0=contains(point('icrs', ra, dec), circle('GALACTIC', 234.56, -34.567, 0.46))and dec > 0.) group by ra, dec order by dec desc")

for i in range(len(adql_string)):

    print('------------------------------------')
    print('')
    print('BEFORE: ', adql_string[i])
    print('')

    adql = ADQL(level=20, debugfile='jcg.debug',
                racol='ra2000', deccol='dec2000',
                xcol = 'x', ycol='y', zcol='z', indxcol='htm20',
                mode=SpatialIndex.HTM, encoding=SpatialIndex.BASE10)

    try:
        sql_string = adql.sql(adql_string[i])

        print('AFTER:  ', sql_string)
        print('')

    except Exception as adql_error:
        print('ERROR: ', adql_error)
