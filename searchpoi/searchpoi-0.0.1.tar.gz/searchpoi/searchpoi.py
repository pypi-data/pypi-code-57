import geopandas as gpd
import overpy
import pandas as pd
from shapely.geometry import Point


class SearchPoi:
    """This class fetch PoIs from Overpass Api for a specific area."""

    tags = {'tourism', 'shop', 'office', 'historic', 'craft', 'emergency', 'station', 'public_transport', 'amenity'}

    def __init__(self, area):
        """
        Constructor of  SearchPoi class

        Parameters:
        area (string): Name of the area to search

        Returns:
        SearchPoi: return the object of this class

        """
        self.area = area
        self.__init_overpass_api()

    def __init_overpass_api(self):

        self.__api = overpy.Overpass()

        nodes = pd.DataFrame(columns=["Latitude", "Longitude", "Tag"])
        result = self.__query_overpass_api(self.tags)
        for node in result.nodes:
            for tag in node.tags.keys():
                if (tag in self.tags):
                    nodes.loc[len(nodes)] = [node.lat, node.lon, tag]

        gdf = gpd.GeoDataFrame(
            nodes, geometry=gpd.points_from_xy(nodes.Longitude, nodes.Latitude), crs='EPSG:4326')

        self.gdf = gdf.drop(columns=['Latitude', 'Longitude']).to_crs('EPSG:2163')

    def __query_overpass_api(self, tags):
        query_string = ''

        for tag in tags:
            query_string += 'area[name="' + self.area + '"]; ('
            query_string += 'node["' + tag + '"](area);'
            query_string += '); out;'

        return self.__api.query(query_string)

    def closest(self, lon, lat, distance=5.0):
        """
        Find closest PoI near the point and return a summary

        Parameters:
        lon (float): Longitude of the point
        lat (float): Latitude of the point
        distance (float): distance of the buffer in kilometers. Defaults is 5km

        Returns:
        pandas.DataFrame: return a summary of the closest points group by tags

        """
        gpd_buffer = gpd.GeoDataFrame(geometry=[Point(lon, lat)], crs='EPSG:4326').to_crs('EPSG:2163')
        buffer_length_in_km = (distance * 1000)
        gpd_buffer = gpd_buffer.buffer(buffer_length_in_km)

        tmp = self.gdf[self.gdf.geometry.intersects(gpd_buffer.loc[0])]
        result = pd.DataFrame(columns=self.tags)
        for tag in self.tags:
            result[tag] = tmp[tmp['Tag'] == tag].count()
        result = result.drop('geometry', axis=0)
        return result
