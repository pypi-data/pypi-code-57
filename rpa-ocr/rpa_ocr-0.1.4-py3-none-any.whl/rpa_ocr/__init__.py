# -*- coding:utf-8 -*-
# @author :adolf
__name__ = 'rpa_ocr'
__version__ = '0.1.4'
from rpa_ocr.Identify_English.train_tools import Train
from rpa_ocr.verification_service.verification_main import ocr_pipeline_main
from rpa_ocr.Identify_English.inference import CRNNInference
