
from setuptools import setup, Extension

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
  name = 'explainx',         # How you named your package folder (MyLib)
  packages = ['explainx'],   # Chose the same as "name"
  version = '1.9',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'State of the art to explain any blackbox Machine Learning model.',   # Give a short description about your library
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'explainx.ai',                   # Type in your name
  author_email = 'muddassar@explainx.ai',      # Type in your E-Mail
  url = 'https://github.com/explainX/explainx',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/explainX/explainx/archive/v_13.zip',    # I explain this later on
  keywords = ['Explainable AI', 'Explainable Machine Learning', 'trust', "interpretability", "transparent"],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'jupyter_dash',
          'dash_bootstrap_components',
          'dash',
          'dash_core_components',
          'dash_html_components',
          'plotly',
          'dash_table',
          'pandas',
          'numpy',
          'dash_bootstrap_components',
          'shap',
          'xgboost==1.0.2',
          'cvxopt',
           'scikit-learn',
           'sklearn',
           'scipy',
            'catboost',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
    package_data={"explainx":["lib/*", "tutorials/*", "datasets/*"]},
)
