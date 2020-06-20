# UQpy is distributed under the MIT license.
#
# Copyright (C) 2020  -- Ketson R. M. dos Santos
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
This module contains the classes and methods to perform the point wise and multi point data-based dimensionality
reduction via projection onto the Grassmann manifold and Diffusion Maps, respectively. Further, interpolation in the
tangent space centered at a given point on the Grassmann manifold can be performed.
* Grassmann: This class contains methods to perform the projection of matrices onto the Grassmann manifold where their
             dimensionality are reduced and where standard interpolation can be performed on a tangent space.
* DiffusionMaps: In this class the diffusion maps create a connection between the spectral properties of the diffusion
                 process and the intrinsic geometry of the data resulting in a multiscale representation of the data.
"""
import scipy as sp
import numpy as np

########################################################################################################################
########################################################################################################################
#                                            Monte Carlo Simulation                                                    #
########################################################################################################################
########################################################################################################################


class MonteCarlo:

    def __init__(self, object=None):

        self.object = distance_object
        
    # Calculate the distance on the manifold
    def MCS(self, nsim=10):

        return nsim

    # ==================================================================================================================
   
