from setuptools import find_packages, setup

setup(
    name='COSC 381 - Movies Website',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask==2.0.3',
    ],
)

