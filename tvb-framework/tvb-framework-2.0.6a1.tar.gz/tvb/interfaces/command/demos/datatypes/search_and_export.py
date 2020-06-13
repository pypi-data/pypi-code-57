# -*- coding: utf-8 -*-
#
#
# TheVirtualBrain-Framework Package. This package holds all Data Management, and
# Web-UI helpful to run brain-simulations. To use it, you also need do download
# TheVirtualBrain-Scientific Package (for simulators). See content of the
# documentation-folder for more details. See also http://www.thevirtualbrain.org
#
# (c) 2012-2020, Baycrest Centre for Geriatric Care ("Baycrest") and others
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#   CITATION:
# When using The Virtual Brain for scientific publications, please cite it as follows:
#
#   Paula Sanz Leon, Stuart A. Knock, M. Marmaduke Woodman, Lia Domide,
#   Jochen Mersmann, Anthony R. McIntosh, Viktor Jirsa (2013)
#       The Virtual Brain: a simulator of primate brain network dynamics.
#   Frontiers in Neuroinformatics (7:10. doi: 10.3389/fninf.2013.00010)
#
#

"""
Demo script on how to filter datatypes and later export them.

.. moduleauthor:: Lia Domide <lia.domide@codemart.ro>
"""

if __name__ == "__main__":
    from tvb.basic.profile import TvbProfile
    TvbProfile.set_profile(TvbProfile.COMMAND_PROFILE)

from tvb.core.entities.filters.chain import FilterChain
from tvb.core.entities.file.files_helper import FilesHelper
from tvb.core.entities.storage import dao
from tvb.core.entities.transient.structure_entities import DataTypeMetaData
from tvb.datatypes.time_series import TimeSeriesRegion
from tvb.datatypes.connectivity import Connectivity
from sys import argv
import os


TVB_EXPORTER = "TVBExporter"


def _retrieve_entities_by_filters(kind, project_id, filters):

    named_tuple_array, counter = dao.get_values_of_datatype(project_id, kind, filters)
    print("Found " + str(counter) + " entities of type " + str(kind))

    result = []
    for named_tuple in named_tuple_array:
        dt_id = named_tuple[0]
        result.append(dao.get_generic_entity(kind, dt_id)[0])

    return result



def search_and_export_ts(project_id, export_folder=os.path.join("~", "TVB")):

    #### This is the simplest filter you could write: filter and entity by Subject
    filter_connectivity = FilterChain(fields=[FilterChain.datatype + '.subject'],
                                      operations=["=="],
                                      values=[DataTypeMetaData.DEFAULT_SUBJECT])

    connectivities = _retrieve_entities_by_filters(Connectivity, project_id, filter_connectivity)


    #### A more complex filter: by linked entity (connectivity), BOLD monitor, sampling, operation param:
    filter_timeseries = FilterChain(fields=[FilterChain.datatype + '._connectivity',
                                            FilterChain.datatype + '._title',
                                            FilterChain.datatype + '._sample_period',
                                            FilterChain.datatype + '._sample_rate',
                                            FilterChain.operation + '.parameters'
                                            ],
                                    operations=["==", "like", ">=", "<=", "like"],
                                    values=[connectivities[0].gid,
                                            "Bold",
                                            "500", "0.002",
                                            '"conduction_speed": "3.0"'
                                            ]
                                    )

    #### If you want to filter another type of TS, change the kind class bellow,
    #### instead of TimeSeriesRegion use TimeSeriesEEG, or TimeSeriesSurface, etc.
    timeseries = _retrieve_entities_by_filters(TimeSeriesRegion, project_id, filter_timeseries)

    for ts in timeseries:
        print("=============================")
        print(ts.summary_info)
        print(" Original file: " + str(ts.get_storage_file_path()))
        destination_file = os.path.expanduser(os.path.join(export_folder, ts.get_storage_file_name()))
        FilesHelper.copy_file(ts.get_storage_file_path(), destination_file)
        if os.path.exists(destination_file):
            print(" TS file copied at: " + destination_file)
        else:
            print(" Some error happened when trying to copy at destination folder!!")


if __name__ == '__main__':

    if len(argv) < 2:
        PROJECT_ID = 1
    else:
        PROJECT_ID = int(argv[1])

    print("We will try to search datatypes in project with ID:" + str(PROJECT_ID))

    search_and_export_ts(PROJECT_ID)