import io
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, "README.rst"), "rt", encoding="utf8") as f:
    readme = f.read()

about = {}
with io.open(os.path.join(here, "grvlmsdiscovery", "__about__.py"), "rt", encoding="utf-8") as f:
    exec(f.read(), about)


setup(
    name="grvlms-discovery",
    version=about["__version__"],
    url="https://docs.grvlms.overhang.io/",
    project_urls={
        "Documentation": "https://docs.grvlms.overhang.io/",
        "Code": "https://github.com/overhangio/grvlms-discovery",
        "Issue tracker": "https://github.com/overhangio/grvlms-discovery/issues",
        "Community": "https://discuss.overhang.io",
    },
    license="AGPLv3",
    author="Overhang.io",
    author_email="contact@overhang.io",
    description="A Grvlms plugin for course discovery, the Open edX service for providing access to consolidated course and program metadata",
    long_description=readme,
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    install_requires=["grvlms-openedx"],
    python_requires=">=3.5",
    entry_points={"grvlms.plugin.v0": ["discovery = grvlmsdiscovery.plugin"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
