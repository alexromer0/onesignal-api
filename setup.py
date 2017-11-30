from setuptools import find_packages
from distutils.core import setup

setup(
    name='onesignalapi',
    packages=find_packages(),  # this must be the same as the name above
    version='0.1',
    description='One Signal API SDK https://onesignal.com',
    author='Alejandro Romero',
    author_email='ealejandrorg@gmail.com',
    url='https://github.com/alexromer0/onesignal-api.git',  # use the URL to the github repo
    download_url='https://github.com/alexromer0/onesignal-api.git/tarball/0.1',
    keywords=['OneSignal', 'Notifications', 'Push'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',],
)
