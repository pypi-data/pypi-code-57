"microapp setup module."


def main():

    import sys

    from setuptools import setup
    from microapp.project import MicroappProject as prj

    if sys.version_info >= (3, 0):
        install_requires = []

    else:
        install_requires = ["enum", "typing"]

    console_scripts = ["microapp=microapp.__main__:main"]

    setup(
        name=prj._name_,
        version=prj._version_,
        description=prj._description_,
        long_description=prj._long_description_,
        author=prj._author_,
        author_email=prj._author_email_,
        url=prj._url_,
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Topic :: Software Development :: Build Tools",
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
        ],
        keywords="microapp",
        packages=[ "microapp" ],
        include_package_data=True,
        install_requires=install_requires,
        entry_points={ "console_scripts": console_scripts },
        test_suite="tests.microapp_unittest_suite",
        project_urls={
            "Bug Reports": "https://github.com/grnydawn/microapp/issues",
            "Source": "https://github.com/grnydawn/microapp",
        }
    )

if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()
    main()
