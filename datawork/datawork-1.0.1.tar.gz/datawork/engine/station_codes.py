from orm_collector.manager import SessionCollector


session = SessionCollector(log_path="~/logs")
stations_all = session.get_stations()
stations = [s for s in stations_all]

print("SSSSSS=====SSSSS")
print(stations)

