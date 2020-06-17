########################################################################################################################
#                                          N-HANS speech separator                                                     #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#   Description:      Loading separator model.                                                                         #
#   Authors:          Shuo Liu, Gil Keren, Bjoern Schuller                                                             #
#   Affiliation:      Chair of Embedded Intelligence for Health Care and Wellbeing, University of Augsburg (UAU)  #
#   Version:          2.0                                                                                              #
#   Last Update:      May. 06, 2020                                                                                    #
#   Dependence Files: xxx                                                                                              #
#   Contact:          shuo.liu@informatik.uni-augburg.de                                                               #
########################################################################################################################
#                                                                                                                      #
#   Copyright (C) 2019, Shuo Liu, Gil Keren and Björn Schuller: University of Augsburg.                                #
#                                                                                                                      #
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public    #
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any       #
# later version.                                                                                                       #
#                                                                                                                      #
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied   #
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.#
#                                                                                                                      #
# You should have received a copy of the GNU General Public License along with this program. #  If not, see            #
# <http://www.gnu.org/licenses/>.                                                                                      #
#                                                                                                                      #
########################################################################################################################

import os


def main():
    dropbox_link = 'https://www.dropbox.com/s/wdk62o4kt8lbvjr/N_HANS___Separator.zip?dl=0'
    download_filename = 'N_HANS_separator.zip'
    command_download = 'wget {} -O {}'.format(dropbox_link, download_filename)
    command_unzip = 'unzip N_HANS_separator.zip'

    os.system(command_download)
    os.system(command_unzip)

