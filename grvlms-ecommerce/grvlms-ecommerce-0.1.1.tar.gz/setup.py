import io
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, "README.rst"), "rt", encoding="utf8") as f:
    readme = f.read()

about = {}
with io.open(os.path.join(here, "grvlmsecommerce", "__about__.py"), "rt", encoding="utf-8") as f:
    exec(f.read(), about)

setup(
    name="grvlms-ecommerce",
    version=about["__version__"],
    url="https://docs.grvlms.groove.education/",
    project_urls={
        "Documentation": "https://docs.grvlms.groove.education",
        "Code": "https://github.com/groovetch/grvlms-ecommerce",
        "Issue tracker": "https://github.com/groovetch/grvlms-ecommerce/issues",
        "Community": "https://groove.education",
    },
    license="AGPLv3",
    author="GrooveTechnology",
    author_email="thuan.ha@groovetechnology.com",
    description="Ecommerce plugin for Grvlms",
    long_description=readme,
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    python_requires=">=3.5",
    install_requires=["grvlms-openedx>=0.0.1", "grvlms-discovery"],
    entry_points={"grvlms.plugin.v0": ["ecommerce = grvlmsecommerce.plugin"]},
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
