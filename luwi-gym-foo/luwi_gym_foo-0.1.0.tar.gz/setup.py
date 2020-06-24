import setuptools
from pathlib import Path

setuptools.setup(
    name='luwi_gym_foo',
    version='0.1.0',
    description="A OpenAI Gym Env for foo",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include="luwi_gym_foo*"),
    install_requires=['gym']  # And any other dependencies foo needs
)

