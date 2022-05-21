from setuptools import find_packages, setupsetup(
    name='pyleset',
    packages=find_packages(['pyleset']),
    version='0.1.0',
    description='Python library for tilesetting Neopets in the Neopian Pound',
    long_description=open('README.md').read(),
    author='Cady | UN: penguinluver222',
    license='MIT',
    url='https://github.com/veprice/tileSetter/'
    install_requires['pandas==1.2.4','numpy']
    include_package_data=True,
    package_data={'': ['data/*.csv']}
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ]
)
