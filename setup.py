from setuptools import setup, find_packages

setup(
    name='harstorage',
    version='0.6',
    description='Free repository for performance measurements',
    long_description="HAR Storage is repository for automated client-side performance testing. It's built on MongoDB and Pylons.",
    author='Pavel Paulau',
    author_email='Pavel.Paulau@gmail.com',
    url='http://harstorage.com/',
    license='BSD, see LICENSE.txt for details',
	platforms=['Linux', 'Windows'],
    setup_requires=[],
	install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'harstorage': ['i18n/*/LC_MESSAGES/*.mo']},
    zip_safe=False,
    paster_plugins=[],
    entry_points="""
    [paste.app_factory]
    main = harstorage.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)