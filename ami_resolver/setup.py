from setuptools import setup

setup(
    name='ami_resolver',
    py_modules=['ami_resolver'],
    entry_points={
        'sceptre.resolvers': [
            'ami_resolver = ami_resolver:Ami_resolver',
        ],
    }
)
