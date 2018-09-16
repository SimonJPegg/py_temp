from setuptools import setup

setup(name='py_temp',
      version='0.0.1',
      description='Heating control system',
      packages=['py_temp'],
      install_requires=[
          'apscheduler>=3.5.3',
          'RPi.GPIO>=0.6.3'
      ],
      entry_points={
          'console_scripts': [
              'py_temp = py_temp.__main__:main'
          ]
      })