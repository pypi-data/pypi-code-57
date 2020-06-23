from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="mongoengine_pagination",
    version="0.1.5",
    keywords=["mongoengine", "pagination", 'mongodb', "fastapi", 'nosql'],
    description="=======you can use this toll to paginate your querysets=======",
    long_description=long_description,

    # long_description="for example ---> User.objects().paginate(page_index, page_size).items",

    # long_description="===========how to use?==========="
    #                  "*******example*******"
    #                  "class User(DocumentPro):   "
    #                  "user_id = IntField() "
    #                  "name = StringField()"
    #                  "page_index = 2"
    #                  "page_size = 20"
    #                  "user_list = User.objects().paginate(page_index, page_size)"
    #                  "result_list = result.items"
    #                  "total_items = result.total total_page = result.pages",

    license="MIT Licence",

    author="yangqi",
    author_email="geekpaul@outlook.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['mongoengine==0.20.0',
                      'pip==20.1.1',
                      'pymongo==3.10.1']
)
