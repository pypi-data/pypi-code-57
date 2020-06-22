from api import API

if __name__ == '__main__':
    api = API("telekom-de", "cae6e4b9-00ca-4019-be80-26ed36a30979", "4d37a73e-72a3-466f-8ed2-f0fd4026cb77",
              "si.tenbeitel@gmx.de", "Pr0gramm13r3n!")
    api.login()
    vehicles = api.get_vehicles()
    print(vehicles[0].licence_plate)
