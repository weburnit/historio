from setuptools import setup

setup(
    name='historio',
    packages=['historio', 'historio.client', 'historio.core', 'historio.definition'],
    include_package_data=True,
    version='0.2',
    install_requires=[
        'mongoengine',
        'grpcio',
        'grpcio-tools',
        'python-json-logger'
    ],
)
