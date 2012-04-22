import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()

requires = [
    'SQLAlchemy',
    'pytz'
]

setup(name='athanor',
      version='0.0',
      description='transit',
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        ],
      author='',
      author_email='',
      url='',
      keywords='sqlalchemy',
      packages=find_packages(),
      include_package_data=False,
      zip_safe=True,
      test_suite='athanor',
      install_requires=requires,
      entry_points="""\
      """,
      )

