
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='annotations',
    version='0.1.0',
    description='Export 3d Annotations',
    long_description=readme,
    author='Hrvoje Marinovic,
    author_email='hrvoje.marinovich@gmail.com',
#    url='https://github.com/',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

