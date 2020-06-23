# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['contact', 'contact.migrations', 'contact.tests']

package_data = \
{'': ['*'], 'contact': ['templates/*', 'templates/email/*']}

install_requires = \
['giant-mixins>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'giant-contact',
    'version': '0.3.7',
    'description': 'Adds a generic contact app for use with Giant projects',
    'long_description': '# Giant Contact\n\nA re-usable package which can be used in any project that requires a generic `Contact` app. \n\nThis will include the basic formatting and functionality such as model creation via the admin and email sending.\n\n## Installation\n\nTo install with the package manager, run:\n\n    $ poetry add giant-contact\n\nYou should then add `"contact"` to the `INSTALLED_APPS` in `base.py` and to the `Makefile`.  \n\nIn `base.py` there should also be a `DEFAULT_FROM_EMAIL` and a `DEFAULT_TO_EMAIL`. This is used by the email sending method.\n\n\n## Configuration\n\nThis application exposes the following settings:\n\n- `DEFAULT_FROM_EMAIL` is the `From` address in the email.\n- `DEFAULT_TO_EMAIL` is the default recipient. This is usually the client\'s address.\n- `CONTACT_ABSOLUTE_URL` allows the user to set a different URL as used in the `get_absolute_url` method\n- `CONTACT_SUCCESS_URL` allows the user to set a different success URL\n\n- `CONTACT_EMAIL_TEMPLATE_HTML` is the path to the email\'s HTML representation.\n- `CONTACT_EMAIL_TEMPLATE_TXT` is the path to the email\'s text representation.\n\n- `CONTACT_ADMIN_LIST_DISPLAY` is the field list for the admin index. This must be a list\n- `CONTACT_ADMIN_FIELDSETS` allows the user to define the admin fieldset. This must be a list of two-tuples\n- `CONTACT_ADMIN_READONLY_FIELDS` allows the user to configure readonly fields in the admin. This must be a list\n\n- `CONTACT_FORM_FIELDS` allows the user to customise what fields are displayed on the contact form. This must be a list\n- `CONTACT_FORM_FIELD_PLACEHOLDERS` allows the user to customise the field placeholder text. This must be a dict containing the fieldnames\n- `CONTACT_FORM_REQUIRED_FIELDS` allows the user to customise what fields are required on the contact form. This must be a list\n- `CONTACT_FORM_LABELS` allows the user to customise what the field labels are on the contact form. This must be a dict of field names and their corresponding label\n- `CONTACT_FORM_WIDGETS` allows the user to customise what the field widgets are on the contact form. This must be a dict of field names and their corresponding widget\n\n## URLs\n\nAdd the following to `core.urls` for general functionality:\n\n    path("contact/", include("contact.urls"), name="contact"),\n\nIf you want to customize the urls to include a different path and/or templates, first you must import `contact.views` in `core.urls` and then you could do add the following:\n\n    path("contact-us/", contact.views.EnquiryFormView.as_view({"template_name": "custom_template_name.html}), name=contact-us)\n    path("contact-us/success/", contact.views..SuccessView.as_view(), name=contact-success)\n \n ## Context Processor\n If you wish to use the Contact form with the context processor you will need to add `contact.context_processors.enquiry_form` into the `TEMPLATES` context processors list. This will allow you to access the form in templates.\n \n ## Preparing for release\n \n In order to prep the package for a new release on TestPyPi and PyPi there is one key thing that you need to do. You need to update the version number in the `pyproject.toml`.\n This is so that the package can be published without running into version number conflicts. The version numbering must also follow the Semantic Version rules which can be found here https://semver.org/.\n \n ## Publishing\n \n Publishing a package with poetry is incredibly easy. Once you have checked that the version number has been updated (not the same as a previous version) then you only need to run two commands.\n \n    $ `poetry build` \n\nwill package the project up for you into a way that can be published.\n \n    $ `poetry publish`\n\nwill publish the package to PyPi. You will need to enter the username and password for the account which can be found in the company password manager',
    'author': 'Will-Hoey',
    'author_email': 'will.hoey@giantmade.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/giantmade/giant-contact',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
