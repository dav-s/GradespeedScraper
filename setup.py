
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(name='GradespeedScraper',
      version='0.1-dev',
      description='Scrapes Gradespeed',
      author='Davis Robertson',
      author_email='davis@daviskr.com',
      license='MIT',
      url='https://github.com/epicdavi/GradespeedScraper/',
      install_requires=['mechanize>=0.2.5', 'beautifulsoup4>=4.3.x,<4.4'],
      )