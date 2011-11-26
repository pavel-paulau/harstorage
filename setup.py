try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='harstorage',
    version='0.5.1',
    description='Free repository for performance measurements',
    long_description="HAR Storage is repository for automated client-side performance testing. It's built on MongoDB and Pylons.",
    author='Pavel Paulau',
    author_email='Pavel.Paulau@gmail.com',
    url='http://harstorage.com/',
    license='BSD, see LICENSE.txt for details',
    install_requires=[
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'harstorage': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors={'harstorage': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', {'input_encoding': 'utf-8'}),
    #        ('public/**', 'ignore', None)]},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = harstorage.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
