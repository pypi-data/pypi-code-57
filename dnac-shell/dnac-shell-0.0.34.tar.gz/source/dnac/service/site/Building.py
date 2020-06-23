import json
from jinja2 import Template
from dnac.maglev.security.SecurityManager import SecurityManager
from dnac.service.site.Site import Site
from dnac.exception.BadProjectFileException import InvalidAttributeException


# copyright (c) 2019 cisco Systems Inc., ALl righhts reseerved

class Building(Site):
    def __init__(self, id, name, hierarchy, address=' ', parent=''):
        super().__init__(id, name, hierarchy, False, parent)
        self._address_ = address
        self._geo_ = None
        self._parent_site_ = None
        self._floors_ = dict()

    @classmethod
    def with_geocoords(cls, idx, namex, parentsite, geocoord):
        building = cls(idx, namex, parentsite.hierarchy + '/' + namex.strip(), ' ', parentsite.id)
        building.geocoordinates = geocoord
        building.parentSite = parentsite
        return building

    @property
    def parentSite(self):
        return self._parent_site_

    @parentSite.setter
    def parentSite(self, parent_site):
        self._parent_site_ = parent_site

    @property
    def address(self):
        return self._address_

    @address.setter
    def address(self, address):
        self._address_ = address

    @property
    def geocoordinates(self):
        return self._geo_

    @property
    def latitude(self):
        return self.geocoordinates[0]

    @property
    def longitude(self):
        return self.geocoordinates[1]

    @geocoordinates.setter
    def geocoordinates(self, geo):
        self._geo_ = geo

    @property
    def floor_count(self):
        return len(self._floors_)

    def get_floor(self, id):
        return self._floors_[id] if id else None

    def get_all_floors(self):
        return [self._floors_[idx] for idx in self._floors_]

    def add_floor(self, floor):
        if not floor or not floor.id:
            raise InvalidAttributeException(floor)
        self._floors_[floor.id] = floor

    def remove_floor(self, floor):
        if not floor or not floor.id:
            raise InvalidAttributeException(floor)
        del self._floors_[floor.id]

    @property
    def jsonTemplate(self):
        return '''
	{
   		"groupTypeList":[
      		"SITE"
   		],
   		"parentId":"{{ tvPARENT_SITE_ID }}",
   		"name":"{{ tvSITE_NAME }}",
   		"childIds":[""],
   		"additionalInfo":[
      			{
         			"nameSpace":"Location",
         			"attributes":{
            				"type":"building",
            				"address":"{{ tvADDRESS }}",
            				"latitude":"{{ tvLATITUDE }}",
            				"longitude":"{{ tvLONGITUDE }}",
            				"country":"United States"
         			}
      			}
   		]
	}
	 	       '''

    # Generate Json version of this object
    @property
    def dnacJson(self):
        x = Template(self.jsonTemplate)

        # Generate stringified operations list...
        return x.render(tvSITE_NAME=self.name, tvPARENT_SITE_ID=self.parentSite.id, tvADDRESS=self.address,
                        tvLATITUDE=self.latitude, tvLONGITUDE=self.longitude)

    # Print out the object
    def print(self):
        print('==== Building ===')
        print('Name = ' + self.name)
        print('Id = ' + str(self.id))
        print('parentId = ' + str(self.parentSite.id))
        print('Hierarchy = ' + str(self.hierarchy))
        print('Address = ' + self.address if self.address else "<None>")
        print('=============')


#
if __name__ == "__main__":
    cbjson = '''
		[{"systemGroup":true,"groupHierarchy":"69444522-a32c-4e59-90fa-bad096537201","groupNameHierarchy":"Global","additionalInfo":[{"nameSpace":"System Settings","attributes":{"group.count.total":"2","hasChild":"TRUE","group.count.direct":"1","group.hierarchy.groupType":"SITE","member.count.total":"0","member.count.direct":"0"}}],"name":"Global","instanceTenantId":"SYS0","id":"69444522-a32c-4e59-90fa-bad096537201"}]
		'''

    bldg = Building('12345', 'SJC04', hierarchy=' ', address='170 East Tasman Drive, San Jose, Ca 95134, USA ',
                    parent='')
    bldg.print()
    print(bldg.dnacJson)
