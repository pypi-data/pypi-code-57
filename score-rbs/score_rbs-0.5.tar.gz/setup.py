import os
from setuptools import setup, find_packages


def readme():
	with open("README.md", "r") as fh:
		long_desc = fh.read()
	return long_desc

def get_version():
    with open("VERSION", 'r') as f:
        v = f.readline().strip()
        return v

def main():
	setup (
		name = 'score_rbs',
		version = get_version(),
		author = "Katelyn McNair, Gary J Olsen",
		author_email = "deprekate@gmail.com",
		description = 'A tool to score prokaryotic ribosomal binding sites',
		long_description = readme(),
		long_description_content_type="text/markdown",
		url =  "https://github.com/deprekate/score_rbs",
		#scripts=['score_rbs.py'],
		classifiers=[
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
			"Operating System :: OS Independent",
		],
		python_requires='>3.5.2',
		packages=find_packages()
	)


if __name__ == "__main__":
	main()
