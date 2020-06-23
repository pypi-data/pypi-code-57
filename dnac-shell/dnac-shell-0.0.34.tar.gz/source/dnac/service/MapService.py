import requests
import json
from dnac.exception import DnacException
from dnac.exception import InvalidCriterionException
from dnac.maglev.security.role.ResourceType import ResourceType
from dnac.maglev.security.role.Role import Role
from dnac.maglev.security.SecurityManager import SecurityManager
from dnac.service.maps.CalibrationModel import CalibrationModel
from dnac.service.maps.Floor import Floor
from dnac.service.maps.FloorGeometry import FloorGeometry
from dnac.maglev.task.TaskManager import TaskManager
from dnac.maglev.task.Task import Task


# copyright (c) 2019 cisco Systems Inc., ALl righhts reseerved

class MapService:
    def __init__(self, services):
        self._services_ = services

    @property
    def maglev(self):
        return self._services_.maglev

    #
    @property
    def dnacSecurityManager(self):
        return self.maglev.security_manager

    #
    @property
    def dnacTaskManager(self):
        return self.maglev.task_manager

    #
    @property
    def groupingService(self):
        return self._services_.groupingService

    #
    @property
    def urlListModels(self):
        return '/api/v1/dna-maps-service/calibration/rfmodels'

    #
    @property
    def urlListFloors(self):
        return '/api/v1/dna-maps-service/domains?type=4'

    def urlListFloorAps(self, floorid):
        return '/api/v1/dna-maps-service/domains/' + floorid.strip() + '/aps'

    def urlListFloorPaps(self, floorid):
        return '/api/v1/dna-maps-service/domains/' + floorid.strip() + '/paps'

    #
    @property
    def urlCreateFloor(self):
        return '/api/v1/dna-maps-service/domains'

    #
    def urlUpdateFloor(self, floorid):
        return '/api/v1/dna-maps-service/domains/' + str(floorid) if floorid else None

    # return  '/api/v1/dna-maps-service/domains/' + floorid.strip() if floorid and floorid.strip() else None

    def urlAssignPaps(self, floorid):
        return '/api/v1/dna-maps-service/domains/' + str(floorid) + '/paps' if floorid else None

    def urlExportArchive(self, floorid):
        return '/api/v1/dna-maps-service/archives/export/' + str(floorid) if floorid else None

    # Discover package version of DNA Maps Service
    def discover_service_version(self):
        return self.maglev.kernel.get_package_version('network-visibility')

    #
    #
    def discover_calibration_models(self):
        cbresp = self.dnacSecurityManager.call_dnac(self.urlListModels)
        return CalibrationModel.parseJson(cbresp.text) if cbresp.status_code == 200 else None

    #

    def discover_floor(self, hierarchy):
        return self.groupingService.discover_site_hierarchy(hierarchy) if hierarchy and hierarchy.strip() else None

    def update_floor(self, floor):
        pass
        # return self.groupingService.discover_site_hierarchy(hierarchy) if hierarchy and hierarchy.strip() else None

    def update_floor_backdrop(self, floor, image):
        return self.dnacSecurityManager.post_image_to_dnac(floor.backdropImageUrl, image)

    #
    # Create a floor with the given parameters
    #
    def create_floor(self, floor):
        if floor:
            print('floor json = ', floor.dnacJson)
            # Create the async task...
            response = self.dnacSecurityManager.post_to_dnac(self.urlCreateFloor, floor.dnacJson)
            if response.status_code < 200 or response.status_code > 202:
                return None

            #
            # Expect a task response - follow the taskid to completion
            #
            task = Task.parseJson(response.text)

            # Follow the async task to completion
            floor.id = self.dnacTaskManager.follow_task(task)
            print('floor id = ' + str(floor.id))
            print(floor)
            return floor

        raise ValueError('Request to create Invalid floor - ignored')

    #
    # Update an existing floor with the given parameters
    #
    def update_floor(self, floor):
        '''
            Update the specified floor
        '''
        if floor:
            # Create the async task...
            print(floor.id)
            url = self.urlUpdateFloor(floor.id)
            response = self.dnacSecurityManager.post_to_dnac(url, floor.dnacJson, operation='put')
            print('put - ')
            print(response.status_code)
            print(response.text)
            if response.status_code < 200 or response.status_code > 202:
                return None

            #
            # Expect a task response - follow the taskid to completion
            #
            task = Task.parseJson(response.text)

            # Follow the async task to completion
            floor.id = self.dnacTaskManager.follow_task(task)
            return floor

        raise ValueError('Request to create Invalid floor - ignored')

    #
    # Delete the specified floor
    #
    def delete_floor(self, floor):
        '''
            Delete the specified floor
        '''
        if floor and floor.url:

            response = self.dnacSecurityManager.post_to_dnac(url=floor.url, json_payload='', operation='delete')
            if response.status_code < 200 or response.status_code > 202:
                return False

            #
            # Expect a task response - follow the taskid to completion
            #
            self.dnacTaskManager.follow_task(Task.parseJson(response.text))
            return True

        raise ValueError('Request to delete Invalid or non-existant floor')

    #
    # Assign PAPs to the  specified floor
    #
    def assign_paps(self, floorx, pap):

        if not floorx or not pap:
            raise ValueError('Invalid parameter sin PAP assignment request - ignored')

        # Create the async task...
        papJson = '[' + pap.dnacJson + ']'
        response = self.dnacSecurityManager.post_to_dnac(self.urlAssignPaps(floorx.id), papJson)
        if response.status_code < 200 or response.status_code > 202:
            return

        #
        # Expect a task response - follow the taskid to completion
        #
        # print('Pap task ', response.text)
        # task = Task.parseJson(response.text)

        # Follow the async task to completion
        # self.dnacTaskManager.follow_task(task)
        return

    #
    # Export the specified site/building/floor
    #
    def export_site(self, sitex, filenamex):

        if not sitex:
            sitex = self.groupingService.discover_global()
            raise ValueError('Fatal internal error: Failed to identify the global site')

        # Create the async task...
        response = self.dnacSecurityManager.post_to_dnac(self.urlExportArchive(sitex), filenamex, operation='post',
                                                         given_headers={'Content-Type': 'application/json',
                                                                        'Accept': '*/*'})
        if response.status_code < 200 or response.status_code > 202:
            response = self.dnacSecurityManager.post_to_dnac(self.urlExportArchive(sitex), filenamex, operation='post',
                                                             given_headers={'Content-Type': 'text/plain',
                                                                            'Accept': '*/*'})
            if response.status_code < 200 or response.status_code > 202:
                return response.status_code, None

        resp_content_type = response.headers['Content-Type']
        if 'application/json' in resp_content_type:
            #
            # Expect a task response - follow the taskid to completion
            #
            task = Task.parseJson(response.text)
            # Follow the async task to completion
            result = self.dnacTaskManager.follow_task(task)
            return response.status_code, resp_content_type, result
        elif 'application/octet-stream' in resp_content_type:
            return response.status_code, resp_content_type, response.content
        else:
            raise ValueError('Fatal error: Unrecognized response from server: ', response.status_code, response.headers,
                             response.headers)

    def discover_floor_aps(self, floorid):
        cbresp = self.dnacSecurityManager.call_dnac(self.urlListFloorAps(floorid))
        if cbresp.status_code == 200:
            cbs = json.loads(cbresp.text)
            return cbs['items']
        return None

    def discover_floor_paps(self, floorid):
        cbresp = self.dnacSecurityManager.call_dnac(self.urlListFloorPaps(floorid))
        if cbresp.status_code == 200:
            cbs = json.loads(cbresp.text)
            return cbs['items']
        return None
