from __future__ import unicode_literals, print_function

import os

import setuptools

from bulk_update import VERSION

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setuptools.setup(
    name='django-bulk-update',
    version=VERSION,
    use_scm_version={'version_scheme': 'post-release'},
    author='Shakurov Vadim Vladimirovich',
    author_email='apelsinsd@gmail.com',
    url='https://github.com/newvadim/django-bulk-update',
    long_description=README,
    description='Bulk update given objects using minmal query over Django ORM.',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
