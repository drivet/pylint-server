"""
pylint-server
----

A small Flask application to keep keep track of pylint reports and ratings
on a per-repository basis.
"""
from setuptools import setup


setup(
    name='pylint-server',
    version='0.1',
    url='https://github.com/drivet/pylint-server/',
    license='MIT',
    author='Desmond Rivet',
    author_email='desmond.rivet@gmail.com',
    description='A Flask application to keep keep track of pylint information',
    long_description=__doc__,
    py_modules=['pylint-server'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'TravisPy'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Version Control',
    ],
)
