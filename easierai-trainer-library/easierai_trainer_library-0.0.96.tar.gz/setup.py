"""
/**
 * Copyright  2020 Atos Spain SA. All rights reserved.
 *
 * This file is part of EASIER.AI.
 *
 * EASIER.AI is free software: you can redistribute it and/or modify it under the terms of GNU Affero General 
 * Public License as published by the Free Software Foundation, either version 3 of the License or 
 * any later version.
 *
 * THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT ANY WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
 * BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT,
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
 * OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *
 * See DISCLAIMER file for the full disclaimer information and LICENSE file for full license information 
 * in the project root.
 */
 """

from setuptools import setup, find_packages
 
setup(name='easierai_trainer_library',
      version='0.0.96',
      url='https://scm.atosresearch.eu/ari/easier/trainer-library',
      license='ATOS',
      author='AIR Unit',
      author_email='adrian.arroyo@atos.net',
      description='This library contains AI code for training purposes.',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      packages=find_packages(),
      install_requires =[
            'flask',
            'flask-api',
            'flask_monitoringdashboard',
            'sklearn',
            'easierai-elasticsearchlib',
            'easierai-common-functions',
            'tensorflow',
            'configparser',
            'numpy',
            'pandas',
            'joblib',
            'keras',
            'datetime',
            'pydash',
            'phased_lstm_keras',
            'schedule',
            'minio',
            'modin[ray]'
      ],
      zip_safe=False)
