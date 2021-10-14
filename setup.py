from setuptools import setup, find_packages

setup(
    name='MetaStruct',
    version='1.0.0',
    description='This package is a basic implicit geometry tool.',
    author='Toby Wilkinson',
    author_email='toby.wilkinson339@gmail.com',
    url='https://github.com/wilko339/MetaStruct.git',
    packages=find_packages(exclude=('test*', 'testing*')),
    entry_points={
        'console_scripts': ['MetStruct-cli = ']
    }
)