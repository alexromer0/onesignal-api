from setuptools import find_packages
from distutils.core import setup

setup(
    name='onesignalapi',
    packages=find_packages(),
    version='0.6',
    description='One Signal API SDK https://onesignal.com',
    author='Alejandro Romero',
    author_email='ealejandrorg@gmail.com',
    url='https://github.com/alexromer0/onesignal-api.git',
    download_url='https://github.com/alexromer0/onesignal-api.git/tarball/0.6',
    keywords=['OneSignal', 'Notifications', 'Push'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3', ], install_requires=['pytz', 'requests']
)
