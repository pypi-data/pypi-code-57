from distutils.core import setup
setup(
  name = 'torchRDS',
  packages = ['torchRDS'],
  version = '0.1',
  license='MIT',
  description = 'Reinforced Data Sampling for Model Diversification',
  author = 'Harry Nguyen',
  author_email = 'harry.nguyen@outlook.com',
  url = 'https://github.com/probeu/RDS',
  download_url = 'https://github.com/probeu/RDS/archive/v_01.tar.gz',
  keywords = ['Data-Sampling', 'Reinforcement-Learning', 'Machine-Learning'],
  install_requires=[
          'numpy',
          'torch',
          'scikit-learn',
          'pandas',
          'tqdm'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
  ],
)