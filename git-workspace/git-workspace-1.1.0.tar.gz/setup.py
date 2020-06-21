from distutils.core import setup

with open("VERSION", "r") as vfile:
    version_line = vfile.readline()

version = version_line.strip()

setup(
    name="git-workspace",
    packages=["."],
    include_package_data=True,
    package_data={
        "": ["CHANGELOG.md", "VERSION", "README.md"]
    },
    version=version,
    license="MIT",
    description="Git 'extension' for managing multirepo workspaces",
    author="Aki Mäkinen",
    author_email="nenshou.sora@gmail.com",
    url="https://gitlab.com/blissfulreboot/python/git-workspace",
    keywords=["Git", "Workspace"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6"
    ],
    scripts=[
        "git-ws"
    ]
)
