
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(name='GradespeedScraper',
      version='0.1',
      description='Scrapes Gradespeed',
      author='Davis Robertson',
      author_email='davis@daviskr.com',
      url='https://github.com/epicdavi/GradespeedScraper/',
      install_requires=['mechanize', 'beautifulsoup4'],
      )