from setuptools import setup

setup(name='dm',
      version='1.0',
      description='OpenShift App',
      author='zsun',
      author_email='example@example.com',
      url='http://www.python.org/sigs/distutils-sig/',
#      install_requires=['Django>=1.3'],
      install_requires=['Flask>=0.10.1'],
	  install_requires=['redis>=2.10.1'],
	  install_requires=['gevent>=1.0.0'],
	  install_requires=['Werkzeug>=0.9.0'],
     )