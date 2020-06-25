# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['news', 'news.migrations', 'news.tests']

package_data = \
{'': ['*'], 'news': ['templates/*']}

install_requires = \
['django-filer>=1.7.1,<2.0.0', 'giant-mixins>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'giant-news',
    'version': '0.1.2.1',
    'description': 'A small reusable package that adds a News app to a project',
    'long_description': '# Giant News\n\nA re-usable package which can be used in any project that requires a generic `News` app. \n\nThis will include the basic formatting and functionality such as model creation via the admin.\n\n## Installation\n\nTo install with the package manager, run:\n\n    $ poetry add giant-news\n\nYou should then add `"news", "easy_thumbnails" and "filer"` to the `INSTALLED_APPS` in `base.py`.  \n\n\n## Configuration\n\nThis application exposes the following settings:\n\n- `ARTICLETAG_ADMIN_LIST_DISPLAY` is the field list for the admin index. This must be a list\n- `ARTICLETAG_ADMIN_FIELDSETS` allows the user to define the admin fieldset. This must be a list of two-tuples\n- `ARTICLETAG_ADMIN_READONLY_FIELDS` allows the user to configure readonly fields in the admin. This must be a list\n\n- `ARTICLE_ADMIN_LIST_DISPLAY`is the field list for the admin index. This must be a list\n- `ARTICLE_ADMIN_SEARCH_FIELDS` allows the user to configure search fields in the admin. This must be a list\n- `ARTICLE_ADMIN_FIELDSETS` allows the user to define the admin fieldset. This must be a list of two-tuples\n- `ARTICLE_ADMIN_READONLY_FIELDS` allows the user to configure readonly fields in the admin. This must be a list\n\n- `AUTHOR_ADMIN_LIST_DISPLAY`  is the field list for the admin index. This must be a list\n- `AUTHOR_ADMIN_FIELDSETS` allows the user to define the admin fieldset. This must be a list of two-tuples\n- `AUTHOR_ADMIN_READONLY_FIELDS` allows the user to configure readonly fields in the admin. This must be a list\n\n## URLs\n\nAdd the following to `core.urls` for general functionality:\n\n    path("news/", include("news.urls"), name="news"),\n\nIf you want to customize the urls to include a different path and/or templates, first you must import `from news import views as news_views` in `core.urls` and then you could add the following:\n\n    path("news/", news_views.ArticleIndex.as_view(template_name="news/index.html"), name="news-index"),\n    path("news/<slug:slug>/", news_views.ArticleDetail.as_view(template_name="news/detail.html"), name="news-detail"),\n \n ## Preparing for release\n \n In order to prep the package for a new release on TestPyPi and PyPi there is one key thing that you need to do. You need to update the version number in the `pyproject.toml`.\n This is so that the package can be published without running into version number conflicts. The version numbering must also follow the Semantic Version rules which can be found here https://semver.org/.\n \n ## Publishing\n \n Publishing a package with poetry is incredibly easy. Once you have checked that the version number has been updated (not the same as a previous version) then you only need to run two commands.\n \n    $ `poetry build` \n\nwill package the project up for you into a way that can be published.\n \n    $ `poetry publish`\n\nwill publish the package to PyPi. You will need to enter the username and password for the account which can be found in the company password manager',
    'author': 'Will-Hoey',
    'author_email': 'will.hoey@giantmade.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/giantmade/giant-news',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
