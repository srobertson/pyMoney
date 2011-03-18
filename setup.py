from setuptools import setup

setup(
    name='pyMoney',
    version = '1.2.31',
    description ='An implementation of a money type for Python 2.2 >',
    license="Apache License 2.0",

    long_description=("An implementation of the money type as described "
                "in 'Patterns of Enterprise Application Architecture.'"),
    
    url='http://github.com/srobertson/pyMoney',
    packages = ['Money'],           
    author='Scott Robertson',
    author_email='srobertson@codeit.com',

)