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
from tvb.simulator.coupling import *
from tvb.adapters.simulator.form_with_ranges import FormWithRanges
from tvb.core.neotraits.forms import ArrayField, ScalarField


def get_coupling_to_form_dict():
    coupling_class_to_form = {
        Linear: LinearCouplingForm,
        Scaling: ScalingCouplingForm,
        HyperbolicTangent: HyperbolicTangentCouplingForm,
        Sigmoidal: SigmoidalCouplingForm,
        SigmoidalJansenRit: SigmoidalJansenRitForm,
        PreSigmoidal: PreSigmoidalCouplingForm,
        Difference: DifferenceCouplingForm,
        Kuramoto: KuramotoCouplingForm
    }
    return coupling_class_to_form


def get_ui_name_to_coupling_dict():
    ui_name_to_coupling = {}
    for coupling_class in get_coupling_to_form_dict():
        ui_name_to_coupling.update({coupling_class.__name__: coupling_class})

    return ui_name_to_coupling


def get_form_for_coupling(coupling_class):
    return get_coupling_to_form_dict().get(coupling_class)


class LinearCouplingForm(FormWithRanges):

    def __init__(self, prefix=''):
        super(LinearCouplingForm, self).__init__(prefix)
        self.a = ArrayField(Linear.a, self)
        self.b = ArrayField(Linear.b, self)


class ScalingCouplingForm(FormWithRanges):

    def __init__(self, prefix=''):
        super(ScalingCouplingForm, self).__init__(prefix)
        self.a = ArrayField(Scaling.a, self)


class HyperbolicTangentCouplingForm(FormWithRanges):

    def __init__(self, prefix=''):
        super(HyperbolicTangentCouplingForm, self).__init__(prefix)
        self.a = ArrayField(HyperbolicTangent.a, self)
        self.b = ArrayField(HyperbolicTangent.b, self)
        self.midpoint = ArrayField(HyperbolicTangent.midpoint, self)
        self.sigma = ArrayField(HyperbolicTangent.sigma, self)


class SigmoidalCouplingForm(FormWithRanges):

    def __init__(self, prefix=''):
        super(SigmoidalCouplingForm, self).__init__(prefix)
        self.cmin = ArrayField(Sigmoidal.cmin, self)
        self.cmax = ArrayField(Sigmoidal.cmax, self)
        self.midpoint = ArrayField(Sigmoidal.midpoint, self)
        self.a = ArrayField(Sigmoidal.a, self)
        self.sigma = ArrayField(Sigmoidal.sigma, self)


class SigmoidalJansenRitForm(FormWithRanges):

    def __init__(self, prefix=''):
        super(SigmoidalJansenRitForm, self).__init__(prefix)
        self.cmin = ArrayField(SigmoidalJansenRit.cmin, self)
        self.cmax = ArrayField(SigmoidalJansenRit.cmax, self)
        self.midpoint = ArrayField(SigmoidalJansenRit.midpoint, self)
        self.r = ArrayField(SigmoidalJansenRit.r, self)
        self.a = ArrayField(SigmoidalJansenRit.a, self)


class PreSigmoidalCouplingForm(FormWithRanges):

    def __init__(self, prefix=''):
        super(PreSigmoidalCouplingForm, self).__init__(prefix)
        self.H = ArrayField(PreSigmoidal.H, self)
        self.Q = ArrayField(PreSigmoidal.Q, self)
        self.G = ArrayField(PreSigmoidal.G, self)
        self.P = ArrayField(PreSigmoidal.P, self)
        self.theta = ArrayField(PreSigmoidal.theta, self)
        self.dynamic = ScalarField(PreSigmoidal.dynamic, self)
        self.globalT= ScalarField(PreSigmoidal.globalT, self)


class DifferenceCouplingForm(FormWithRanges):

    def __init__(self, prefix=''):
        super(DifferenceCouplingForm, self).__init__(prefix)
        self.a = ArrayField(Difference.a, self)


class KuramotoCouplingForm(FormWithRanges):

    def __init__(self, prefix=''):
        super(KuramotoCouplingForm, self).__init__(prefix)
        self.a = ArrayField(Kuramoto.a, self)