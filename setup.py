from setuptools import find_packages
from setuptools import setup

setup(name='service_registry',
      version='0.0.1',
      description='a test task for studioh67',
      url='',
      author='Yuri Turchenkov',
      author_email='solarw@solarw.info',
      license='proprietary',
      packages=find_packages(),
      zip_safe=False,
      dependency_links=[
          'git+git://github.com/solarw/aiohttp-json-rpc@9dda76f0a7978ac70f00c3102291dcec1494f08c#egg=aiohttp-json-rpc-0.9.1-slw1',
      ],
      install_requires=['aiohttp', 'aiohttp-json-rpc==0.9.1-slw1'],
      )
