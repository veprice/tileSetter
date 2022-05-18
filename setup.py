from setuptools import find_packages, setupsetup(
    name='pyleset',
    packages=find_packages(['pyleset']),
    version='0.1.0',
    description='Python library for tilesetting Neopets in the Neopian Pound',
    author='Cady | UN: penguinluver222',
    license='MIT',
    install_requires['pandas==1.2.4']
    include_package_data=True,
    package_data={'': ['data/*.csv']}
)
