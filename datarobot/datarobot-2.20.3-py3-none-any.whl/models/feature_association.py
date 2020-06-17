import trafaret as t

from datarobot.models.api_object import APIObject
from datarobot.utils import encode_utf8_if_py2


class FeatureAssociation(APIObject):
    """ Feature association statistics for a project.

    Attributes
    ----------
    type : str
        Either 'association' or 'correlation' the class of the pairwise stats
    metric : str
        the metric of either class of pairwise stats
        'spearman', 'pearson', etc for correlation, 'mutualInfo', 'cramersV'
        for association
    """
    _converter = t.Dict({
        t.Key('type'): t.Or(t.String, t.Null),
        t.Key('metric'): t.Or(t.String, t.Null),
        t.Key('featurelistId'): t.Or(t.String, t.Null)
    })

    def __init__(self, metric=None, assoc_type=None, featurelistId=None):
        self.metric = metric if metric else 'mutualInfo'
        self.assoc_type = type if type else 'association'
        self.featurelistId = featurelistId

    def __repr__(self):
        return encode_utf8_if_py2(u'FeatureAssociation({}/{}/{})'.format(
            self.assoc_type, self.metric, self.featurelistId))


class FeatureAssociationMatrixDetails(APIObject):
    """ Plotting details for a pair of passed features present in the feature
    association matrix

    Attributes
    ----------
    feature1 : str
        Feature name for the first feature of interest
    feature2 : str
        Feature name for the second feature of interest
    """
    _converter = t.Dict({
        t.Key('feature1'): t.String,
        t.Key('feature2'): t.String
    })

    def __init__(self, feature1=None, feature2=None):
        self.feature1 = feature1
        self.feature2 = feature2

    def __repr__(self):
        return encode_utf8_if_py2(u'FeatureAssociationMatrixDetails({}/{})'.format(
            self.feature1, self.feature2))


class FeatureAssociationFeaturelists(APIObject):
    """ Get project featurelists and see if they have association statistics
    """
    def __repr__(self):
        return encode_utf8_if_py2(u'FeatureAssocationFeaturelists')
