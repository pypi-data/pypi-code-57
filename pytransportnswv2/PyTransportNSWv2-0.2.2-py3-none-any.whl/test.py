from TransportNSW import TransportNSW
tnsw = TransportNSW()

sApiKey = 'oWwCalKSy0ZQB5JTw7sTXlcaOjv01fto1W3v'
#sStopId = '207261'   #Gordon, platform 1
sStopId = '10101121' #Gordon station
#sDestId = '10101122' #Pymble station
#sStopId = '2000336'  #Central, platform 16
sDestId = '10101421'  #Redfern
#sDestId = '10101331'  #Domestic airport
#sDestId = '2015137' #Redfern, platform 7
#sStopId = '2015133'  #Redfern, platform 11
#sStopId = '207248'   # Gordon bus stop
#sStopId = '207537'   # St Ives stop
#sDestId = '2073161'  #Pymble station
#sStopId = '2000225'   # Circular Quay Wharf 4
#sDestId = '20883'     # Taronga Zoo Wharf
#sStopId = '20461'     # Abbotsford
#sDestId = '2137186'   # Cabarita
nMinDueTime = 6

journey = tnsw.get_trip(sStopId, sDestId, sApiKey, nMinDueTime)
print (' ')
print(journey)
