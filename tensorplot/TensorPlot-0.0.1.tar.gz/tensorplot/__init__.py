""" Init params """
import tensorplot as tp
__version__ = '0.0.1'
__author__ = 'Manuel Blanco Valentin'
__email__ = 'manuel.blanco.valentin@gmail.com'
site = 'http://github.com/manuelblancovalentin/tensorplot'

""" Init paths """
import os
__toolbox_dir__ = os.path.dirname(tp.__file__)
__root_dir__ = (os.sep).join(__toolbox_dir__.split(os.sep)[:-1])
__fonts_dir__ = os.path.join(__toolbox_dir__, '__res__', 'fonts')
__css_dir__ = os.path.join(__toolbox_dir__, '__res__', 'css')

""" Import css refs """
import json
__css_refs__ = os.path.join(__css_dir__,'layers_styles.json')

__layers_css__ = dict()
if os.path.isfile(__css_refs__):
    with open(__css_refs__,'r', encoding='utf-8') as fjson:
        __layers_css__ = json.load(fjson)
