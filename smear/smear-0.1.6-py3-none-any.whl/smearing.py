import enum
from smear.uiterm import markup_print


class SmearingEngines:
    EIC_SMEAR = 'eic_smear'
    JLEIC_SMEAR = 'jleic_smear'


class DetectorDescription:
    def __init__(self, version='', description='', flag='', engine='eic_smear', link=''):
        self.version = version
        self.description = description
        self.engine = engine
        self.link = link


detectors = {
    "matrix": DetectorDescription(
            version='v0.1',
            description="Yellow Reports Detector Working Goroup detector based on the Detector Matrix (alias to matrix-0.1)",
            link='https://physdiv.jlab.org/cgi-bin/DetectorMatrix/view',
            engine=str(SmearingEngines.EIC_SMEAR)
        ),

    "matrix-0.1": DetectorDescription(
            version='v0.1',
            description="Strict handbook table (simple smear engine by YF)",
            link='eic_smear/ESDetectorHandBook_v1_0_4.cc',
            engine=str(SmearingEngines.JLEIC_SMEAR)
        ),
    "smatrix": DetectorDescription(
        version='v0.0',
        description="Strict YP DWG Matirx table (simple smear engine by YF)",
        link='eic_smear/ESDetectorHandBook_v1_0_4.cc',
        engine=str(SmearingEngines.JLEIC_SMEAR)
    ),
    "handbook": DetectorDescription(
        version='v1.2',
        description="Based on HANDBOOK v1.2 (Feb 20, 2020) with adaptations (alias to handbook-1.2)",
        link='http://www.eicug.org/web/content/detector-rd',
        engine=str(SmearingEngines.EIC_SMEAR)
    ),

    "handbook-1.2": DetectorDescription(
        version='v1.2',
        description="Based on HANDBOOK v1.2 (Feb 20, 2020) with adaptations",
        link='http://www.eicug.org/web/content/detector-rd',
        engine=str(SmearingEngines.EIC_SMEAR)
    ),

    "beast": DetectorDescription(
        version='v0.1',
        description="BeAST (alias to beast 0.1)",
        link='ESDetectorBeAST_v1_0_4.cc',
        engine=str(SmearingEngines.EIC_SMEAR)
    ),

    "beast-0.1": DetectorDescription(
        version='v0.1',
        description="BeAST detector ",
        link='https://arxiv.org/abs/1708.01527',
        engine=str(SmearingEngines.EIC_SMEAR)
    ),
    "beast-0.0": DetectorDescription(
        version='v0.0',
        description="BeAST",
        link='https://arxiv.org/abs/1708.01527',
        engine=str(SmearingEngines.EIC_SMEAR)
    ),
    "jleic": DetectorDescription(
        version='0.2',
        description="JLEIC detector (simple smear engine by YF)",
        link='',
        engine=str(SmearingEngines.JLEIC_SMEAR)
    ),
    "jleic-0.2": DetectorDescription(
        version='0.2',
        description="JLEIC (simple smear engine)",
        link='',
        engine=str(SmearingEngines.JLEIC_SMEAR)
    ),
    "jleic-0.1": DetectorDescription(
        version='0.1',
        description="JLEIC (simple smear engine)",
        link='',
        engine=str(SmearingEngines.JLEIC_SMEAR)
    ),
    "ephenix": DetectorDescription(
        version='v0.0',
        description="ePHENIX detector (Example from 2014)",
        link='ePHENIX',
        engine=str(SmearingEngines.EIC_SMEAR)
    ),
    "ephenix_nms": DetectorDescription(
        version='v0.0',
        description="ePHENIX detector (Example from 2014). No multiple scattering",
        link='https://arxiv.org/abs/1708.01527',
        engine=str(SmearingEngines.EIC_SMEAR)
    ),
    "estar": DetectorDescription(
        version='v0.0',
        description="An example implementation from 2014",
        link='https://wiki.bnl.gov/conferences/index.php/January_2014',
        engine=str(SmearingEngines.EIC_SMEAR)
    ),
    "star": DetectorDescription(
        version='v0.0',
        description="STAR parametrization example",
        link='https://wiki.bnl.gov/conferences/index.php/January_2014',
        engine=str(SmearingEngines.EIC_SMEAR)
    ),
    "zeus": DetectorDescription(
        version='v0.0',
        description="Example of ZEUS detector",
        link='ESDetectorZeus_v1_0_0.cc',
        engine=str(SmearingEngines.EIC_SMEAR)
    ),
    "perfect": DetectorDescription(
        version='0.0',
        description="Perfect detection and PID in |η| < 15",
        link='',
        engine=str(SmearingEngines.JLEIC_SMEAR)
    ),
}


def print_detectors():
    """ Pretty prints detectors list"""
    for name, detector in detectors.items():
        markup_print("\n<blue>detector</blue>: {}".format(name))
        markup_print(" <b>version</b> : {}".format(detector.version))
        markup_print(" <b>descr.</b>  : {}".format(detector.description))
        markup_print(" <b>link</b>    : {}".format(detector.link))
        markup_print(" <b>engine</b>  : {}".format(detector.engine))


if __name__ == '__main__':
    print_detectors()
