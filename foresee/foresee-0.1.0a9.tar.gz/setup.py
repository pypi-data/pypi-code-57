import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
					name='foresee',
					version='0.1.0a9',
					author='Hamid Mohammadi',
					author_email='hmohammadi6545@gmail.com',
					description='Generate forecasts using several time series forecasting models in python.',
					long_description=long_description,
					long_description_content_type='text/markdown',
					url='https://github.com/HamidM6/foresee',
					packages=setuptools.find_packages(),
					classifiers=[
						'Development Status :: 3 - Alpha',
						"Programming Language :: Python :: 3",
						"License :: OSI Approved :: MIT License",
						"Operating System :: OS Independent",
					],
					include_package_data=True,
				)